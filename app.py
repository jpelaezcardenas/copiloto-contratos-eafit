"""Main application: Copiloto Jurídico EAFIT con diseño Premium Apilex.ai."""

import streamlit as st
import os
from ui.styles import apply_custom_styles
from ui.components import render_dashboard, render_sidebar, show_loading_animation
from core.pdf_extractor import extract_text_from_pdf
from core.llm_analyzer import analyze_contract
from core.risk_detector import process_analysis_results

# 1. Configuración de página
st.set_page_config(
    page_title="Copiloto Jurídico EAFIT | AI Legal Assistant",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Aplicar estilos personalizados (Nueva identidad visual)
apply_custom_styles()

def main():
    # ── HERO SECTION ─────────────────────────────────────
    st.markdown('<div class="hero-container">', unsafe_allow_html=True)
    st.markdown('<h1 class="main-title">AI Legal Assistant</h1>', unsafe_allow_html=True)
    st.markdown(
        '<p class="subtitle">Análisis avanzado de contratos, revisión de documentos legales e investigación normativa en segundos. Optimiza tu gestión jurídica con el estándar de excelencia de EAFIT.</p>',
        unsafe_allow_html=True
    )
    
    # ── ÁREA DE CARGA DE DOCUMENTOS ───────────────────────
    uploaded_file = st.file_uploader(
        "Sube tu contrato (PDF)", 
        type=["pdf"], 
        help="Los archivos se procesan de forma privada y no se almacenan permanentemente."
    )
    
    # Renderizar Sidebar con beneficios (Estilo Apilex)
    render_sidebar()

    if uploaded_file:
        if st.button("🚀 Iniciar Análisis de Documento"):
            with show_loading_animation():
                try:
                    # 1. Extracción
                    text = extract_text_from_pdf(uploaded_file)
                    
                    if not text.strip():
                        st.error("No se pudo extraer texto del archivo. ¿Es un PDF escaneado sin OCR?")
                        return

                    # 2. Análisis LLM (DeepSeek via Groq)
                    analysis_raw = analyze_contract(text)
                    
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
        # Mostrar beneficios si no hay análisis
        st.markdown("""
        <div style="display: flex; justify-content: space-around; gap: 20px; margin-top: 4rem; text-align: left;">
            <div class="risk-card animated-card">
                <h3 style="color: var(--primary);">Context-Aware</h3>
                <p style="color: var(--text-muted);">Respuestas personalizadas basadas en el contexto específico de cada cláusula.</p>
            </div>
            <div class="risk-card animated-card">
                <h3 style="color: var(--primary);">Source-Cited</h3>
                <p style="color: var(--text-muted);">Contenido transparente con referencias legales y normativa colombiana.</p>
            </div>
            <div class="risk-card animated-card">
                <h3 style="color: var(--primary);">Legal Language</h3>
                <p style="color: var(--text-muted);">Tono profesional alineado con la terminología de la Secretaría General.</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    if "analysis_complete" not in st.session_state:
        st.session_state.analysis_complete = False
    main()
