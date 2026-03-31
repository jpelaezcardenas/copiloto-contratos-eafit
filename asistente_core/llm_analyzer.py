"""Integración con LLM (Groq y Gemini como fallback) para análisis de contratos."""

import json
import re
import streamlit as st
import os
import requests
from groq import Groq

from config.settings import LLM_MODEL, LLM_TEMPERATURE, LLM_MAX_TOKENS, RISK_CATEGORIES

def get_groq_client():
    """Crea el cliente de Groq (Nativo)."""
    api_key = st.secrets.get("GROQ_API_KEY") or os.environ.get("GROQ_API_KEY")
    if not api_key:
        return None
    return Groq(api_key=api_key)

def analyze_contract(contract_text: str) -> dict:
    """Analiza un contrato con fallback dinámico entre Groq y Gemini (REST API)."""
    from asistente_core.prompts import SYSTEM_PROMPT, ANALYSIS_PROMPT
    
    max_chars = 30_000
    if len(contract_text) > max_chars:
        contract_text = contract_text[:max_chars] + "\n\n[... DOCUMENTO TRUNCADO ...]"
    prompt = ANALYSIS_PROMPT.replace("{{CONTRACT_TEXT}}", contract_text)

    # 1. Intentar con Groq
    groq_client = get_groq_client()
    if groq_client:
        try:
            response = groq_client.chat.completions.create(
                model=LLM_MODEL,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": prompt},
                ],
                temperature=LLM_TEMPERATURE,
                max_tokens=LLM_MAX_TOKENS,
                response_format={"type": "json_object"}
            )
            return _parse_llm_response(response.choices[0].message.content.strip())
        except Exception as e:
            msg = str(e).lower()
            if "429" in msg or "rate_limit" in msg:
                st.warning("⚠️ Límite de Groq alcanzado. Cambiando automáticamente a motor secundario (Gemini)...")
            else:
                st.info(f"Groq temporalmente fuera de línea, probando Gemini...")

    # 2. Fallback a Gemini (usando REST API Nativa para evitar errores 404 de SDK)
    gemini_key = st.secrets.get("GEMINI_API_KEY") or os.environ.get("GEMINI_API_KEY")
    if gemini_key:
        try:
            # URL oficial de la API de Gemini (v1beta es la más estable para modelos Flash nuevos)
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={gemini_key}"
            
            payload = {
                "contents": [{
                    "parts": [{"text": f"{SYSTEM_PROMPT}\n\n{prompt}"}]
                }],
                "generationConfig": {
                    "temperature": LLM_TEMPERATURE,
                    "maxOutputTokens": LLM_MAX_TOKENS,
                    "responseMimeType": "application/json"
                }
            }
            
            headers = {'Content-Type': 'application/json'}
            response = requests.post(url, headers=headers, json=payload, timeout=60)
            
            if response.status_code == 200:
                result = response.json()
                # La estructura de Gemini es: candidates[0].content.parts[0].text
                raw_text = result['candidates'][0]['content']['parts'][0]['text']
                return _parse_llm_response(raw_text)
            else:
                # Si falla v1beta, intentamos con v1 (estándar)
                url_v1 = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={gemini_key}"
                response = requests.post(url_v1, headers=headers, json=payload, timeout=60)
                if response.status_code == 200:
                    result = response.json()
                    raw_text = result['candidates'][0]['content']['parts'][0]['text']
                    return _parse_llm_response(raw_text)
                else:
                    st.error(f"Error de API Gemini ({response.status_code}): {response.text}")
                    raise Exception("Falla crítica en motor secundario.")
                    
        except Exception as ge:
            st.error(f"Gemini (Native) falló: {str(ge)}")
            raise Exception("Ningún motor inteligente pudo procesar el contrato.")
    
    raise Exception("Límite de Groq alcanzado y Gemini no está configurado.")

def _parse_llm_response(raw_text: str) -> dict:
    """Parsea la respuesta para asegurar un dict válido."""
    try:
        clean = re.sub(r"^```(?:json)?\s*\n?", "", raw_text)
        clean = re.sub(r"\n?```\s*$", "", clean)
        clean = clean.strip()
        return json.loads(clean)
    except json.JSONDecodeError:
        match = re.search(r"(\{[\s\S]*\})", raw_text)
        if match:
            try:
                return json.loads(match.group(1))
            except:
                pass
        
        return {
            "error": True,
            "mensaje": "Respuesta no estructurada.",
            "respuesta_cruda": raw_text[:2000],
            "semaforo": "ALTO",
        }

def compare_contracts(contract1_text: str, contract2_text: str) -> dict:
    """Compara dos contratos usando Groq o Gemini Nativo."""
    from asistente_core.prompts import SYSTEM_PROMPT, COMPARISON_PROMPT
    
    max_chars = 15_000 
    c1 = contract1_text[:max_chars] if len(contract1_text) > max_chars else contract1_text
    c2 = contract2_text[:max_chars] if len(contract2_text) > max_chars else contract2_text
    prompt = COMPARISON_PROMPT.replace("{contract_1}", c1).replace("{contract_2}", c2)

    # Lógica simplificada: Groq -> Gemini (Native)
    try:
        client = get_groq_client()
        if client:
            response = client.chat.completions.create(
                model=LLM_MODEL,
                messages=[{"role": "system", "content": SYSTEM_PROMPT},{"role": "user", "content": prompt}],
                temperature=LLM_TEMPERATURE, max_tokens=LLM_MAX_TOKENS,
                response_format={"type": "json_object"}
            )
            return _parse_llm_response(response.choices[0].message.content.strip())
    except:
        pass

    try:
        gemini_key = st.secrets.get("GEMINI_API_KEY") or os.environ.get("GEMINI_API_KEY")
        if gemini_key:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={gemini_key}"
            payload = {
                "contents": [{"parts": [{"text": f"{SYSTEM_PROMPT}\n\n{prompt}"}]}],
                "generationConfig": {"responseMimeType": "application/json"}
            }
            response = requests.post(url, json=payload, timeout=60)
            if response.status_code == 200:
                raw_text = response.json()['candidates'][0]['content']['parts'][0]['text']
                return _parse_llm_response(raw_text)
    except:
        pass

    return {"error": True, "mensaje": "Comparación no disponible."}
