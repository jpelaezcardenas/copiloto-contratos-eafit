import os
import sys

# ── FORZAR DIRECTORIO RAÍZ (PARA DESPLIEGUE CLOUD) ──────────────────
base_path = os.path.dirname(os.path.abspath(__file__))
if base_path not in sys.path:
    sys.path.insert(0, base_path)

import streamlit as st
import json

# ── CONFIGURACIÓN DE PÁGINA (DEBE SER EL PRIMER COMANDO ST) ──────────────
st.set_page_config(
    page_title="Asistente jurídico para análisis contractual | EAFIT",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# IMPORTACIONES LOCALES (Deben coincidir con los nombres de las carpetas)
from asistente_ui.styles import apply_custom_styles
from asistente_ui.components import render_dashboard, render_sidebar, show_loading_animation, render_footer, render_comparison_dashboard

# ── LOGICA DE NEGOCIO ──────────────────────────────────────────
from asistente_core.pdf_extractor import extract_text_from_pdf, sanitize_extracted_text
from asistente_core.llm_analyzer import analyze_contract, compare_contracts
from asistente_core.risk_detector import process_analysis_results

# 2. Aplicar estilos personalizados
apply_custom_styles()

def check_password():
    """Devuelve `True` si el usuario ingresa la contraseña correcta."""
    # Si no hay contraseña configurada en secrets, permitir acceso (modo público/desarrollo)
    if "APP_PASSWORD" not in st.secrets:
        return True

    def password_entered():
        """Verifica si la contraseña ingresada es correcta."""
        if st.session_state["pwd_input"] == st.secrets["APP_PASSWORD"]:
            st.session_state["password_correct"] = True
            del st.session_state["pwd_input"]  # Eliminar por seguridad
        else:
            st.session_state["password_correct"] = False

    if st.session_state.get("password_correct", False):
        return True

    # Interfaz de login centralizada
    st.markdown("<div style='height: 15vh;'></div>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<div class='hero-container' style='text-align: center; padding: 2rem;'>", unsafe_allow_html=True)
        st.markdown("<h2>🔒 Acceso Restringido</h2>", unsafe_allow_html=True)
        st.markdown("<p>Por favor, ingresa la contraseña corporativa para usar el Asistente jurídico para análisis contractual.</p>", unsafe_allow_html=True)
        st.text_input(
            "Contraseña", type="password", on_change=password_entered, key="pwd_input"
        )
        if "password_correct" in st.session_state and not st.session_state["password_correct"]:
            st.error("😕 Contraseña incorrecta. Inténtalo de nuevo.")
        st.markdown("</div>", unsafe_allow_html=True)
    return False

if not check_password():
    st.stop()

def main():
    # ── ESPACIO SUPERIOR PARA DISTRIBUCIÓN VERTICAL ───
    st.markdown("<div style='height: 12vh;'></div>", unsafe_allow_html=True)

    # ── ÁREA PRINCIPAL (HERO + CARGA DE DOCUMENTOS) ──────────────
    col_u1, col_u2, col_u3 = st.columns([1, 6, 1])
    with col_u2:
        # ── HERO SECTION ─────────────────────────────────────
        st.markdown("""
            <div class="hero-container" style="text-align: center; display: flex; flex-direction: column; align-items: center;">
                <h1 class="main-title">Asistente jurídico para análisis contractual</h1>
                <p class="subtitle">Nuestra inteligencia artificial comprende los contratos más complejos y entrega análisis integrales o comparativos en segundos. Acelera la revisión documental y optimiza los procesos legales de la secretaria general de la Universidad EAFIT</p>
            </div>
            <div style="height: 1rem;"></div>
        """, unsafe_allow_html=True)
        
        # ── TABS: PDF, Texto, Comparar, Evaluar ──────────────────────
        tab_pdf, tab_text, tab_compare = st.tabs(["📄 Cargar PDF", "📋 Pegar Texto", "⚖️ Comparar Contratos"])

        with tab_pdf:
            uploaded_file = st.file_uploader(
                "Arrastra y suelta el contrato (PDF) para iniciar el análisis", 
                type=["pdf"], 
                key="file_pdf",
                help="Los archivos se procesan de forma privada y no se almacenan permanentemente."
            )

        with tab_text:
            text_default = st.session_state.get("pasted_text_demo", "")
            pasted_text = st.text_area(
                "Pega aquí el texto del contrato",
                height=300,
                key="text_single",
                value=text_default,
                placeholder="Copia y pega el contenido del contrato directamente aquí...",
                help="Si no tienes el PDF, puedes pegar el texto del contrato manualmente."
            )
            
            # Limpiar el texto cargado de demo si el usuario ya analizó o cambió algo
            if text_default and st.button("Limpiar Ejemplo", key="clear_demo"):
                st.session_state.pasted_text_demo = ""
                st.rerun()

        with tab_compare:
            st.markdown("<p style='color: white; font-weight: 500;'>Carga dos documentos para detectar discrepancias y cambios clave.</p>", unsafe_allow_html=True)
            ccol1, ccol2 = st.columns(2)
            with ccol1:
                st.markdown("**Versión 1 (Documento Base)**")
                comp_file1 = st.file_uploader("PDF 1", type=["pdf"], key="comp_file1")
                comp_text1 = st.text_area("O pega el texto 1", height=150, key="comp_text1")
            with ccol2:
                st.markdown("**Versión 2 (Documento Modificado)**")
                comp_file2 = st.file_uploader("PDF 2", type=["pdf"], key="comp_file2")
                comp_text2 = st.text_area("O pega el texto 2", height=150, key="comp_text2")


    # Renderizar Sidebar (incluye historial)
    render_sidebar()

    # Variables de control
    has_pdf = uploaded_file is not None if 'uploaded_file' in locals() else False
    has_text = bool(pasted_text.strip()) if 'pasted_text' in locals() and pasted_text else False
    
    # Evaluar si se puede comparar
    has_comp1 = (comp_file1 is not None) or bool(comp_text1.strip())
    has_comp2 = (comp_file2 is not None) or bool(comp_text2.strip())
    can_compare = has_comp1 and has_comp2

    with col_u2:
        col_b1, col_b2, col_b3 = st.columns([1, 1, 1])
        with col_b2:
            if has_pdf or has_text:
                if st.button("🔍 INICIAR ANÁLISIS JURÍDICO", width="stretch", type="primary"):
                    with show_loading_animation():
                        try:
                            # 1. Extracción según la fuente
                            if has_pdf:
                                text = extract_text_from_pdf(uploaded_file)
                                full_text = str(text) if isinstance(text, dict) else str(text)
                                doc_name = uploaded_file.name
                            else:
                                full_text = sanitize_extracted_text(pasted_text)
                                doc_name = "Texto Pegado"
                                
                            if not full_text.strip():
                                st.error("No se pudo extraer texto. Verifica el documento.")
                            else:
                                # 2. Análisis LLM
                                analysis_raw = analyze_contract(full_text)
                                # 3. Procesamiento de riesgos
                                final_data = process_analysis_results(analysis_raw)
                                
                                # Guardar resultados en el estado
                                st.session_state.analysis_complete = True
                                st.session_state.comparison_complete = False
                                st.session_state.analysis_data = final_data
                                
                                # Guardar en el historial
                                st.session_state.history.append({
                                    "name": f"{doc_name} ({final_data.get('semaforo', 'OK')})",
                                    "data": final_data
                                })
                                st.rerun() # Recargar la página para limpiar boton
                        except Exception as e:
                            st.error(f"❌ Error al analizar el contrato: {str(e)}")

            elif can_compare:
                if st.button("⚖️ INICIAR COMPARACIÓN", width="stretch", type="primary"):
                    with show_loading_animation():
                        try:
                            # Extraer TXT 1
                            if comp_file1 is not None:
                                t1 = extract_text_from_pdf(comp_file1)
                                n1 = comp_file1.name
                            else:
                                t1 = sanitize_extracted_text(comp_text1)
                                n1 = "Texto 1"
                                
                            # Extraer TXT 2
                            if comp_file2 is not None:
                                t2 = extract_text_from_pdf(comp_file2)
                                n2 = comp_file2.name
                            else:
                                t2 = sanitize_extracted_text(comp_text2)
                                n2 = "Texto 2"
                                
                            comp_raw = compare_contracts(str(t1), str(t2))
                            
                            st.session_state.comparison_complete = True
                            st.session_state.analysis_complete = False
                            st.session_state.comp_data = comp_raw
                            st.session_state.comp_names = (n1, n2)
                            st.rerun()
                        except Exception as e:
                            st.error(f"❌ Error al comparar los contratos: {str(e)}")

    # 4. Mostrar Dashboard (Individual o Comparativo)
    if st.session_state.get("analysis_complete") and not st.session_state.get("comparison_complete"):
        render_dashboard(st.session_state.analysis_data)
    elif st.session_state.get("comparison_complete"):
        n1, n2 = st.session_state.get("comp_names", ("Doc 1", "Doc 2"))
        render_comparison_dashboard(st.session_state.comp_data, n1, n2)
    else:
        st.markdown("<div style='height: 2vh;'></div>", unsafe_allow_html=True)

    # 5. FOOTER INSTITUCIONAL
    render_footer()

if __name__ == "__main__":
    if "analysis_complete" not in st.session_state:
        st.session_state.analysis_complete = False
    if "comparison_complete" not in st.session_state:
        st.session_state.comparison_complete = False
    if "history" not in st.session_state:
        st.session_state.history = []
    main()
