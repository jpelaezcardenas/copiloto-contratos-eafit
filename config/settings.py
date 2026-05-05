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

# Configuración de categorías de riesgo (Taxonomía EAFIT — 10 categorías)
RISK_CATEGORIES = {
    "AMBIGUEDAD_Y_PI": "Cláusulas imprecisas, propiedad intelectual y confidencialidad.",
    "CLAUSULAS_ECONOMICAS": "Penalidades asimétricas, reajustes y recargos excesivos.",
    "CLAUSULAS_ABUSIVAS": "Limitaciones extremas de responsabilidad, renuncias encubiertas.",
    "JURISDICCION": "Conflictos de leyes, fueros desfavorables, costos judiciales asimétricos.",
    "RUPTURA_EQUILIBRIO_SLAS": "Modificaciones unilaterales de alcance, SLAs débiles.",
    "VIGENCIA_TERMINACION": "Prórrogas agresivas, terminación asimétrica, lock-in.",
    "OBLIGACIONES_DESPROPORCIONADAS": "Compromisos excesivos sin límites claros.",
    "LIMITACIONES_DERECHOS": "Renuncia a remedios legales o garantías implícitas.",
    "MODIFICACIONES_UNILATERALES": "Cambio de condiciones sin consentimiento mutuo.",
    "GARANTIAS_ASIMETRICAS": "Desequilibrios en declaraciones y garantías de las partes.",
}
