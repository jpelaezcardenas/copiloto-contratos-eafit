"""Integración con LLM (Groq) para análisis de contratos."""

import json
import re
from openai import OpenAI
from config.settings import GROQ_API_KEY, GROQ_BASE_URL, LLM_MODEL, LLM_TEMPERATURE, LLM_MAX_TOKENS
from asistente_core.prompts import SYSTEM_PROMPT, ANALYSIS_PROMPT


def get_client():
    """Crea el cliente de Groq (estilo OpenAI)."""
    if not GROQ_API_KEY:
        raise ValueError(
            "❌ GROQ_API_KEY no configurada. "
            "Obtén una en console.groq.com"
        )
    return OpenAI(api_key=GROQ_API_KEY, base_url=GROQ_BASE_URL)


def analyze_contract(contract_text: str) -> dict:
    """Analiza un contrato usando Groq y devuelve el análisis estructurado."""
    client = get_client()

    # Truncar texto si es muy largo (Groq tiene límites de tokens según el modelo)
    max_chars = 30_000 # Llama 3 en Groq tiene límites de TPM
    if len(contract_text) > max_chars:
        contract_text = contract_text[:max_chars] + "\n\n[... DOCUMENTO TRUNCADO ...]"

    # Usar replace en lugar de format para evitar errores con llaves
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
        raise Exception(f"Error de comunicación con Groq: {str(e)}")


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
