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
    page_title="Asistente para Análisis de Contratos | EAFIT",
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
    # ── BANNER INSTITUCIONAL ELIMINADO ─────────────────────────────

    # ── ESPACIO SUPERIOR PARA DISTRIBUCIÓN VERTICAL ───
    st.markdown("<div style='height: 12vh;'></div>", unsafe_allow_html=True)

    # ── ÁREA PRINCIPAL (HERO + CARGA DE DOCUMENTOS) ──────────────
    col_u1, col_u2, col_u3 = st.columns([1, 6, 1])
    with col_u2:
        # ── HERO SECTION ─────────────────────────────────────
        st.markdown("""
            <div class="hero-container" style="text-align: center; display: flex; flex-direction: column; align-items: center;">
                <h1 class="main-title">Asistente para Análisis de Contratos</h1>
                <p class="subtitle">Nuestra inteligencia artificial comprende los contratos más complejos y entrega análisis integrales en segundos. Acelera la revisión documental y optimiza los procesos legales de la Universidad.</p>
            </div>
            <div style="height: 1rem;"></div>
        """, unsafe_allow_html=True)
        
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
        # Espacio mínimo solo si no hay resultados ni carga para balancear el footer si sube mucho
        st.markdown("<div style='height: 2vh;'></div>", unsafe_allow_html=True)

    # 5. FOOTER INSTITUCIONAL (Siempre visible al final)
    render_footer()

if __name__ == "__main__":
    if "analysis_complete" not in st.session_state:
        st.session_state.analysis_complete = False
    main()
