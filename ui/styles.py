"""Sistema de diseño premium inspirado en Apilex.ai para el asistente legal."""

import streamlit as st

def apply_custom_styles():
    """Inyecta el CSS personalizado para un look premium y moderno."""
    st.markdown(
        """
        <style>
        /* Importar tipografía moderna */
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&family=Inter:wght@300;400;500;600&display=swap');

        :root {
            --primary: #0066FF;
            --primary-glow: rgba(0, 102, 255, 0.3);
            --bg-dark: #0A0D14;
            --card-bg: rgba(255, 255, 255, 0.03);
            --text-main: #FFFFFF;
            --text-muted: #94A3B8;
            --border: rgba(255, 255, 255, 0.1);
            --accent-green: #10B981;
            --accent-yellow: #F59E0B;
            --accent-red: #EF4444;
        }

        /* Reset general */
        .stApp {
            background-color: var(--bg-dark);
            font-family: 'Inter', sans-serif;
            color: var(--text-main);
        }

        h1, h2, h3, .main-title {
            font-family: 'Outfit', sans-serif !important;
            font-weight: 700 !important;
            letter-spacing: -0.02em;
        }

        /* Hero Section */
        .hero-container {
            padding: 4rem 1rem 2rem 1rem;
            text-align: center;
            background: radial-gradient(circle at 50% -20%, var(--primary-glow) 0%, transparent 70%);
        }

        .main-title {
            font-size: 3.5rem !important;
            background: linear-gradient(135deg, #FFFFFF 0%, #94A3B8 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 1rem !important;
        }

        .subtitle {
            font-size: 1.25rem;
            color: var(--text-muted);
            max-width: 700px;
            margin: 0 auto 2.5rem auto;
            line-height: 1.6;
        }

        /* Botones estilo Apilex */
        .stButton > button {
            background-color: var(--primary) !important;
            color: white !important;
            border-radius: 50px !important;
            padding: 0.75rem 2.5rem !important;
            font-weight: 600 !important;
            border: none !important;
            box-shadow: 0 4px 14px 0 var(--primary-glow) !important;
            transition: all 0.25s ease-in-out !important;
            width: auto !important;
        }

        .stButton > button:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 6px 20px 0 var(--primary-glow) !important;
            opacity: 0.9 !important;
        }

        /* Tarjetas de Riesgo (Glassmorphism) */
        .risk-card {
            background: var(--card-bg);
            border: 1px solid var(--border);
            border-radius: 16px;
            padding: 1.5rem;
            margin-bottom: 1rem;
            backdrop-filter: blur(10px);
            transition: border-color 0.3s ease;
        }

        .risk-card:hover {
            border-color: var(--primary);
        }

        .risk-header {
            display: flex;
            align-items: center;
            gap: 12px;
            margin-bottom: 0.8rem;
        }

        .risk-status {
            width: 12px;
            height: 12px;
            border-radius: 50%;
        }

        .status-low { background-color: var(--accent-green); box-shadow: 0 0 10px var(--accent-green); }
        .status-medium { background-color: var(--accent-yellow); box-shadow: 0 0 10px var(--accent-yellow); }
        .status-high { background-color: var(--accent-red); box-shadow: 0 0 10px var(--accent-red); }

        /* Widgets de Sidebar */
        section[data-testid="stSidebar"] {
            background-color: #05070A !important;
            border-right: 1px solid var(--border) !important;
        }

        /* Ocultar elementos de Streamlit predeterminados */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}

        /* Animaciones suaves */
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }

        .animated-card {
            animation: fadeIn 0.5s ease-out forwards;
        }

        </style>
        """,
        unsafe_allow_html=True,
    )
