"""Integración con LLM (Groq) para análisis de contratos."""

import json
import re
import streamlit as st
from groq import Groq
from config.settings import LLM_MODEL, LLM_TEMPERATURE, LLM_MAX_TOKENS, RISK_CATEGORIES

# No importaremos GROQ_API_KEY a nivel de módulo para evitar que sea estática si cambia el entorno

def get_client():
    """Crea el cliente de Groq (Nativo)."""
    # 1. Obtener clave de secrets (Cloud) o env (Local)
    api_key = st.secrets.get("GROQ_API_KEY", "")
    
    if not api_key:
        import os
        api_key = os.getenv("GROQ_API_KEY", "")

    if not api_key:
        raise ValueError(
            "❌ GROQ_API_KEY no configurada. "
            "Asegúrate de agregarla en los 'Secrets' de Streamlit Cloud."
        )
        
    return Groq(api_key=api_key)


def analyze_contract(contract_text: str) -> dict:
    """Analiza un contrato usando Groq y devuelve el análisis estructurado."""
    from asistente_core.prompts import SYSTEM_PROMPT, ANALYSIS_PROMPT
    client = get_client()

    # Truncar texto si es muy largo
    max_chars = 30_000
    if len(contract_text) > max_chars:
        contract_text = contract_text[:max_chars] + "\n\n[... DOCUMENTO TRUNCADO ...]"

    prompt = ANALYSIS_PROMPT.replace("{{CONTRACT_TEXT}}", contract_text)

    try:
        response = client.chat.completions.create(
            model=LLM_MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt},
            ],
            temperature=LLM_TEMPERATURE,
            max_tokens=LLM_MAX_TOKENS,
            response_format={"type": "json_object"}
        )
        
        raw_text = response.choices[0].message.content.strip()
        return _parse_llm_response(raw_text)
        
    except Exception as e:
        # Extraer mensaje de error legible para el usuario
        error_msg = str(e)
        if "401" in error_msg:
            error_msg = "Error 401: API Key inválida o no configurada en Streamlit Cloud Secrets."
        raise Exception(f"Error de comunicación con Groq: {error_msg}")


def _parse_llm_response(raw_text: str) -> dict:
    """Parsea la respuesta para asegurar un dict válido."""
    try:
        return json.loads(raw_text)
    except json.JSONDecodeError:
        # Limpieza de bloques de código markdown si existen
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
            "mensaje": "No se pudo parsear la respuesta de Groq.",
            "respuesta_cruda": raw_text[:2000],
            "identificacion": {},
            "obligaciones": {},
            "riesgos": [],
            "resumen_ejecutivo": "Error al procesar la respuesta con el motor de Groq.",
            "semaforo": "ALTO",
            "notas_adicionales": "Se requiere un nuevo análisis.",
        }


def compare_contracts(contract1_text: str, contract2_text: str) -> dict:
    """Compara dos contratos usando Groq."""
    from asistente_core.prompts import SYSTEM_PROMPT, COMPARISON_PROMPT
    client = get_client()

    max_chars = 15_000 
    c1 = contract1_text[:max_chars] if len(contract1_text) > max_chars else contract1_text
    c2 = contract2_text[:max_chars] if len(contract2_text) > max_chars else contract2_text

    prompt = COMPARISON_PROMPT.replace("{contract_1}", c1).replace("{contract_2}", c2)

    try:
        response = client.chat.completions.create(
            model=LLM_MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt},
            ],
            temperature=LLM_TEMPERATURE,
            max_tokens=LLM_MAX_TOKENS,
            response_format={"type": "json_object"}
        )
        
        raw_text = response.choices[0].message.content.strip()
        data = _parse_llm_response(raw_text)
        if "error" in data and data["error"]:
            return {
                "diferencias": [],
                "resumen_comparacion": "Error procesando comparación.",
                "error": True
            }
        return data
        
    except Exception as e:
        raise Exception(f"Error de comunicación con Groq (Comparación): {str(e)}")
