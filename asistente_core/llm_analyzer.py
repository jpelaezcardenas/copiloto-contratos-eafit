"""Integración con múltiples LLMs para máxima resiliencia (Groq, Cerebras, Mistral, Gemini, OpenRouter)."""

import json
import re
import streamlit as st
import os
import requests
from groq import Groq
from openai import OpenAI

from config.settings import LLM_MODEL, LLM_TEMPERATURE, LLM_MAX_TOKENS

def get_ai_response(prompt: str, system_prompt: str, is_json: bool = True) -> dict:
    """Intenta obtener una respuesta de múltiples proveedores de IA en orden de prioridad."""
    
    # Lista de proveedores configurados por prioridad y fiabilidad
    providers = [
        {
            "name": "Groq (Primario)",
            "key": st.secrets.get("GROQ_API_KEY") or os.environ.get("GROQ_API_KEY"),
            "type": "groq",
            "model": LLM_MODEL
        },
        {
            "name": "Cerebras (Respaldo Ultra-Rápido)",
            "key": st.secrets.get("CEREBRAS_API_KEY") or os.environ.get("CEREBRAS_API_KEY"),
            "type": "openai_compat",
            "base_url": "https://api.cerebras.ai/v1",
            "model": "llama-3.3-70b"
        },
        {
            "name": "Mistral (Análisis Jurídico)",
            "key": st.secrets.get("MISTRAL_API_KEY") or os.environ.get("MISTRAL_API_KEY"),
            "type": "openai_compat",
            "base_url": "https://api.mistral.ai/v1",
            "model": "mistral-large-latest"
        },
        {
            "name": "Gemini 2.0 (Respaldo Google)",
            "key": st.secrets.get("GEMINI_API_KEY") or os.environ.get("GEMINI_API_KEY"),
            "type": "gemini_rest",
            "model": "gemini-2.0-flash"
        },
        {
            "name": "OpenRouter (Seguro Final)",
            "key": st.secrets.get("OPENROUTER_API_KEY") or os.environ.get("OPENROUTER_API_KEY"),
            "type": "openai_compat",
            "base_url": "https://openrouter.ai/api/v1",
            "model": "meta-llama/llama-3.3-70b-instruct"
        }
    ]

    for p in providers:
        if not p["key"]:
            continue
            
        try:
            # st.info(f"Probando {p['name']}...") # Opcional: Para debug interno
            
            if p["type"] == "groq":
                client = Groq(api_key=p["key"])
                response = client.chat.completions.create(
                    model=p["model"],
                    messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": prompt}],
                    temperature=LLM_TEMPERATURE,
                    max_tokens=LLM_MAX_TOKENS,
                    response_format={"type": "json_object"} if is_json else None
                )
                return _parse_llm_response(response.choices[0].message.content.strip())

            elif p["type"] == "openai_compat":
                client = OpenAI(api_key=p["key"], base_url=p["base_url"])
                response = client.chat.completions.create(
                    model=p["model"],
                    messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": prompt}],
                    temperature=LLM_TEMPERATURE,
                    max_tokens=LLM_MAX_TOKENS
                )
                return _parse_llm_response(response.choices[0].message.content.strip())

            elif p["type"] == "gemini_rest":
                url = f"https://generativelanguage.googleapis.com/v1/models/{p['model']}:generateContent?key={p['key']}"
                payload = {"contents": [{"parts": [{"text": f"{system_prompt}\n\n{prompt}"}]}]}
                res = requests.post(url, json=payload, timeout=60)
                if res.status_code == 200:
                    raw_text = res.json()['candidates'][0]['content']['parts'][0]['text']
                    return _parse_llm_response(raw_text)
                else:
                    raise Exception(f"Error Gemini REST: {res.status_code}")

        except Exception as e:
            msg = str(e).lower()
            if "429" in msg or "rate_limit" in msg:
                st.warning(f"⚠️ Límite de {p['name']} alcanzado. Cambiando de motor...")
            else:
                # Ocultar errores técnicos menores para no asustar al usuario
                pass
            continue

    raise Exception("Ningún motor de IA pudo completar la solicitud. Verifica tus API Keys.")

def analyze_contract(contract_text: str) -> dict:
    """Punto de entrada principal para análisis de contratos."""
    from asistente_core.prompts import SYSTEM_PROMPT, ANALYSIS_PROMPT
    
    max_chars = 40_000 # Cerebras y Gemini soportan mucho más
    text = contract_text[:max_chars] if len(contract_text) > max_chars else contract_text
    prompt = ANALYSIS_PROMPT.replace("{{CONTRACT_TEXT}}", text)

    return get_ai_response(prompt, SYSTEM_PROMPT, is_json=True)

def compare_contracts(contract1_text: str, contract2_text: str) -> dict:
    """Punto de entrada para comparación de contratos."""
    from asistente_core.prompts import SYSTEM_PROMPT, COMPARISON_PROMPT
    
    max_chars = 15_000 
    c1 = contract1_text[:max_chars] if len(contract1_text) > max_chars else contract1_text
    c2 = contract2_text[:max_chars] if len(contract2_text) > max_chars else contract2_text
    prompt = COMPARISON_PROMPT.replace("{contract_1}", c1).replace("{contract_2}", c2)

    return get_ai_response(prompt, SYSTEM_PROMPT, is_json=True)

def _parse_llm_response(raw_text: str) -> dict:
    """Parsea la respuesta para asegurar un dict válido, eliminando markdown si existe."""
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
            "respuesta_cruda": raw_text[:1000],
            "semaforo": "ALTO",
        }
