"""Sistema de diseño premium inspirado en Apilex.ai para el asistente legal."""

import streamlit as st
import base64
import os

def apply_custom_styles():
    """Inyecta el CSS personalizado para un look premium y moderno."""
    # Intentar cargar imagen local como base64 para evitar errores de red
    bg_img_base64 = ""
    try:
        with open("eafit-medellin.webp", "rb") as image_file:
            bg_img_base64 = base64.b64encode(image_file.read()).decode()
    except:
        pass

    css_content = """
        <style>
        /* Importar tipografía moderna */
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&family=Inter:wght@300;400;500;600&display=swap');

        :root {
            --primary: #003399; /* Azul EAFIT */
            --primary-glow: rgba(0, 51, 153, 0.3);
            --bg-dark: #000000;
            --card-bg: rgba(255, 255, 255, 0.05);
            --text-main: #FFFFFF;
            --text-muted: #A0A0A0;
            --border: rgba(255, 255, 255, 0.1);
            --accent-blue: #003399;
            --accent-yellow: #FFCC00;
            --accent-green: #10B981;
            --accent-red: #EF4444;
        }

        /* Reset general con fondo de imagen (Base64) */
        .stApp, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
            background-image: linear-gradient(rgba(0, 0, 0, 0.82), rgba(0, 0, 0, 0.96)), url("data:image/webp;base64,__BG_IMG_BASE64__") !important;
            background-size: cover !important;
            background-position: center !important;
            background-attachment: fixed !important;
            background-color: black !important;
        }

        /* Limpiar fondos de contenedores internos y reducir padding top/bottom */
        .main, .block-container {
            background: transparent !important;
            padding-top: 2rem !important;
            padding-bottom: 1rem !important;
        }

        h1, h2, h3, .main-title {
            font-family: 'Outfit', sans-serif !important;
            font-weight: 700 !important;
            letter-spacing: -0.02em;
        }

        /* Hero Section - Reducir el padding para evitar scroll */
        .hero-container {
            padding: 1rem 1rem 1rem 1rem;
            text-align: center;
            background: linear-gradient(180deg, rgba(0, 51, 153, 0.15) 0%, transparent 100%);
        }

        .main-title {
            font-size: 3rem !important; /* Un poco más pequeño para ahorrar espacio */
            background: linear-gradient(135deg, #FFFFFF 0%, #FFCC00 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 0.5rem !important;
        }

        .subtitle {
            font-size: 1.1rem;
            color: var(--text-muted);
            max-width: 800px;
            margin: 0 auto 1.5rem auto;
            line-height: 1.5;
            text-align: center;
        }

        /* Botones estilo EAFIT */
        .stButton > button {
            background-color: var(--primary) !important;
            color: white !important;
            border-radius: 4px !important; /* Bordes más rectos/institucionales */
            padding: 0.8rem 2.8rem !important;
            font-weight: 600 !important;
            border: 1px solid var(--accent-yellow) !important;
            transition: all 0.3s ease !important;
            text-transform: uppercase;
            letter-spacing: 1px;
        }

        .stButton > button:hover {
            background-color: var(--accent-yellow) !important;
            color: black !important;
            transform: translateY(-2px);
        }

        /* Drag and Drop Zone Ampliado */
        div[data-testid="stFileUploaderDropzone"] {
            min-height: 400px !important;
            display: flex;
            align-items: center;
            justify-content: center;
            background-color: rgba(0, 51, 153, 0.1) !important;
            border: 2px dashed var(--accent-yellow) !important;
            border-radius: 12px;
        }

        /* Footer Institucional - Más compacto */
        .eafit-footer {
            background-color: #000000;
            color: white;
            padding: 2rem 2rem 1rem 2rem;
            border-top: 1px solid #333;
            margin-top: 2rem;
            font-family: 'Inter', sans-serif;
        }

        .footer-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 2rem;
            max-width: 1200px;
            margin: 0 auto;
        }

        .footer-col h4 {
            color: white;
            font-size: 1.1rem;
            margin-bottom: 1.5rem;
            font-weight: 700;
            border-bottom: 2px solid var(--accent-yellow);
            display: inline-block;
            padding-bottom: 5px;
        }

        .footer-col p {
            color: #ccc;
            font-size: 0.9rem;
            line-height: 1.5;
            margin-bottom: 0.5rem;
        }

        .footer-social {
            display: flex;
            gap: 15px;
            margin-top: 2rem;
            justify-content: center;
            border-top: 1px solid #222;
            padding-top: 2rem;
        }

        /* Tarjetas de Riesgo */
        .risk-card {
            background: var(--card-bg);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 2rem;
            margin-bottom: 1.5rem;
            transition: transform 0.3s ease;
        }

        .risk-card:hover {
            transform: scale(1.01);
            border-color: var(--accent-yellow);
        }

        /* Semáforo Global */
        .semaforo-banner {
            padding: 3rem;
            border-radius: 16px;
            text-align: center;
            margin-bottom: 3rem;
            background: rgba(255, 255, 255, 0.03);
            border: 1px solid rgba(255,255,255,0.1);
        }

        .semaforo-glow-ALTO { border-left: 8px solid #EF4444; background: linear-gradient(90deg, rgba(239, 68, 68, 0.1) 0%, transparent 100%); }
        .semaforo-glow-MEDIO { border-left: 8px solid #F59E0B; background: linear-gradient(90deg, rgba(245, 158, 11, 0.1) 0%, transparent 100%); }
        .semaforo-glow-BAJO { border-left: 8px solid #10B981; background: linear-gradient(90deg, rgba(16, 185, 129, 0.1) 0%, transparent 100%); }

        .text-ALTO { color: #EF4444 !important; }
        .text-MEDIO { color: #F59E0B !important; }
        .text-BAJO { color: #10B981 !important; }

        /* Sidebar Logo */
        .sidebar-logo {
            width: 100%;
            margin-bottom: 2rem;
            padding: 1rem;
        }

        </style>
        """
    
    # Inyectar la variable de forma segura
    css_content = css_content.replace("__BG_IMG_BASE64__", bg_img_base64)
    st.markdown(css_content, unsafe_allow_html=True)
