"""Configuración centralizada del asistente de contratos."""

import os
from dotenv import load_dotenv

load_dotenv()

# ── API Keys ──────────────────────────────────────────────
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "")
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")

# ── LLM Settings ─────────────────────────────────────────
LLM_MODEL = "llama-3.3-70b-versatile"  # Modelo top en Groq (70 mil millones de parámetros)
LLM_TEMPERATURE = 0.1 # Muy bajo para evitar alucinaciones legales
LLM_MAX_TOKENS = 8192
GROQ_BASE_URL = "https://api.groq.com/openai/v1"

# ── App Settings ─────────────────────────────────────────
APP_TITLE = "⚖️ Copiloto Jurídico EAFIT"
APP_SUBTITLE = "Asistente Inteligente para Análisis de Contratos"
MAX_FILE_SIZE_MB = 50
SUPPORTED_FILE_TYPES = ["pdf"]

# ── Risk Categories ──────────────────────────────────────
RISK_CATEGORIES = {
    "ambiguedad": {
        "label": "Ambigüedad",
        "icon": "🟡",
        "description": "Lenguaje que permite múltiples interpretaciones",
        "referencia": "Artículo 1624 Código Civil",
    },
    "falta_penalidades": {
        "label": "Falta de Penalidades",
        "icon": "🔴",
        "description": "Ausencia de multa por mora o incumplimiento",
        "referencia": "Artículo 1592 Código Civil",
    },
    "clausulas_abusivas": {
        "label": "Cláusulas Abusivas",
        "icon": "🔴",
        "description": "Desequilibrio injustificado para una de las partes",
        "referencia": "Artículo 42 Ley 1480 de 2011",
    },
    "ruptura_equilibrio": {
        "label": "Ruptura de Equilibrio",
        "icon": "🟠",
        "description": "Terminación unilateral sin indemnización justa",
        "referencia": "Sentencias del Consejo de Estado",
    },
    "vigencia_inconsistente": {
        "label": "Vigencia Inconsistente",
        "icon": "🟡",
        "description": "Fechas contradictorias o renovación automática sin preaviso",
        "referencia": "Ley 1480 de 2011",
    },
    "terminacion_deficiente": {
        "label": "Terminación Deficiente",
        "icon": "🟠",
        "description": "Falta de causales claras de terminación o procedimientos de salida",
        "referencia": "Código Civil / Código de Comercio",
    },
}
