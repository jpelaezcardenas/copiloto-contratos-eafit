"""Componentes premium de la interfaz de usuario estilo Apilex."""

import json
import streamlit as st
import base64
import os

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

def render_dashboard(data, analysis_time=None):
    """Renderiza el tablero con estética institucional EAFIT."""
    st.markdown('<div class="hero-container">', unsafe_allow_html=True)
    st.markdown(f'<h1 class="main-title">Reporte de Análisis Contractual</h1>', unsafe_allow_html=True)
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

    # ── MÉTRICAS RÁPIDAS ──
    riesgos = data.get("riesgos", [])
    n_riesgos = len(riesgos)
    n_alto = sum(1 for r in riesgos if r.get("level", r.get("nivel", "")).upper() == "ALTO")
    n_medio = sum(1 for r in riesgos if r.get("level", r.get("nivel", "")).upper() in ["MEDIO", "MODERADO"])
    
    mcol1, mcol2, mcol3, mcol4 = st.columns(4)
    with mcol1:
        st.metric("Riesgos Detectados", n_riesgos)
    with mcol2:
        st.metric("🔴 Críticos", n_alto)
    with mcol3:
        st.metric("🟡 Moderados", n_medio)
    with mcol4:
        if analysis_time:
            st.metric("⏱️ Tiempo", f"{analysis_time:.1f}s")
        else:
            st.metric("🟢 Bajos", n_riesgos - n_alto - n_medio)

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

    # ── EVALUACIÓN PRINCIPIOS EAFIT (NUEVA SECCIÓN) ──
    principios = data.get("evaluacion_principios_eafit", {})
    if principios:
        st.markdown('<h2 style="margin-top: 3rem; margin-bottom: 2rem; color: #FFFFFF; font-family: Outfit; text-align: center;">Evaluación de Principios EAFIT</h2>', unsafe_allow_html=True)
        
        pcols = st.columns(len(principios))
        for i, (k, v) in enumerate(principios.items()):
            with pcols[i]:
                key_clean = k.replace('_', ' ').title()
                val_str = str(v)
                # Determinar color según cumplimiento
                if "CUMPLE" in val_str and "NO CUMPLE" not in val_str and "PARCIAL" not in val_str:
                    badge_color = "var(--accent-bajo)"
                    icon = "✅"
                elif "PARCIAL" in val_str:
                    badge_color = "var(--accent-yellow)"
                    icon = "⚠️"
                else:
                    badge_color = "var(--accent-alto)"
                    icon = "🔴"
                
                # Separar estado de explicación
                parts = val_str.split("—", 1) if "—" in val_str else val_str.split("-", 1)
                estado = parts[0].strip()
                explicacion = parts[1].strip() if len(parts) > 1 else ""
                
                st.markdown(f"""
                <div class="risk-card animated-card" style="text-align: center; min-height: 160px;">
                    <div style="font-size: 1.5rem; margin-bottom: 0.5rem;">{icon}</div>
                    <div style="color: var(--text-muted); font-size: 0.75rem; text-transform: uppercase; letter-spacing: 1px;">{key_clean}</div>
                    <div style="color: {badge_color}; font-weight: 800; font-size: 0.9rem; margin: 0.5rem 0;">{estado}</div>
                    <div style="color: #aaa; font-size: 0.8rem;">{explicacion}</div>
                </div>
                """, unsafe_allow_html=True)

    # 3. Mapeo de Riesgos Detallados
    st.markdown('<h2 style="margin-top: 4rem; margin-bottom: 2rem; color: #FFFFFF; font-family: Outfit; text-align: center;">Matriz de Hallazgos y Mitigación</h2>', unsafe_allow_html=True)
    
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

    # ── DESCARGA PDF + JSON ────────────────────────
    st.markdown('<div style="text-align: center; margin-top: 3rem;">', unsafe_allow_html=True)
    
    dcol1, dcol2 = st.columns(2)
    with dcol1:
        try:
            from asistente_core.pdf_report import generate_pdf_report
            pdf_bytes = generate_pdf_report(data)
            st.download_button(
                label="📄 Descargar Reporte PDF",
                data=pdf_bytes,
                file_name="reporte_analisis_contrato_eafit.pdf",
                mime="application/pdf",
                type="primary",
                icon="📄",
            )
        except Exception as e:
            st.warning(f"PDF no disponible: {e}")
            
    with dcol2:
        st.download_button(
            label="📥 Descargar Datos (JSON)",
            data=json.dumps(data, ensure_ascii=False, indent=2),
            file_name="analisis_contrato_eafit.json",
            mime="application/json",
        )
    st.markdown('</div>', unsafe_allow_html=True)

