"""Integración con LLM (Groq y Gemini como fallback) para análisis de contratos."""

import json
import re
import streamlit as st
from groq import Groq
try:
    from google import genai
    from google.genai import types
except ImportError:
    # Fallback si no está instalado el nuevo SDK
    pass

from config.settings import LLM_MODEL, LLM_TEMPERATURE, LLM_MAX_TOKENS, RISK_CATEGORIES, GEMINI_API_KEY

def get_groq_client():
    """Crea el cliente de Groq (Nativo)."""
    api_key = st.secrets.get("GROQ_API_KEY", "")
    if not api_key:
        import os
        api_key = os.getenv("GROQ_API_KEY", "")
    if not api_key:
        return None
    return Groq(api_key=api_key)

def get_gemini_client():
    """Crea el cliente de Gemini (Google GenAI)."""
    if not GEMINI_API_KEY:
        return None
    try:
        return genai.Client(api_key=GEMINI_API_KEY)
    except:
        return None

def analyze_contract(contract_text: str) -> dict:
    """Analiza un contrato usando Groq con fallback automático a Gemini."""
    from asistente_core.prompts import SYSTEM_PROMPT, ANALYSIS_PROMPT
    
    # Preparar el prompt
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
            raw_text = response.choices[0].message.content.strip()
            return _parse_llm_response(raw_text)
        except Exception as e:
            if "429" in str(e) or "rate_limit" in str(e).lower():
                st.warning("⚠️ Límite de Groq alcanzado. Cambiando automáticamente a motor secundario (Gemini)...")
            else:
                st.error(f"Error en Groq: {str(e)}")
    
    # 2. Fallback a Gemini
    gemini_client = get_gemini_client()
    if gemini_client:
        try:
            full_prompt = f"{SYSTEM_PROMPT}\n\n{prompt}"
            # Usar Gemini 2.0 Flash que es gratuito y muy rápido
            response = gemini_client.models.generate_content(
                model="gemini-2.0-flash",
                contents=full_prompt,
                config=types.GenerateContentConfig(
                    temperature=LLM_TEMPERATURE,
                    max_output_tokens=LLM_MAX_TOKENS,
                    response_mime_type="application/json"
                )
            )
            return _parse_llm_response(response.text)
        except Exception as ge:
            raise Exception(f"Fallo crítico: Groq (Límite) y Gemini (Error: {str(ge)})")
    
    raise Exception("No hay servicios de IA disponibles (Verifica API Keys).")

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
            "mensaje": "No se pudo parsear la respuesta del modelo.",
            "respuesta_cruda": raw_text[:2000],
            "semaforo": "ALTO",
        }

def compare_contracts(contract1_text: str, contract2_text: str) -> dict:
    """Compara dos contratos usando Groq o Gemini."""
    from asistente_core.prompts import SYSTEM_PROMPT, COMPARISON_PROMPT
    
    max_chars = 15_000 
    c1 = contract1_text[:max_chars] if len(contract1_text) > max_chars else contract1_text
    c2 = contract2_text[:max_chars] if len(contract2_text) > max_chars else contract2_text
    prompt = COMPARISON_PROMPT.replace("{contract_1}", c1).replace("{contract_2}", c2)

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
        except Exception:
            pass # Fallback silencioso en comparación

    # 2. Fallback a Gemini
    gemini_client = get_gemini_client()
    if gemini_client:
        try:
            full_prompt = f"{SYSTEM_PROMPT}\n\n{prompt}"
            response = gemini_client.models.generate_content(
                model="gemini-2.0-flash",
                contents=full_prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json"
                )
            )
            return _parse_llm_response(response.text)
        except:
            pass

    return {"error": True, "mensaje": "Servicios de comparación no disponibles."}
