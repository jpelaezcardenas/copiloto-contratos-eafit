"""Componentes premium de la interfaz de usuario estilo Apilex."""

import streamlit as st

def _format_value(value):
    """Limpia valores para mostrarlos de forma elegante en la UI."""
    if isinstance(value, list):
        return ", ".join([str(i) for i in value if str(i).strip()])
    if isinstance(value, bool):
        return "Sí" if value else "No"
    if isinstance(value, dict):
        # Convertir diccionario a texto legible: "Clave: Valor, Clave2: Valor2"
        parts = []
        for k, v in value.items():
            k_clean = k.replace('_', ' ').title()
            v_clean = _format_value(v) # Recursivo
            parts.append(f"{k_clean}: {v_clean}")
        return " | ".join(parts)
    if value == "No especificado" or value == ["No especificado"]:
        return "Pendiente de identificar"
    return str(value)

def render_dashboard(data):
    """Renderiza el tablero con estética institucional EAFIT."""
    # Logo superior centrado
    st.markdown('<div style="text-align: center; margin-bottom: 2rem;">', unsafe_allow_html=True)
    st.image("LOGO EAFIT BLANCO.jpg", width=200)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="hero-container">', unsafe_allow_html=True)
    st.markdown(f'<h1 class="main-title">Reporte de Análisis Legal</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Secretaría General - Universidad EAFIT</p>', unsafe_allow_html=True)
    
    # ── SEMÁFORO GLOBAL ──────────────────
    semaforo = data.get("semaforo", "BAJO").upper()
    label_map = {
        "ALTO": "RIESGO CRÍTICO DETECTADO",
        "MEDIO": "RIESGO MODERADO - REVISIÓN REQUERIDA",
        "BAJO": "CONTRATO SEGURO - RIESGOS MÍNIMOS"
    }
    
    st.markdown(f"""
    <div class="semaforo-banner semaforo-glow-{semaforo} animated-card">
        <div style="font-size: 0.9rem; color: #A0A0A0; text-transform: uppercase; letter-spacing: 2px; margin-bottom: 1rem;">Nivel de Riesgo Institucional</div>
        <h2 class="semaforo-text text-{semaforo}" style="font-size: 4rem; font-weight: 900;">{semaforo}</h2>
        <div style="margin-top: 1rem; font-weight: 600; color: white;">{label_map.get(semaforo, "")}</div>
    </div>
    """, unsafe_allow_html=True)

    # 1. Resumen Ejecutivo
    st.markdown('<div class="risk-card animated-card">', unsafe_allow_html=True)
    st.markdown(f'<h2 style="color: var(--accent-yellow); margin-bottom: 1.5rem;">Concepto Jurídico</h2>', unsafe_allow_html=True)
    st.markdown(f'<p style="color: var(--text-main); line-height: 1.8; font-size: 1.15rem;">{data.get("resumen_ejecutivo", "Sin resumen.")}</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1], gap="large")

    with col1:
        st.markdown('<div class="risk-card animated-card" style="height: 100%;">', unsafe_allow_html=True)
        st.markdown(f'<h3 style="color: var(--accent-yellow); border-bottom: 1px solid var(--border); padding-bottom: 10px; margin-bottom: 15px;">🔍 Identificación</h3>', unsafe_allow_html=True)
        ident = data.get("identificacion", {})
        for k, v in ident.items():
            key_clean = k.replace('_', ' ').title()
            val_clean = _format_value(v)
            st.markdown(f"<div style='margin-bottom: 8px;'><span style='color:var(--text-muted); font-size: 0.9rem;'>{key_clean}:</span><br/><span style='color:white; font-weight: 500;'>{val_clean}</span></div>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="risk-card animated-card" style="height: 100%;">', unsafe_allow_html=True)
        st.markdown(f'<h3 style="color: var(--accent-yellow); border-bottom: 1px solid var(--border); padding-bottom: 10px; margin-bottom: 15px;">📝 Obligaciones Clave</h3>', unsafe_allow_html=True)
        obli = data.get("obligaciones", {})
        for k, v in obli.items():
            val_clean = _format_value(v)
            if val_clean and val_clean != "No":
                st.markdown(f"""
                <div style="margin-bottom: 12px; display: flex; gap: 10px; align-items: flex-start;">
                    <div style="color: var(--accent-yellow); margin-top: 4px;">•</div>
                    <div style="color: white; font-size: 0.95rem;">{val_clean}</div>
                </div>
                """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # 3. Mapeo de Riesgos Detallados
    st.markdown('<h2 style="margin-top: 4rem; margin-bottom: 2rem; color: #FFFFFF; font-family: Outfit; text-align: center;">Matriz de Hallazgos y Mitigación</h2>', unsafe_allow_html=True)
    
    riesgos = data.get("riesgos", [])
    if not riesgos:
        st.success("✅ No se identificaron riesgos que requieran atención inmediata.")
    else:
        for r in riesgos:
            nivel = r.get("nivel", "BAJO").upper()
            st.markdown(f"""
            <div class="risk-card animated-card" style="border-left: 5px solid var(--accent-{nivel.lower() if nivel != 'ALTO' else 'red'});">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
                    <strong style="color: white; font-size: 1.2rem;">{_format_value(r.get('categoria', 'Riesgo'))}</strong>
                    <span style="background: rgba(255,255,255,0.1); padding: 4px 12px; border-radius: 20px; color: var(--accent-{nivel.lower() if nivel != 'ALTO' else 'red'}); font-size: 0.8rem; font-weight: 800;">{nivel}</span>
                </div>
                <p style="color: #ccc; font-size: 1rem; margin-bottom: 1.5rem;">{_format_value(r.get('descripcion', ''))}</p>
                <div style="background: #000; border: 1px solid #333; border-radius: 8px; padding: 15px; border-left: 3px solid var(--accent-yellow);">
                    <div style="color: var(--accent-yellow); font-size: 0.7rem; font-weight: 800; text-transform: uppercase; margin-bottom: 5px; letter-spacing: 1px;">Sugerencia de la Secretaría General</div>
                    <div style="font-size: 1rem; color: white; line-height: 1.5;">{_format_value(r.get('recomendacion', ''))}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

def render_sidebar():
    """Barra lateral con identidad EAFIT."""
    with st.sidebar:
        st.image("LOGO EAFIT BLANCO.jpg", use_container_width=True)
        st.markdown("<div style='text-align: center; margin-top: -10px; margin-bottom: 20px;'><small style='color: #666;'>VIGILADA MINEDUCACIÓN</small></div>", unsafe_allow_html=True)
        st.markdown("<hr style='border-color: rgba(255,255,255,0.1)'/>", unsafe_allow_html=True)
        st.markdown("### Copiloto de Contratos")
        st.markdown("<p style='color: #A0A0A0; font-size: 0.85rem;'>Sistema de soporte para la toma de decisiones legales y gestión de riesgos contractuales.</p>", unsafe_allow_html=True)
        st.write("")
        st.markdown("---")
        st.markdown("#### Configuración")
        st.info("🤖 **Llama 3.3 (Groq)**")

def render_footer():
    """Footer institucional basado en la imagen 'termina'."""
    st.markdown(f"""
    <div class="eafit-footer">
        <div class="footer-grid">
            <div class="footer-col">
                <img src="https://itinerarioestudiantil.com/wp-content/uploads/2024/02/EAFIT_logo_blanco.png" width="150" style="margin-bottom: 1.5rem;">
                <p>Universidad EAFIT</p>
                <p>Personería Jurídica: Res. 75 del 28 de junio de 1960 - Mineducación.</p>
            </div>
            <div class="footer-col">
                <h4>EAFIT Medellín</h4>
                <p>Carrera 49 N° 7 Sur-50</p>
                <p>Línea nacional: 01 8000 515 900</p>
                <p>Línea de atención: (57) 604 2619500</p>
            </div>
            <div class="footer-col">
                <h4>EAFIT Pereira</h4>
                <p>Carrera 19 #12-70 Megacentro Pinares</p>
                <p>Línea de atención: (57) 606 3214115</p>
                <p>Correo: eafit.pereira@eafit.edu.co</p>
            </div>
            <div class="footer-col">
                <h4>EAFIT Bogotá</h4>
                <p>Carrera 15 #88-64 oficina 401</p>
                <p>Línea de atención: (57) 601 6114618</p>
                <p>Correo: eafit.bogota@eafit.edu.co</p>
            </div>
        </div>
        <div class="footer-social">
            <p style="font-size: 0.8rem; color: #555;">© 2024 Universidad EAFIT - Todos los derechos reservados</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

def show_loading_animation():
    """Animación de carga personalizada."""
    return st.spinner("⚖️ Analizando normativa institucional... Detectando cláusulas de riesgo...")
