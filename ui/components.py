"""Componentes premium de la interfaz de usuario estilo Apilex."""

import streamlit as st
import time

def render_dashboard(data):
    """Renderiza el tablero de análisis completo con Semáforo Global."""
    st.markdown('<div class="hero-container">', unsafe_allow_html=True)
    st.markdown(f'<h1 class="main-title">Análisis Finalizado</h1>', unsafe_allow_html=True)
    
    # ── SEMÁFORO GLOBAL (ALERTA VISUAL) ──────────────────
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

    # 1. Resumen Ejecutivo (Premium Card)
    st.markdown('<div class="risk-card animated-card">', unsafe_allow_html=True)
    st.markdown(f'<h2 style="color: var(--primary);">Resumen Ejecutivo</h2>', unsafe_allow_html=True)
    st.markdown(f'<p style="color: var(--text-main); line-height: 1.6;">{data.get("resumen_ejecutivo", "Sin resumen.")}</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1], gap="large")

    with col1:
        st.markdown('<div class="risk-card animated-card">', unsafe_allow_html=True)
        st.markdown(f'<h2 style="color: var(--primary);">Identificación</h2>', unsafe_allow_html=True)
        ident = data.get("identificacion", {})
        for k, v in ident.items():
            st.markdown(f"**{k.replace('_', ' ').title()}:** {v}")
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="risk-card animated-card">', unsafe_allow_html=True)
        st.markdown(f'<h2 style="color: var(--primary);">Obligaciones Clave</h2>', unsafe_allow_html=True)
        obli = data.get("obligaciones", {})
        for k, v in obli.items():
            st.markdown(f"* {v}")
        st.markdown('</div>', unsafe_allow_html=True)

    # 3. Mapeo de Riesgos Detallados
    st.markdown('<h2 style="margin-top: 2rem; color: #FFFFFF; font-family: Outfit;">Mapa Detallado de Contención</h2>', unsafe_allow_html=True)
    
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
                    <strong style="color: var(--text-main); font-size: 1.1rem;">{r.get('categoria', 'Riesgo')}</strong>
                    <span style="margin-left: auto; color: var(--text-muted); font-size: 0.8rem;">{nivel}</span>
                </div>
                <p style="color: var(--text-muted);">{r.get('descripcion', '')}</p>
                <div style="background: rgba(0,0,0,0.2); border-radius: 8px; padding: 10px; margin-top: 10px; border-left: 3px solid var(--primary);">
                    <small style="color: var(--primary);">🔍 Recomendación:</small><br/>
                    <span style="font-size: 0.9rem; color: var(--text-main);">{r.get('recomendacion', '')}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

def render_sidebar():
    """Barra lateral."""
    with st.sidebar:
        st.markdown("<h2 style='color: white;'>Copiloto Jurídico</h2>", unsafe_allow_html=True)
        st.markdown("<hr/>", unsafe_allow_html=True)
        st.markdown("<p style='color: #94A3B8;'>Analista inteligente para EAFIT.</p>", unsafe_allow_html=True)
        st.info("✅ Conectado a **Groq (Llama 3.3)**")

def show_loading_animation():
    """Carga."""
    return st.spinner("⚖️ Analizando estructura legal...")