def render_sidebar():
    """Barra lateral con identidad EAFIT y pensamiento crítico arquitectónico."""
    with st.sidebar:
        st.image("LOGO EAFIT BLANCO.jpg", width="stretch")
        st.markdown("<hr style='border-color: rgba(255,255,255,0.1)'/>", unsafe_allow_html=True)
        st.markdown("### Ecosistema de Innovación Universidad EAFIT")
        st.markdown("<p style='color: #A0A0A0; font-size: 0.85rem;'>Impulsando la eficiencia jurídica con IA</p>", unsafe_allow_html=True)
        
        # ── HISTORIAL DE SESIÓN ──
        if "history" in st.session_state and st.session_state.history:
            st.markdown("---")
            st.markdown("#### 🕒 Historial de Análisis")
            st.markdown("<p style='color: #A0A0A0; font-size: 0.8rem;'>Documentos evaluados hoy:</p>", unsafe_allow_html=True)
            for idx, item in enumerate(reversed(st.session_state.history)):
                if st.button(f"📄 {item['name'][:25]}...", key=f"hist_{idx}", width="stretch"):
                    st.session_state.analysis_complete = True
                    st.session_state.analysis_data = item['data']
                    st.session_state.comparison_complete = False
                    st.rerun()
                    
        st.markdown("---")
        
        # ── PENSAMIENTO CRÍTICO: ARQUITECTURA Y TRADE-OFFS ──
        with st.expander("🧠 ¿Por qué esta arquitectura?", expanded=False):
            st.markdown("""
**¿Por qué multi-proveedor con failover?**

Los LLMs gratuitos tienen **rate limits estrictos** (ej. Groq: 30 req/min). 
Un solo proveedor = un solo punto de falla. Con 5 proveedores en cascada, 
garantizamos **disponibilidad >99.9%** sin costo de infraestructura.

**¿Por qué Groq como primario?**

Groq utiliza **LPU (Language Processing Units)**, chips especializados que 
procesan Llama 3.3 70B a ~500 tokens/seg — **10x más rápido** que GPUs 
convencionales. Para un abogado que espera resultados, la velocidad es crítica.

**¿Por qué Llama 3.3 70B y no GPT-4?**

| Factor | GPT-4 | Llama 3.3 70B |
|--------|-------|---------------|
| Costo | $30/M tokens | **$0 (API gratuita)** |
| Velocidad | ~50 tok/s | ~500 tok/s (Groq) |
| Calidad jurídica | Excelente | Muy buena |
| Privacidad | Datos en OpenAI | Groq no entrena |

**Trade-off aceptado:** Sacrificamos ~5% de calidad vs GPT-4 a cambio de 
**costo cero + 10x velocidad + mayor privacidad**. Para un MVP, es la 
decisión óptima.

**¿Por qué Streamlit y no React/Next.js?**

- **Velocidad de desarrollo:** MVP en 4 semanas vs 8-12 semanas
- **Python nativo:** Mismo lenguaje para backend y frontend
- **Deploy gratuito:** Streamlit Cloud = $0/mes
- **Trade-off:** Menos control visual, pero suficiente para un MVP

**¿Por qué sanitización anti prompt injection?**

Los PDFs pueden contener texto malicioso insertado invisiblemente. 
Sin sanitización, un atacante podría **inyectar instrucciones** que 
hagan que la IA ignore riesgos reales. Nuestra capa detecta y 
neutraliza **7 patrones de ataque** antes de que lleguen al LLM.
            """)

        # ── STACK TÉCNICO VISUAL ──
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
<div style="color: #FFF; font-size: 13px; font-weight: 600;">5 Motores IA</div>
<div style="color: #9E9E9E; font-size: 11px;">Failover automático 99.9%</div>
</div>
</div>
<div style="display: flex; align-items: center; margin-bottom: 12px;">
<div style="background: rgba(255,212,59,0.1); border-radius: 6px; padding: 4px; margin-right: 12px; width: 28px; height: 28px; display: flex; justify-content: center; align-items: center;">
<span style="font-size: 16px;">🛡️</span>
</div>
<div style="line-height: 1.3;">
<div style="color: #FFF; font-size: 13px; font-weight: 600;">Anti Prompt Injection</div>
<div style="color: #9E9E9E; font-size: 11px;">7 patrones de ataque neutralizados</div>
</div>
</div>
<div style="display: flex; align-items: center;">
<div style="background: rgba(40,167,69,0.1); border-radius: 6px; padding: 4px; margin-right: 12px; width: 28px; height: 28px; display: flex; justify-content: center; align-items: center;">
<span style="font-size: 16px;">📋</span>
</div>
<div style="line-height: 1.3;">
<div style="color: #FFF; font-size: 13px; font-weight: 600;">Reglamento EAFIT</div>
<div style="color: #9E9E9E; font-size: 11px;">Contexto institucional integrado</div>
</div>
</div>
</div>
""", unsafe_allow_html=True)

def render_footer():
    """Footer institucional completo siguiendo el diseño de EAFIT."""
    # Intentar cargar el logo para embeberlo en base64
    logo_html = ""
    try:
        # LOGO EAFIT NEGRO.jpg es el que tiene texto blanco sobre fondo negro
        logo_path = "LOGO EAFIT NEGRO.jpg"
        if os.path.exists(logo_path):
            with open(logo_path, "rb") as f:
                logo_data = base64.b64encode(f.read()).decode()
                logo_html = f'<img src="data:image/jpeg;base64,{logo_data}" style="height: 60px; margin-bottom: 2.5rem; filter: brightness(1.2);">'
        else:
            logo_html = '<h2 style="color: white; margin-bottom: 2rem; font-family: sans-serif;">UNIVERSIDAD EAFIT</h2>'
    except Exception:
        logo_html = '<h2 style="color: white; margin-bottom: 2rem; font-family: sans-serif;">UNIVERSIDAD EAFIT</h2>'

    footer_html = f"""
