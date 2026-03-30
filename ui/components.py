"""Componentes reutilizables de la interfaz Streamlit."""

import streamlit as st
from core.risk_detector import (
    classify_risk_level,
    get_risk_category_info,
    get_risk_nivel_badge,
    get_risk_stats,
)


def render_header():
    """Renderiza el encabezado principal."""
    st.markdown(
        """
        <div class="main-header animate-in">
            <h1>⚖️ Copiloto Jurídico</h1>
            <p>Asistente Inteligente para Análisis de Contratos — Universidad EAFIT</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_upload_section():
    """Renderiza la sección de carga de archivos."""
    st.markdown(
        """
        <div class="upload-area animate-in">
            <div class="upload-icon">📄</div>
            <div class="upload-text">
                Arrastra tu contrato PDF aquí o haz clic para seleccionarlo
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    uploaded_file = st.file_uploader(
        "Cargar contrato PDF",
        type=["pdf"],
        label_visibility="collapsed",
        help="Máximo 50 MB. Solo archivos PDF.",
    )
    return uploaded_file


def render_document_info(extraction: dict):
    """Renderiza la información del documento extraído."""
    meta = extraction.get("metadata", {})
    st.markdown(
        f"""
        <div class="glass-card animate-in">
            <h3>📋 Documento Cargado</h3>
            <div class="info-grid">
                <div class="info-item">
                    <div class="info-label">Páginas</div>
                    <div class="info-value">{extraction['page_count']}</div>
                </div>
                <div class="info-item">
                    <div class="info-label">Palabras</div>
                    <div class="info-value">{len(extraction['text'].split()):,}</div>
                </div>
                <div class="info-item">
                    <div class="info-label">Tablas</div>
                    <div class="info-value">{len(extraction['tables'])}</div>
                </div>
                <div class="info-item">
                    <div class="info-label">Título</div>
                    <div class="info-value">{meta.get('title', 'No especificado') or 'No especificado'}</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_semaforo(semaforo: str):
    """Renderiza el semáforo de cumplimiento."""
    info = classify_risk_level(semaforo)
    st.markdown(
        f"""
        <div class="semaforo-container animate-in" style="
            background: {info['bg_color']};
            border: 1px solid {info['border_color']};
        ">
            <div class="semaforo-emoji">{info['emoji']}</div>
            <div class="semaforo-label" style="color: {info['color']};">
                {info['label']}
            </div>
            <div class="semaforo-desc" style="color: {info['color']};">
                {info['description']}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_identificacion(identificacion: dict):
    """Renderiza la sección de identificación del contrato."""
    partes = identificacion.get("partes", {})

    items_html = ""
    fields = [
        ("Contratante", partes.get("contratante", "No identificado")),
        ("Contratista", partes.get("contratista", "No identificado")),
        ("Tipo de Contrato", identificacion.get("tipo_contrato", "No identificado")),
        ("Objeto", identificacion.get("objeto", "No identificado")),
        ("Valor", identificacion.get("valor", "No especificado")),
        ("Forma de Pago", identificacion.get("forma_pago", "No especificada")),
        ("Plazo de Ejecución", identificacion.get("plazo_ejecucion", "No especificado")),
        ("Vigencia", identificacion.get("vigencia", "No especificada")),
        ("Lugar", identificacion.get("lugar_ejecucion", "No especificado")),
        ("Fecha", identificacion.get("fecha_suscripcion", "No especificada")),
    ]

    for label, value in fields:
        items_html += f"""
            <div class="info-item">
                <div class="info-label">{label}</div>
                <div class="info-value">{value}</div>
            </div>
        """

    st.markdown(
        f"""
        <div class="glass-card animate-in">
            <h3>🔍 Identificación del Contrato</h3>
            <div class="info-grid">{items_html}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_obligaciones(obligaciones: dict):
    """Renderiza la sección de obligaciones."""
    contratante_obs = obligaciones.get("contratante", [])
    contratista_obs = obligaciones.get("contratista", [])

    col1, col2 = st.columns(2)

    with col1:
        contratante_html = "".join(
            f"<li>{o}</li>" for o in contratante_obs
        ) if contratante_obs else "<li>No identificadas</li>"
        st.markdown(
            f"""
            <div class="glass-card">
                <h3>🏛️ Obligaciones del Contratante</h3>
                <ul style="color: #94a3b8; font-size: 0.9rem; line-height: 1.8;">
                    {contratante_html}
                </ul>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col2:
        contratista_html = "".join(
            f"<li>{o}</li>" for o in contratista_obs
        ) if contratista_obs else "<li>No identificadas</li>"
        st.markdown(
            f"""
            <div class="glass-card">
                <h3>👤 Obligaciones del Contratista</h3>
                <ul style="color: #94a3b8; font-size: 0.9rem; line-height: 1.8;">
                    {contratista_html}
                </ul>
            </div>
            """,
            unsafe_allow_html=True,
        )

    if obligaciones.get("hay_desequilibrio"):
        st.markdown(
            f"""
            <div class="glass-card" style="border-left: 4px solid #f59e0b;">
                <h3>⚠️ Desequilibrio Detectado</h3>
                <p>{obligaciones.get('nota_desequilibrio', '')}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )


def render_risks(riesgos: list):
    """Renderiza la lista de riesgos detectados."""
    if not riesgos:
        st.markdown(
            """
            <div class="glass-card" style="text-align: center;">
                <h3>✅ Sin riesgos significativos detectados</h3>
                <p>El contrato no presenta riesgos críticos evidentes.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        return

    # Métricas de riesgo
    stats = get_risk_stats(riesgos)
    st.markdown(
        f"""
        <div class="metric-row animate-in">
            <div class="metric-card">
                <div class="metric-value">{stats['total']}</div>
                <div class="metric-label">Total Riesgos</div>
            </div>
            <div class="metric-card">
                <div class="metric-value" style="background: linear-gradient(135deg, #ef4444, #dc2626);
                -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
                    {stats['por_nivel'].get('ALTO', 0)}
                </div>
                <div class="metric-label">Críticos</div>
            </div>
            <div class="metric-card">
                <div class="metric-value" style="background: linear-gradient(135deg, #f59e0b, #d97706);
                -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
                    {stats['por_nivel'].get('MEDIO', 0)}
                </div>
                <div class="metric-label">Moderados</div>
            </div>
            <div class="metric-card">
                <div class="metric-value" style="background: linear-gradient(135deg, #10b981, #059669);
                -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
                    {stats['por_nivel'].get('BAJO', 0)}
                </div>
                <div class="metric-label">Bajos</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Tarjetas de riesgo individual
    # Ordenar: ALTO primero, luego MEDIO, luego BAJO
    order = {"ALTO": 0, "MEDIO": 1, "BAJO": 2, "NO_APLICA": 3}
    sorted_risks = sorted(riesgos, key=lambda r: order.get(r.get("nivel", "MEDIO"), 2))

    for risk in sorted_risks:
        nivel = risk.get("nivel", "MEDIO")
        if nivel == "NO_APLICA":
            continue

        cat_info = get_risk_category_info(risk.get("categoria", ""))
        badge = get_risk_nivel_badge(nivel)

        clausula = risk.get("clausula_afectada", "")
        clausula_html = (
            f'<p class="risk-desc" style="font-style: italic; border-left: 2px solid rgba(255,255,255,0.1); padding-left: 0.8rem;">"{clausula}"</p>'
            if clausula
            else ""
        )

        rec = risk.get("recomendacion", "")
        rec_html = (
            f'<div class="risk-rec">💡 {rec}</div>' if rec else ""
        )

        st.markdown(
            f"""
            <div class="risk-card {nivel.lower()} animate-in">
                <div class="risk-header">
                    <span class="risk-title">{cat_info['icon']} {cat_info['label']}</span>
                    {badge}
                </div>
                <p class="risk-desc">{risk.get('descripcion', '')}</p>
                {clausula_html}
                <p class="risk-ref">📖 {risk.get('referencia_legal', cat_info.get('referencia', ''))}</p>
                {rec_html}
            </div>
            """,
            unsafe_allow_html=True,
        )


def render_resumen_ejecutivo(resumen: str):
    """Renderiza el resumen ejecutivo."""
    st.markdown(
        f"""
        <div class="glass-card animate-in">
            <h3>📝 Resumen Ejecutivo</h3>
            <p style="color: #cbd5e1; line-height: 1.8; font-size: 0.95rem;">{resumen}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_disclaimer():
    """Renderiza el disclaimer legal obligatorio."""
    st.markdown(
        """
        <div class="disclaimer">
            <p>
                ⚠️ <strong>Aviso Legal:</strong> Este análisis es generado por inteligencia artificial
                y tiene carácter informativo y de apoyo. <strong>No sustituye el criterio profesional
                de un abogado.</strong> Todo resultado debe ser validado por un profesional del derecho
                antes de producir efectos legales (Sentencia T-323 de 2024, Corte Constitucional de Colombia).
                La Universidad EAFIT no se hace responsable por decisiones tomadas exclusivamente
                con base en este análisis automatizado.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_sidebar():
    """Renderiza el sidebar con información del proyecto."""
    with st.sidebar:
        st.markdown(
            """
            <div style="text-align: center; padding: 1rem 0;">
                <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">⚖️</div>
                <div style="color: #a5b4fc; font-weight: 700; font-size: 1.1rem;">
                    Copiloto Jurídico
                </div>
                <div style="color: #64748b; font-size: 0.8rem;">
                    Universidad EAFIT
                </div>
            </div>
            <hr style="border-color: rgba(255,255,255,0.06); margin: 1rem 0;">
            """,
            unsafe_allow_html=True,
        )

        st.markdown("### 📌 Acerca de")
        st.markdown(
            """
            <div style="color: #94a3b8; font-size: 0.85rem; line-height: 1.6;">
                Herramienta de IA para análisis de contratos jurídicos
                de la Secretaría General de EAFIT.<br><br>
                <strong>Detecta:</strong><br>
                • Cláusulas ambiguas<br>
                • Falta de penalidades<br>
                • Cláusulas abusivas<br>
                • Ruptura de equilibrio<br>
                • Vigencia inconsistente<br>
                • Terminación deficiente
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("")
        st.markdown("### 📚 Marco Legal")
        st.markdown(
            """
            <div style="color: #94a3b8; font-size: 0.8rem; line-height: 1.6;">
                • Código Civil Colombiano<br>
                • Código Sustantivo del Trabajo<br>
                • Ley 1480 de 2011<br>
                • Ley 1581 de 2012<br>
                • Sentencia T-323 de 2024
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("")
        st.markdown(
            """
            <hr style="border-color: rgba(255,255,255,0.06); margin: 1.5rem 0 1rem;">
            <div style="text-align: center; color: #475569; font-size: 0.75rem;">
                Beca SER ANDI — Etapa 3<br>
                Powered by Google Gemini ✨
            </div>
            """,
            unsafe_allow_html=True,
        )
