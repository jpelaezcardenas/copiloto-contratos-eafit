"""Sistema de diseño premium inspirado en Apilex.ai para el asistente legal."""

import streamlit as st
import base64
import os

def apply_custom_styles():
    """Inyecta el CSS personalizado para un look premium y moderno."""
    # Intentar cargar imagen local como base64 para evitar errores de red
    bg_img_base64 = ""
    try:
        # Calcular ruta absoluta relativa a la raíz del proyecto
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        bg_path = os.path.join(base_dir, "eafit-medellin.webp")
        with open(bg_path, "rb") as image_file:
            bg_img_base64 = base64.b64encode(image_file.read()).decode()
    except Exception:
        pass

    # Usar comillas triples simples para evitar que Python intente parsear {} como variables f-string
    css_content = """
        <style>
        /* Importar tipografía moderna */
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&family=Inter:wght@300;400;500;600&display=swap');

        :root {
            --primary: #003399; /* Azul EAFIT */
            --primary-glow: rgba(0, 51, 153, 0.3);
            --bg-dark: #000000;
            --card-bg: rgba(255, 255, 255, 0.03);
            --text-main: #FFFFFF;
            --text-muted: #A0A0A0;
            --border: rgba(255, 255, 255, 0.08);
            --accent-blue: #003399;
            --accent-yellow: #FFCC00;
            --accent-green: #10B981;
            --accent-red: #EF4444;
        }

        /* Reset general con fondo de imagen (Base64) */
        .stApp, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
            background-image: linear-gradient(to bottom, rgba(0, 10, 30, 0.7), rgba(0, 5, 15, 0.95)), url("data:image/webp;base64,__BG_IMG_BASE64__") !important;
            background-size: cover !important;
            background-position: center !important;
            background-attachment: fixed !important;
            background-color: #000000 !important;
            color: #FFFFFF !important;
        }

        /* Forzar modo oscuro en widgets de Streamlit */
        [data-testid="stSidebar"] {
            background-color: rgba(0, 0, 0, 0.8) !important;
            backdrop-filter: blur(20px);
            border-right: 1px solid var(--border);
        }

        .main, .block-container {
            background: transparent !important;
            padding-top: 2rem !important;
            padding-bottom: 1rem !important;
        }

        h1, h2, h3, .main-title {
            font-family: 'Outfit', sans-serif !important;
            font-weight: 700 !important;
            letter-spacing: -0.02em;
            color: #FFFFFF !important;
        }

        /* Hero Section Premium con Glassmorphism */
        .hero-container {
            padding: 2.5rem;
            text-align: center;
            background: linear-gradient(135deg, rgba(0, 51, 153, 0.15) 0%, rgba(255, 255, 255, 0.02) 100%);
            border-radius: 20px;
            border: 1px solid rgba(255, 255, 255, 0.08);
            box-shadow: 0 15px 40px rgba(0, 0, 0, 0.6), inset 0 1px 1px rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(15px);
            -webkit-backdrop-filter: blur(15px);
            margin-bottom: 2rem;
        }

        .main-title {
            font-size: 3.5rem !important; 
            background: linear-gradient(135deg, #FFFFFF 0%, #FFCC00 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 1rem !important;
            filter: drop-shadow(0px 4px 10px rgba(0, 0, 0, 0.5));
        }

        .subtitle {
            font-size: 1.2rem;
            color: rgba(255, 255, 255, 0.8);
            max-width: 850px;
            margin: 0 auto;
            line-height: 1.6;
            text-shadow: 0 2px 4px rgba(0, 0, 0, 0.5);
        }

        /* Tabs personalizadas para modo oscuro */
        .stTabs [data-baseweb="tab-list"] {
            gap: 10px;
            background-color: transparent;
        }

        .stTabs [data-baseweb="tab"] {
            background-color: rgba(255, 255, 255, 0.05) !important;
            border-radius: 8px 8px 0 0 !important;
            color: #A0A0A0 !important;
            padding: 10px 20px !important;
            border: 1px solid transparent !important;
        }

        .stTabs [aria-selected="true"] {
            background-color: rgba(0, 51, 153, 0.3) !important;
            color: #FFCC00 !important;
            border-top: 2px solid #FFCC00 !important;
        }

        /* Botones estilo EAFIT Premium */
        .stButton > button {
            background: linear-gradient(135deg, var(--primary) 0%, #002266 100%) !important;
            color: white !important;
            border-radius: 10px !important;
            padding: 0.8rem 2.5rem !important;
            font-weight: 600 !important;
            border: 1px solid rgba(255, 204, 0, 0.3) !important;
            box-shadow: 0 4px 15px rgba(0, 51, 153, 0.3) !important;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
            text-transform: uppercase;
            letter-spacing: 1px;
        }

        .stButton > button:hover {
            background: linear-gradient(135deg, #FFCC00 0%, #E6B800 100%) !important;
            color: #000000 !important;
            border: 1px solid #FFFFFF !important;
            box-shadow: 0 6px 25px rgba(255, 204, 0, 0.4) !important;
            transform: translateY(-2px);
        }

        /* Drag and Drop Zone Premium */
        div[data-testid="stFileUploaderDropzone"] {
            background: rgba(255, 255, 255, 0.02) !important;
            border: 2px dashed rgba(255, 204, 0, 0.3) !important;
            border-radius: 16px;
            transition: all 0.3s ease;
        }

        div[data-testid="stFileUploaderDropzone"]:hover {
            border-color: var(--accent-yellow) !important;
            background: rgba(255, 204, 0, 0.05) !important;
        }

        /* Tarjetas de Riesgo */
        .risk-card {
            background: rgba(255, 255, 255, 0.03);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 16px;
            padding: 2rem;
            margin-bottom: 1.5rem;
            backdrop-filter: blur(5px);
            transition: all 0.3s ease;
        }

        .risk-card:hover {
            border-color: rgba(255, 204, 0, 0.4);
            background: rgba(255, 255, 255, 0.05);
            transform: translateY(-2px);
        }

        /* Semáforo Global */
        .semaforo-banner {
            padding: 2.5rem;
            border-radius: 20px;
            text-align: center;
            margin-bottom: 2.5rem;
            background: rgba(0, 0, 0, 0.4);
            border: 1px solid rgba(255, 255, 255, 0.1);
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
        }

        .semaforo-glow-ALTO { border-top: 4px solid #EF4444; }
        .semaforo-glow-MEDIO, .semaforo-glow-MODERADO { border-top: 4px solid #F59E0B; }
        .semaforo-glow-BAJO { border-top: 4px solid #10B981; }

        .text-ALTO { color: #EF4444 !important; text-shadow: 0 0 15px rgba(239, 68, 68, 0.3); }
        .text-MEDIO, .text-MODERADO { color: #F59E0B !important; text-shadow: 0 0 15px rgba(245, 158, 11, 0.3); }
        .text-BAJO { color: #10B981 !important; text-shadow: 0 0 15px rgba(16, 185, 129, 0.3); }

        /* Inputs y Text Areas */
        .stTextArea textarea {
            background-color: rgba(0, 0, 0, 0.3) !important;
            color: white !important;
            border: 1px solid var(--border) !important;
            border-radius: 10px !important;
        }

        /* Footer minimalista */
        .eafit-footer {
            text-align: center;
            color: #666;
            font-size: 0.8rem;
            padding: 2rem 0;
            border-top: 1px solid rgba(255, 255, 255, 0.05);
            margin-top: 4rem;
        }

        </style>
        """
    
    # Inyectar la variable de forma segura
    css_content = css_content.replace("__BG_IMG_BASE64__", bg_img_base64)
    st.markdown(css_content, unsafe_allow_html=True)
