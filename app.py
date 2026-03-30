"""
⚖️ Copiloto Jurídico EAFIT
Asistente Inteligente para Análisis de Contratos

Aplicación principal Streamlit.
"""

import streamlit as st
import json
import time

from ui.styles import get_custom_css
from ui.components import (
    render_header,
    render_upload_section,
    render_document_info,
    render_semaforo,
    render_identificacion,
    render_obligaciones,
    render_risks,
    render_resumen_ejecutivo,
    render_disclaimer,
    render_sidebar,
)
from core.pdf_extractor import extract_text_from_pdf, sanitize_extracted_text
from core.llm_analyzer import analyze_contract
from core.risk_detector import get_risk_stats

# ── Page Config ──────────────────────────────────────────
st.set_page_config(
    page_title="Copiloto Jurídico EAFIT",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── CSS ──────────────────────────────────────────────────
st.markdown(get_custom_css(), unsafe_allow_html=True)

# ── Session State ────────────────────────────────────────
if "analysis_result" not in st.session_state:
    st.session_state.analysis_result = None
if "extraction" not in st.session_state:
    st.session_state.extraction = None
if "analysis_history" not in st.session_state:
    st.session_state.analysis_history = []

# ── Sidebar ──────────────────────────────────────────────
render_sidebar()

# ── Main Content ─────────────────────────────────────────
render_header()

# ── Upload Section ───────────────────────────────────────
uploaded_file = render_upload_section()

if uploaded_file is not None:
    pdf_bytes = uploaded_file.read()

    # Extraer texto
    with st.spinner(""):
        st.markdown(
            """
            <div class="analyzing-container">
                <div class="pulse" style="font-size: 2rem;">📄</div>
                <p style="color: #94a3b8; margin-top: 1rem;">Extrayendo texto del documento...</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        extraction = extract_text_from_pdf(pdf_bytes)
        extraction["text"] = sanitize_extracted_text(extraction["text"])
        st.session_state.extraction = extraction

    # Mostrar info del documento
    render_document_info(extraction)

    # Verificar que hay texto
    if not extraction["text"].strip():
        st.error(
            "⚠️ No se pudo extraer texto del PDF. "
            "El documento puede ser una imagen escaneada sin OCR. "
            "Intenta con un PDF que contenga texto seleccionable."
        )
        st.stop()

    # Botón de análisis
    st.markdown("")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        analyze_btn = st.button(
            "🤖 Analizar Contrato con IA",
            use_container_width=True,
        )

    if analyze_btn:
        try:
            # Animación de análisis
            progress_placeholder = st.empty()
            progress_placeholder.markdown(
                """
                <div class="analyzing-container animate-in">
                    <div class="pulse" style="font-size: 3rem;">🤖</div>
                    <p style="color: #a5b4fc; font-size: 1.1rem; margin-top: 1rem; font-weight: 500;">
                        Analizando contrato con inteligencia artificial...
                    </p>
                    <p style="color: #64748b; font-size: 0.85rem;">
                        Detectando riesgos legales • Evaluando cláusulas • Generando informe
                    </p>
                </div>
                """,
                unsafe_allow_html=True,
            )

            start_time = time.time()
            result = analyze_contract(extraction["text"])
            elapsed = time.time() - start_time

            progress_placeholder.empty()

            st.session_state.analysis_result = result

            # Guardar en historial
            st.session_state.analysis_history.append(
                {
                    "filename": uploaded_file.name,
                    "semaforo": result.get("semaforo", "MODERADO"),
                    "total_riesgos": len(result.get("riesgos", [])),
                    "tiempo_analisis": f"{elapsed:.1f}s",
                }
            )

        except ValueError as e:
            st.error(str(e))
            st.info(
                "💡 Necesitas configurar tu API key de Gemini. "
                "Crea un archivo `.env` en la carpeta del proyecto con:\n\n"
                "`GEMINI_API_KEY=tu_api_key_aqui`\n\n"
                "Puedes obtener una gratis en [Google AI Studio](https://aistudio.google.com/)"
            )
            st.stop()
        except Exception as e:
            st.error(f"❌ Error al analizar el contrato: {str(e)}")
            st.stop()

    # ── Mostrar Resultados ───────────────────────────────
    if st.session_state.analysis_result:
        result = st.session_state.analysis_result

        if result.get("error"):
            st.warning(
                f"⚠️ {result.get('mensaje', 'Error en el análisis')}. "
                "Intenta cargar el contrato nuevamente."
            )
            with st.expander("Ver respuesta cruda del modelo"):
                st.code(result.get("respuesta_cruda", ""))
        else:
            st.markdown("---")

            # Tabs de resultados
            tab1, tab2, tab3, tab4, tab5 = st.tabs(
                [
                    "📊 Resumen",
                    "🔍 Identificación",
                    "📋 Obligaciones",
                    "⚠️ Riesgos",
                    "📄 Texto Extraído",
                ]
            )

            with tab1:
                # Semáforo
                render_semaforo(result.get("semaforo", "MODERADO"))

                # Resumen ejecutivo
                render_resumen_ejecutivo(
                    result.get("resumen_ejecutivo", "No disponible.")
                )

                # Métricas rápidas
                riesgos = result.get("riesgos", [])
                stats = get_risk_stats(riesgos)

                # Notas adicionales
                notas = result.get("notas_adicionales", "")
                if notas:
                    st.markdown(
                        f"""
                        <div class="glass-card">
                            <h3>📌 Notas Adicionales</h3>
                            <p style="color: #94a3b8; line-height: 1.7;">{notas}</p>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

            with tab2:
                render_identificacion(result.get("identificacion", {}))

            with tab3:
                render_obligaciones(result.get("obligaciones", {}))

            with tab4:
                st.markdown(
                    '<h2 style="color: #e2e8f0; font-weight: 600;">⚠️ Análisis de Riesgos</h2>',
                    unsafe_allow_html=True,
                )
                render_risks(result.get("riesgos", []))

            with tab5:
                st.markdown(
                    '<h2 style="color: #e2e8f0; font-weight: 600;">📄 Texto Extraído del Contrato</h2>',
                    unsafe_allow_html=True,
                )
                st.text_area(
                    "Texto completo",
                    extraction["text"],
                    height=500,
                    label_visibility="collapsed",
                )

            # Exportar JSON
            st.markdown("")
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                st.download_button(
                    label="📥 Descargar Análisis (JSON)",
                    data=json.dumps(result, ensure_ascii=False, indent=2),
                    file_name=f"analisis_{uploaded_file.name.replace('.pdf', '')}.json",
                    mime="application/json",
                    use_container_width=True,
                )

# ── Historial ────────────────────────────────────────────
if st.session_state.analysis_history:
    st.markdown("---")
    st.markdown(
        '<h2 style="color: #e2e8f0; font-weight: 600;">📜 Historial de Análisis</h2>',
        unsafe_allow_html=True,
    )
    for i, item in enumerate(reversed(st.session_state.analysis_history)):
        semaforo_emoji = {"BAJO": "🟢", "MODERADO": "🟡", "ALTO": "🔴"}.get(
            item["semaforo"], "🟡"
        )
        st.markdown(
            f"""
            <div class="glass-card">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <span style="color: #e2e8f0; font-weight: 500;">
                        {semaforo_emoji} {item['filename']}
                    </span>
                    <span style="color: #64748b; font-size: 0.85rem;">
                        {item['total_riesgos']} riesgos • {item['tiempo_analisis']}
                    </span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

# ── Footer ───────────────────────────────────────────────
render_disclaimer()