<div style="background-color: #000; color: #fff; padding: 40px 20px; border-top: 1px solid #333; font-family: sans-serif; min-height: 400px;">
    <div style="text-align: center; width: 100%;">
        {logo_html}
    </div>
    
    <div style="display: flex; flex-wrap: wrap; justify-content: space-between; max-width: 1100px; margin: 0 auto; gap: 30px;">
        <div style="flex: 1; min-width: 200px;">
            <h3 style="font-size: 16px; font-weight: 700; margin-bottom: 20px; border-bottom: 2px solid #333; padding-bottom: 8px; display: inline-block; color: #eee;">Virtual EAFIT</h3>
            <ul style="list-style: none; padding: 0; font-size: 14px; color: #999; line-height: 2;">
                <li>¿Por qué estudiar en EAFIT?</li>
                <li>¿Qué quieres estudiar?</li>
            </ul>
        </div>
        
        <div style="flex: 1; min-width: 200px;">
            <h3 style="font-size: 16px; font-weight: 700; margin-bottom: 20px; border-bottom: 2px solid #333; padding-bottom: 8px; display: inline-block; color: #eee;">Consultar aquí</h3>
            <ul style="list-style: none; padding: 0; font-size: 14px; color: #999; line-height: 2;">
                <li>Política de protección de datos</li>
                <li>Políticas de cookies</li>
                <li>Políticas de cancelación y devolución</li>
            </ul>
        </div>
        
        <div style="flex: 1; min-width: 200px;">
            <h3 style="font-size: 16px; font-weight: 700; margin-bottom: 20px; border-bottom: 2px solid #333; padding-bottom: 8px; display: inline-block; color: #eee;">Contáctanos</h3>
            <ul style="list-style: none; padding: 0; font-size: 14px; color: #999; line-height: 2;">
                <li>Tel: (60) (4) 2619500 opción 1 - opción 3</li>
                <li>WhatsApp: +57 310 8992908</li>
                <li>Email: inscripciones-ep@eafit.edu.co</li>
                <li>Déjanos tus datos</li>
            </ul>
        </div>
    </div>
    
    <div style="margin-top: 60px; padding-top: 20px; border-top: 1px solid #222; display: flex; flex-wrap: wrap; justify-content: space-between; align-items: center; font-size: 11px; color: #555; gap: 10px;">
        <div style="max-width: 600px;">
            Vigilada Mineducación Universidad con Acreditación Institucional hasta 2026. Todos los derechos reservados.
        </div>
        <div style="text-align: right;">
            &copy; 2026 Universidad EAFIT | Asistente Jurídico IA — Equipo Antigravity
        </div>
    </div>
</div>
"""
    # Usar st.components.v1.html para asegurar que el HTML se interprete como tal
    st.components.v1.html(footer_html, height=450)

def show_loading_animation():
    """Animación de carga personalizada."""
    return st.spinner("⚖️ Analizando normativa institucional y Reglamento EAFIT... Detectando cláusulas de riesgo en 10 categorías...")

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
        width="content",
    )
    st.markdown('</div>', unsafe_allow_html=True)
