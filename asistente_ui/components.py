"""Componentes premium de la interfaz de usuario estilo Apilex."""

import json
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
    st.markdown('<div class="hero-container">', unsafe_allow_html=True)
    st.markdown(f'<h1 class="main-title">Reporte de Análisis Legal</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Secretaría General - Universidad EAFIT</p>', unsafe_allow_html=True)
    
    # ── SEMÁFORO GLOBAL ──────────────────
    semaforo = data.get("semaforo", "BAJO").upper()
    label_map = {
        "ALTO": "RIESGO CRÍTICO DETECTADO",
        "MODERADO": "RIESGO MODERADO - REVISIÓN REQUERIDA",
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
            nivel = r.get("level", r.get("nivel", "BAJO")).upper()
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

    # ── DESCARGA JSON ESTRUCTURADO ────────────────────────
    st.markdown('<div style="text-align: center; margin-top: 3rem;">', unsafe_allow_html=True)
    st.download_button(
        label="📥 Descargar Análisis Completo (JSON)",
        data=json.dumps(data, ensure_ascii=False, indent=2),
        file_name="analisis_contrato_eafit.json",
        mime="application/json",
        use_container_width=False,
    )
    st.markdown('</div>', unsafe_allow_html=True)

def render_sidebar():
    """Barra lateral con identidad EAFIT."""
    with st.sidebar:
        st.image("LOGO EAFIT BLANCO.jpg", use_container_width=True)
        st.markdown("<hr style='border-color: rgba(255,255,255,0.1)'/>", unsafe_allow_html=True)
        st.markdown("### Ecosistema de Innovación Universidad EAFIT")
        st.markdown("<p style='color: #A0A0A0; font-size: 0.85rem;'>Impulsando la eficiencia jurídica con IA</p>", unsafe_allow_html=True)
        
        # ── HISTORIAL DE SESIÓN ──
        if "history" in st.session_state and st.session_state.history:
            st.markdown("---")
            st.markdown("#### 🕒 Historial de Análisis")
            st.markdown("<p style='color: #A0A0A0; font-size: 0.8rem;'>Documentos evaluados hoy:</p>", unsafe_allow_html=True)
            for idx, item in enumerate(reversed(st.session_state.history)):
                # Mostrar botón para restaurar
                # item["name"] tiene el nombre del doc o timestamp
                if st.button(f"📄 {item['name'][:25]}...", key=f"hist_{idx}", use_container_width=True):
                    st.session_state.analysis_complete = True
                    st.session_state.analysis_data = item['data']
                    st.session_state.comparison_complete = False
                    st.rerun()
                    
        st.markdown("---")
        st.markdown("""
<div style="background: rgba(25, 25, 35, 0.5); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 8px; padding: 12px; margin-top: 10px; font-family: 'Inter', sans-serif;">
<div style="display: flex; align-items: center; margin-bottom: 12px;">
<div style="background: rgba(255,87,34,0.1); border-radius: 6px; padding: 4px; margin-right: 12px; width: 28px; height: 28px; display: flex; justify-content: center; align-items: center;">
<span style="font-size: 16px;">🧠</span>
</div>
<div style="line-height: 1.3;">
<div style="color: #FFF; font-size: 13px; font-weight: 600;">LPU Groq Inference</div>
<div style="color: #9E9E9E; font-size: 11px;">Motor Llama 3.3 Ultra-rápido</div>
</div>
</div>
<div style="display: flex; align-items: center; margin-bottom: 12px;">
<div style="background: rgba(255,75,75,0.1); border-radius: 6px; padding: 4px; margin-right: 12px; width: 28px; height: 28px; display: flex; justify-content: center; align-items: center;">
<span style="font-size: 16px;">☁️</span>
</div>
<div style="line-height: 1.3;">
<div style="color: #FFF; font-size: 13px; font-weight: 600;">Streamlit Cloud</div>
<div style="color: #9E9E9E; font-size: 11px;">Alojamiento Serverless & UI</div>
</div>
</div>
<div style="display: flex; align-items: center; margin-bottom: 12px;">
<div style="background: rgba(66,133,244,0.1); border-radius: 6px; padding: 4px; margin-right: 12px; width: 28px; height: 28px; display: flex; justify-content: center; align-items: center;">
<span style="font-size: 16px;">🌐</span>
</div>
<div style="line-height: 1.3;">
<div style="color: #FFF; font-size: 13px; font-weight: 600;">Google GenAI</div>
<div style="color: #9E9E9E; font-size: 11px;">Capacidades Semánticas Core</div>
</div>
</div>
<div style="display: flex; align-items: center;">
<div style="background: rgba(255,212,59,0.1); border-radius: 6px; padding: 4px; margin-right: 12px; width: 28px; height: 28px; display: flex; justify-content: center; align-items: center;">
<span style="font-size: 16px;">🐍</span>
</div>
<div style="line-height: 1.3;">
<div style="color: #FFF; font-size: 13px; font-weight: 600;">Python Native API</div>
<div style="color: #9E9E9E; font-size: 11px;">Orquestación Backend Segura</div>
</div>
</div>
</div>
""", unsafe_allow_html=True)

def render_footer():
    """Footer institucional minimalista."""
    st.markdown("""
    <div style="text-align: center; color: #444; font-size: 0.70rem; padding: 1rem 0; margin-top: 2rem; border-top: 1px solid #222;">
        &copy; 2024 Universidad EAFIT - Medellín, Colombia
    </div>
    """, unsafe_allow_html=True)

def show_loading_animation():
    """Animación de carga personalizada."""
    return st.spinner("⚖️ Analizando normativa institucional... Detectando cláusulas de riesgo...")

def render_comparison_dashboard(data, name1="Contrato 1", name2="Contrato 2"):
    """Renderiza el tablero de comparación de dos contratos."""
    st.markdown('<div class="hero-container">', unsafe_allow_html=True)
    st.markdown(f'<h1 class="main-title">Análisis Legal Comparativo</h1>', unsafe_allow_html=True)
    st.markdown(f'<p class="subtitle">Contrastando: {name1} vs {name2}</p>', unsafe_allow_html=True)
    
    st.markdown('<div class="risk-card animated-card">', unsafe_allow_html=True)
    st.markdown(f'<h2 style="color: var(--accent-yellow); margin-bottom: 1.5rem;">Resumen de la Comparación</h2>', unsafe_allow_html=True)
    st.markdown(f'<p style="color: var(--text-main); line-height: 1.8; font-size: 1.15rem;">{data.get("resumen_comparacion", "Sin resumen.")}</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    diferencias = data.get("diferencias", [])
    if not diferencias:
        st.info("No se encontraron diferencias reseñables entre los documentos.")
    else:
        st.markdown('<h2 style="margin-top: 3rem; margin-bottom: 2rem; color: #FFFFFF; font-family: Outfit; text-align: center;">Diferencias Clave Detectadas</h2>', unsafe_allow_html=True)
        for diff in diferencias:
            impacto = diff.get("impacto", "NEUTRO").upper()
            
            # Colores por impacto para EAFIT (Verde, Amarillo, Rojo/Naranja)
            color_impacto = "var(--text-muted)"
            if impacto == "FAVORABLE": color_impacto = "var(--accent-bajo)"
            elif impacto == "DESFAVORABLE": color_impacto = "var(--accent-alto)"
            
            st.markdown(f"""
            <div class="risk-card animated-card" style="border-left: 5px solid {color_impacto};">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
                    <strong style="color: white; font-size: 1.2rem;">{diff.get('aspecto', 'Diferencia')}</strong>
                    <span style="background: rgba(255,255,255,0.1); padding: 4px 12px; border-radius: 20px; color: {color_impacto}; font-size: 0.8rem; font-weight: 800;">{impacto}</span>
                </div>
                
                <div style="display: flex; gap: 20px; margin-bottom: 15px;">
                    <div style="flex: 1; min-width: 0; background: rgba(0,0,0,0.3); padding: 15px; border-radius: 8px;">
                        <span style="color: #888; font-size: 0.8rem; text-transform: uppercase;">Versión 1 ({name1[:15]})</span><br/>
                        <span style="color: #ccc; font-size: 0.95rem;">{diff.get('contrato_1', '')}</span>
                    </div>
                    <div style="flex: 1; min-width: 0; background: rgba(0,0,0,0.3); padding: 15px; border-radius: 8px; border: 1px solid rgba(255,255,255,0.05);">
                        <span style="color: #888; font-size: 0.8rem; text-transform: uppercase;">Versión 2 ({name2[:15]})</span><br/>
                        <span style="color: #ccc; font-size: 0.95rem;">{diff.get('contrato_2', '')}</span>
                    </div>
                </div>
                
                <div style="background: rgba(4, 31, 58, 0.4); border-radius: 8px; padding: 15px; border-left: 3px solid var(--accent-yellow);">
                    <div style="color: var(--accent-yellow); font-size: 0.75rem; font-weight: 800; text-transform: uppercase; margin-bottom: 5px; letter-spacing: 1px;">Análisis e Implicaciones</div>
                    <div style="font-size: 0.95rem; color: white;">{diff.get('comentario', '')}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
    # ── DESCARGA JSON COMP ────────────────────────
    st.markdown('<div style="text-align: center; margin-top: 3rem;">', unsafe_allow_html=True)
    st.download_button(
        label="📥 Descargar Comparación (JSON)",
        data=json.dumps(data, ensure_ascii=False, indent=2),
        file_name="comparacion_contratos_eafit.json",
        mime="application/json",
        use_container_width=False,
    )
    st.markdown('</div>', unsafe_allow_html=True)

def render_evaluation_tab():
    """Renderiza el modo de evaluación de capacidad de detección."""
    from asistente_core.demo_cases import DEMO_CASES
    
    st.markdown('<div class="hero-container">', unsafe_allow_html=True)
    st.markdown('<h1 class="main-title">Evaluación de Capacidades</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Prueba el motor de IA con escenarios de riesgo prediseñados para verificar la profundidad del análisis institucional.</p>', unsafe_allow_html=True)
    
    st.markdown('<div style="height: 2rem;"></div>', unsafe_allow_html=True)
    
    cols = st.columns(len(DEMO_CASES))
    for i, (name, case) in enumerate(DEMO_CASES.items()):
        with cols[i]:
            st.markdown(f"""
            <div class="risk-card animated-card" style="min-height: 250px; display: flex; flex-direction: column; justify-content: space-between;">
                <h4 style="color: var(--accent-yellow); margin-top: 0;">{name}</h4>
                <p style="font-size: 0.9rem; color: #ccc;">{case['description']}</p>
            </div>
            """, unsafe_allow_html=True)
            if st.button(f"Cargar {name.split(' ')[0]}", key=f"btn_demo_{i}", use_container_width=True):
                st.session_state.pasted_text_demo = case['text']
                st.session_state.demo_name = name
                st.info(f"✅ Ejemplo '{name}' cargado en la pestaña 'Pegar Texto'. Ve allí para iniciar el análisis.")

    st.markdown("""
    <div style="background: rgba(255, 204, 0, 0.05); border: 1px solid rgba(255, 204, 0, 0.2); border-radius: 12px; padding: 20px; margin-top: 2rem;">
        <h4 style="color: var(--accent-yellow); margin-top: 0;">¿Qué estamos evaluando?</h4>
        <ul style="color: #ccc; font-size: 0.95rem;">
            <li><b>Detección de asimetrías:</b> Desequilibrios en plazos, multas y facultades unilaterales.</li>
            <li><b>Cláusulas abusivas encubiertas:</b> Renuncias de vicios ocultos o cobros de infraestructura.</li>
            <li><b>Propiedad Intelectual (PI):</b> Cesión de desarrollos previos o pérdida de código fuente.</li>
            <li><b>Riesgos económicos:</b> Reajustes excesivos o penalidades desproporcionadas.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

