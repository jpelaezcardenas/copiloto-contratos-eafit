import streamlit as st
import os
from dotenv import load_dotenv

# 1. Cargar .env por si acaso se corre local (aunque el usuario prioriza Cloud)
load_dotenv()

# 2. Inyección de Secretos para Streamlit Cloud
# Esto resuelve el problema de tiempo de inicialización sugerido por el usuario
def initialize_env_secrets():
    try:
        if "GROQ_API_KEY" in st.secrets:
            os.environ["GROQ_API_KEY"] = st.secrets["GROQ_API_KEY"]
            # print("DEBUG: GROQ_API_KEY injected into os.environ from st.secrets")
    except:
        pass

initialize_env_secrets()

# 3. Helpers para obtener secretos
def get_secret(key, default=""):
    """Prioriza st.secrets (Cloud) sobre os.getenv (Local)."""
    try:
        # En Streamlit Cloud, st.secrets es un dict-like
        return st.secrets.get(key, os.getenv(key, default))
    except:
        return os.getenv(key, default)

# 4. Configuración Global
GEMINI_API_KEY = get_secret("GEMINI_API_KEY")
DEEPSEEK_API_KEY = get_secret("DEEPSEEK_API_KEY")
GROQ_API_KEY = get_secret("GROQ_API_KEY")

# URL base para Groq (endpoint compatible con OpenAI si se usa OpenAI SDK, 
# pero el usuario pidió Groq SDK nativo)
GROQ_BASE_URL = "https://api.groq.com/openai/v1"

# Modelo por defecto (según prompt original)
LLM_MODEL = "llama-3.3-70b-versatile"
LLM_TEMPERATURE = 0.1
LLM_MAX_TOKENS = 4096

# Configuración de categorías de riesgo (Taxonomía EAFIT)
RISK_CATEGORIES = {
    "AMBIGUEDAD": "Cláusulas imprecisas o confusas.",
    "PENALIDADES": "Sanciones desproporcionadas o unilaterales.",
    "VALIDEZ": "Incumplimiento de normativa colombiana (CST, CC, etc.).",
    "TERMINACION": "Condiciones de salida asimétricas.",
    "PROPIEDAD_INTELECTUAL": "Riesgos en la titularidad de derechos.",
    "JURISDICCION": "Conflictos de leyes o fueros extranjeros."
}
