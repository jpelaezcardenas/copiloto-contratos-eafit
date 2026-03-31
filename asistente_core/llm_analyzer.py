"""Integración con LLM (Groq y Gemini como fallback) para análisis de contratos."""

import json
import re
import streamlit as st
import os
from groq import Groq
try:
    import google.generativeai as genai
except ImportError:
    pass

from config.settings import LLM_MODEL, LLM_TEMPERATURE, LLM_MAX_TOKENS, RISK_CATEGORIES

def get_groq_client():
    """Crea el cliente de Groq (Nativo)."""
    api_key = st.secrets.get("GROQ_API_KEY") or os.environ.get("GROQ_API_KEY")
    if not api_key:
        return None
    return Groq(api_key=api_key)

def analyze_contract(contract_text: str) -> dict:
    """Analiza un contrato con fallback dinámico entre Groq y Gemini."""
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

    # 2. Fallback a Gemini (usando SDK estable)
    gemini_key = st.secrets.get("GEMINI_API_KEY") or os.environ.get("GEMINI_API_KEY")
    if gemini_key:
        try:
            genai.configure(api_key=gemini_key)
            # Gemini 1.5 Flash es el más estable y rápido para fallback
            model = genai.GenerativeModel("gemini-1.5-flash")
            full_prompt = f"{SYSTEM_PROMPT}\n\n{prompt}"
            
            response = model.generate_content(
                full_prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=LLM_TEMPERATURE,
                    max_output_tokens=LLM_MAX_TOKENS,
                    response_mime_type="application/json",
                ),
            )
            return _parse_llm_response(response.text)
        except Exception as ge:
            st.error(f"Gemini falló: {str(ge)}")
            raise Exception("No fue posible obtener respuesta de ningún motor inteligente.")
    
    raise Exception("Límite de Groq alcanzado y Gemini no está configurado.")

def _parse_llm_response(raw_text: str) -> dict:
    """Parsea la respuesta para asegurar un dict válido."""
    try:
        return json.loads(raw_text)
    except json.JSONDecodeError:
        clean = re.sub(r"^```(?:json)?\s*\n?", "", raw_text)
        clean = re.sub(r"\n?```\s*$", "", clean)
        clean = clean.strip()
        try:
            return json.loads(clean)
        except json.JSONDecodeError:
            match = re.search(r"(\{[\s\S]*\})", clean)
            if match:
                try:
                    return json.loads(match.group(1))
                except:
                    pass
        
        return {
            "error": True,
            "mensaje": "Formato JSON no válido.",
            "respuesta_cruda": raw_text[:2000],
            "semaforo": "ALTO",
        }

def compare_contracts(contract1_text: str, contract2_text: str) -> dict:
    """Compara dos contratos usando cualquier servicio disponible."""
    from asistente_core.prompts import SYSTEM_PROMPT, COMPARISON_PROMPT
    
    max_chars = 15_000 
    c1 = contract1_text[:max_chars] if len(contract1_text) > max_chars else contract1_text
    c2 = contract2_text[:max_chars] if len(contract2_text) > max_chars else contract2_text
    prompt = COMPARISON_PROMPT.replace("{contract_1}", c1).replace("{contract_2}", c2)

    # Lógica simplificada: Groq -> Gemini
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
            genai.configure(api_key=gemini_key)
            model = genai.GenerativeModel("gemini-1.5-flash")
            response = model.generate_content(
                f"{SYSTEM_PROMPT}\n\n{prompt}",
                generation_config={"response_mime_type": "application/json"}
            )
            return _parse_llm_response(response.text)
    except:
        pass

    return {"error": True, "mensaje": "Comparación no disponible."}
