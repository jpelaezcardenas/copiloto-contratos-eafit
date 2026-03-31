"""Integración con LLM (Groq y Gemini como fallback) para análisis de contratos."""

import json
import re
import streamlit as st
import os
from groq import Groq
try:
    from google import genai
    from google.genai import types
except ImportError:
    # Fallback si no está instalado el nuevo SDK
    pass

from config.settings import LLM_MODEL, LLM_TEMPERATURE, LLM_MAX_TOKENS, RISK_CATEGORIES

def get_groq_client():
    """Crea el cliente de Groq (Nativo)."""
    api_key = st.secrets.get("GROQ_API_KEY") or os.environ.get("GROQ_API_KEY")
    if not api_key:
        return None
    return Groq(api_key=api_key)

def get_gemini_client():
    """Crea el cliente de Gemini (Google GenAI)."""
    # Intentar obtener de secrets o de os.environ
    gemini_key = st.secrets.get("GEMINI_API_KEY") or os.environ.get("GEMINI_API_KEY")
    
    if not gemini_key:
        return None
    try:
        return genai.Client(api_key=gemini_key)
    except Exception as e:
        st.error(f"Error inicializando Gemini SDK: {str(e)}")
        return None

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

    # 2. Fallback a Gemini
    gemini_client = get_gemini_client()
    if gemini_client:
        try:
            full_prompt = f"{SYSTEM_PROMPT}\n\n{prompt}"
            # Probamos primero el 2.0 y si falla el 1.5 que es el estándar
            try:
                model_to_use = "gemini-2.0-flash"
                response = gemini_client.models.generate_content(
                    model=model_to_use,
                    contents=full_prompt,
                    config=types.GenerateContentConfig(
                        temperature=LLM_TEMPERATURE,
                        max_output_tokens=LLM_MAX_TOKENS,
                        response_mime_type="application/json"
                    )
                )
            except:
                model_to_use = "gemini-1.5-flash" # Fallback a 1.5 si 2.0 falla por región
                response = gemini_client.models.generate_content(
                    model=model_to_use,
                    contents=full_prompt,
                    config=types.GenerateContentConfig(
                        temperature=LLM_TEMPERATURE,
                        max_output_tokens=LLM_MAX_TOKENS,
                        response_mime_type="application/json"
                    )
                )
            
            return _parse_llm_response(response.text)
        except Exception as ge:
            st.error(f"Gemini falló también: {str(ge)}")
            raise Exception("No fue posible obtener respuesta de ningún motor inteligente.")
    
    raise Exception("Límite de Groq alcanzado y no hay API Key de Gemini configurada.")

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
            "mensaje": "Respuesta no estructurada.",
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
        client = get_gemini_client()
        if client:
            response = client.models.generate_content(
                model="gemini-1.5-flash", contents=f"{SYSTEM_PROMPT}\n\n{prompt}",
                config=types.GenerateContentConfig(response_mime_type="application/json")
            )
            return _parse_llm_response(response.text)
    except:
        pass

    return {"error": True, "mensaje": "Comparación no disponible."}
