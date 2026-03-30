"""Componentes premium de la interfaz de usuario estilo Apilex."""

import streamlit as st
import time

def render_dashboard(data):
    """Renderiza el tablero de análisis completo."""
    st.markdown('<div class="hero-container">', unsafe_allow_html=True)
    st.markdown(f'<h1 class="main-title">Análisis Finalizado</h1>', unsafe_allow_html=True)
    
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

    # 3. Mapeo de Riesgos (Semáforo Premium)
    st.markdown('<h2 style="margin-top: 2rem; color: #FFFFFF; font-family: Outfit;">Mapa de Riesgos Jurídicos</h2>', unsafe_allow_html=True)
    
    riesgos = data.get("riesgos", [])
    if not riesgos:
        st.info("No se detectaron riesgos específicos.")
    else:
        for r in riesgos:
            nivel = r.get("nivel", "BAJO").upper()
            status_class = f"status-{nivel.lower()}"
            
            st.markdown(f"""
            <div class="risk-card animated-card">
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
    """Muestra detalles y créditos en la barra lateral."""
    with st.sidebar:
        st.markdown(
            """
            <h2 style="color: #FFFFFF; font-family: Outfit; font-weight: 700;">Copiloto Jurídico EAFIT</h2>
            <hr style="border-color: rgba(255,255,255,0.1)"/>
            """, 
            unsafe_allow_html=True
        )
        
        st.markdown("""
        <div style="background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.1); border-radius: 12px; padding: 1.2rem;">
            <p style="color: var(--text-muted); font-size: 0.9rem; line-height: 1.5;">
                Analista Legal Inteligente entrenado para la normativa colombiana y el reglamento de EAFIT.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br/>", unsafe_allow_html=True)
        st.info("✅ Conectado a **Groq (Llama 3.3)**")
        st.success("🤖 Motor Jurídico optimizado")

def show_loading_animation():
    """Animación personalizada de carga."""
    return st.spinner("⚖️ Analizando estructura legal, verificando normativa y detectando riesgos potenciales... Esto toma unos segundos.")
