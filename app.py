"""Main application: Copiloto Jurídico EAFIT con diseño Premium Apilex.ai."""

import streamlit as st
import os
import sys

# Agregar el directorio actual al path para resolver módulos en Streamlit Cloud y Local
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

# 1. Configuración de página
st.set_page_config(
    page_title="Copiloto Jurídico EAFIT | AI Legal Assistant",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

from asistente_ui.styles import apply_custom_styles
from asistente_ui.components import render_dashboard, render_sidebar, show_loading_animation, render_footer

# ── LOGICA DE NEGOCIO (CON NOMBRES ÚNICOS) ──────────────────────
from asistente_core.pdf_extractor import extract_text_from_pdf
from asistente_core.llm_analyzer import analyze_contract
from asistente_core.risk_detector import process_analysis_results

# 2. Aplicar estilos personalizados (Nueva identidad visual)
apply_custom_styles()

def main():
    # ── BANNER INSTITUCIONAL ─────────────────────────────
    st.markdown('<div style="background-color: #000; padding: 1rem; border-bottom: 1px solid #333; margin-bottom: 2rem; display: flex; align-items: center; justify-content: center;">', unsafe_allow_html=True)
    st.markdown('<div style="color: #666; font-size: 0.75rem; font-weight: 700; letter-spacing: 2px;">SECRETARÍA GENERAL | ASISTENTE LEGAL AI</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # ── HERO SECTION ─────────────────────────────────────
    st.markdown('<div class="hero-container">', unsafe_allow_html=True)
    st.markdown('<h1 class="main-title">EAFIT Legal Copilot</h1>', unsafe_allow_html=True)
    st.markdown(
        '<p class="subtitle">Nuestra inteligencia artificial comprende los contratos más complejos y entrega análisis integrales en segundos. Acelera la revisión documental y optimiza los procesos legales de la Universidad.</p>',
        unsafe_allow_html=True
    )
    
    # ── ÁREA DE CARGA DE DOCUMENTOS ───────────────────────
    col_u1, col_u2, col_u3 = st.columns([1, 2, 1])
    with col_u2:
        uploaded_file = st.file_uploader(
            "Carga el contrato (PDF) para iniciar el análisis institucional", 
            type=["pdf"], 
            help="Los archivos se procesan de forma privada y no se almacenan permanentemente."
        )
    
    # Renderizar Sidebar
    render_sidebar()

    if uploaded_file:
        col_b1, col_b2, col_b3 = st.columns([1, 1, 1])
        with col_b2:
            if st.button("🔍 INICIAR ANÁLISIS JURÍDICO", use_container_width=True):
                with show_loading_animation():
                    try:
                        # 1. Extracción
                        text = extract_text_from_pdf(uploaded_file)
                        full_text = str(text) if isinstance(text, dict) else str(text)
                        
                        if not full_text.strip():
                            st.error("No se pudo extraer texto del archivo. ¿Es un PDF escaneado sin OCR?")
                            return

                        # 2. Análisis LLM (Llama 3.3 via Groq)
                        analysis_raw = analyze_contract(full_text)
                        
                        # 3. Procesamiento de riesgos
                        final_data = process_analysis_results(analysis_raw)
                        
                        # Guardar resultados en el estado
                        st.session_state.analysis_complete = True
                        st.session_state.analysis_data = final_data
                        
                    except Exception as e:
                        st.error(f"❌ Error al analizar el contrato: {str(e)}")

    # 4. Mostrar Dashboard si el análisis está listo
    if st.session_state.get("analysis_complete"):
        render_dashboard(st.session_state.analysis_data)
    else:
        # Mostrar beneficios si no hay análisis (Cards Estilo EAFIT)
        st.markdown("""
        <div style="display: flex; justify-content: center; gap: 30px; margin-top: 5rem; margin-bottom: 5rem; max-width: 1200px; margin-left: auto; margin-right: auto;">
            <div class="risk-card animated-card" style="flex: 1; text-align: center; border-bottom: 4px solid var(--accent-yellow);">
                <h3 style="color: var(--accent-yellow); font-size: 1.4rem;">Respuestas en Segundos</h3>
                <p style="color: var(--text-muted); font-size: 0.95rem;">Escribe tu pregunta; el asistente produce respuestas claras, precisas y accionables.</p>
            </div>
            <div class="risk-card animated-card" style="flex: 1; text-align: center; border-bottom: 4px solid var(--accent-yellow);">
                <h3 style="color: var(--accent-yellow); font-size: 1.4rem;">Fuentes Citadas</h3>
                <p style="color: var(--text-muted); font-size: 0.95rem;">Contenido transparente con referencias a legislación y jurisprudencia colombiana.</p>
            </div>
            <div class="risk-card animated-card" style="flex: 1; text-align: center; border-bottom: 4px solid var(--accent-yellow);">
                <h3 style="color: var(--accent-yellow); font-size: 1.4rem;">Lenguaje Jurídico</h3>
                <p style="color: var(--text-muted); font-size: 0.95rem;">Tono profesional alineado con los estándares de la Secretaría General.</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # 5. FOOTER INSTITUCIONAL (Siempre visible al final)
    render_footer()

if __name__ == "__main__":
    if "analysis_complete" not in st.session_state:
        st.session_state.analysis_complete = False
    main()
