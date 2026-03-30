"""Componentes premium de la interfaz de usuario estilo Apilex."""

import streamlit as st

def _format_value(value):
    """Limpia valores para mostrarlos de forma elegante en la UI."""
    if isinstance(value, list):
        return ", ".join([str(i) for i in value if str(i).strip()])
    if isinstance(value, bool):
        return "Sí" if value else "No"
    if value == "No especificado" or value == ["No especificado"]:
        return "Notificado como pendiente"
    return str(value)

def render_dashboard(data):
    """Renderiza el tablero con limpieza de datos profesional."""
    st.markdown('<div class="hero-container">', unsafe_allow_html=True)
    st.markdown(f'<h1 class="main-title">Análisis Finalizado</h1>', unsafe_allow_html=True)
    
    # ── SEMÁFORO GLOBAL ──────────────────
    semaforo = data.get("semaforo", "BAJO").upper()
    label_map = {
        "ALTO": "RIESGO CRÍTICO DETECTADO",
        "MEDIO": "RIESGO MODERADO - REVISIÓN REQUERIDA",
        "BAJO": "CONTRATO SEGURO - RIESGOS MÍNIMOS"
    }
    
    st.markdown(f"""
    <div class="semaforo-banner semaforo-glow-{semaforo} animated-card">
        <div class="semaforo-label">{label_map.get(semaforo, "ESTADO DEL CONTRATO")}</div>
        <h2 class="semaforo-text text-{semaforo}">{semaforo}</h2>
    </div>
    """, unsafe_allow_html=True)

    # 1. Resumen Ejecutivo
    st.markdown('<div class="risk-card animated-card">', unsafe_allow_html=True)
    st.markdown(f'<h2 style="color: var(--primary);">Análisis de Situación</h2>', unsafe_allow_html=True)
    st.markdown(f'<p style="color: var(--text-main); line-height: 1.6; font-size: 1.1rem;">{data.get("resumen_ejecutivo", "Sin resumen.")}</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1], gap="large")

    with col1:
        st.markdown('<div class="risk-card animated-card" style="height: 100%;">', unsafe_allow_html=True)
        st.markdown(f'<h3 style="color: var(--primary); border-bottom: 1px solid var(--border); padding-bottom: 10px; margin-bottom: 15px;">🔍 Identificación</h3>', unsafe_allow_html=True)
        ident = data.get("identificacion", {})
        for k, v in ident.items():
            key_clean = k.replace('_', ' ').title()
            val_clean = _format_value(v)
            st.markdown(f"<span style='color:var(--text-muted)'>{key_clean}:</span> <span style='color:white'>{val_clean}</span>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="risk-card animated-card" style="height: 100%;">', unsafe_allow_html=True)
        st.markdown(f'<h3 style="color: var(--primary); border-bottom: 1px solid var(--border); padding-bottom: 10px; margin-bottom: 15px;">📝 Obligaciones y Cláusulas</h3>', unsafe_allow_html=True)
        obli = data.get("obligaciones", {})
        for k, v in obli.items():
            val_clean = _format_value(v)
            if val_clean and val_clean != "No":
                st.markdown(f"""
                <div style="margin-bottom: 12px; display: flex; gap: 10px; align-items: flex-start;">
                    <div style="color: var(--primary); margin-top: 4px;">•</div>
                    <div style="color: white; font-size: 0.95rem;">{val_clean}</div>
                </div>
                """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # 3. Mapeo de Riesgos Detallados
    st.markdown('<h2 style="margin-top: 3rem; color: #FFFFFF; font-family: Outfit; text-align: center;">Detección de Riesgos y Contención</h2>', unsafe_allow_html=True)
    
    riesgos = data.get("riesgos", [])
    if not riesgos:
        st.info("No se detectaron riesgos específicos.")
    else:
        for r in riesgos:
            nivel = r.get("nivel", "BAJO").upper()
            status_class = f"status-{nivel.lower()}"
            
            st.markdown(f"""
            <div class="risk-card animated-card" style="border-left: 4px solid var(--accent-{nivel.lower() if nivel != 'ALTO' else 'red'});">
                <div class="risk-header">
                    <div class="risk-status {status_class}"></div>
                    <strong style="color: var(--text-main); font-size: 1.1rem;">{_format_value(r.get('categoria', 'Riesgo'))}</strong>
                    <span style="margin-left: auto; color: var(--text-muted); font-size: 0.8rem; font-weight: 600;">{nivel}</span>
                </div>
                <p style="color: var(--text-muted);">{_format_value(r.get('descripcion', ''))}</p>
                <div style="background: rgba(0,0,0,0.2); border-radius: 8px; padding: 12px; margin-top: 15px; border-left: 2px solid var(--primary);">
                    <div style="color: var(--primary); font-size: 0.75rem; font-weight: 700; text-transform: uppercase; margin-bottom: 4px;">Recomendación Jurídica</div>
                    <span style="font-size: 0.95rem; color: var(--text-main); line-height: 1.4;">{_format_value(r.get('recomendacion', ''))}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

def render_sidebar():
    """Barra lateral estilizada."""
    with st.sidebar:
        st.markdown("<h2 style='color: white; font-family: Outfit;'>Copiloto Jurídico EAFIT</h2>", unsafe_allow_html=True)
        st.markdown("<hr style='border-color: rgba(255,255,255,0.1)'/>", unsafe_allow_html=True)
        st.markdown("<p style='color: #94A3B8; font-size: 0.9rem;'>Analista inteligente optimizado para la normativa de la Secretaría General.</p>", unsafe_allow_html=True)
        st.write("")
        st.success("🤖 Motor: **Groq (Llama 3)**")
        st.info("⚡ Análisis en segundos")

def show_loading_animation():
    """Animación de carga personalizada."""
    return st.spinner("⚖️ Procesando documento legal, detectando riesgos y verificando normativa... Un momento por favor.")
