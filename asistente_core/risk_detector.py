"""Lógica para clasificar riesgos y determinar el semáforo final."""

def process_analysis_results(analysis_raw: dict) -> dict:
    """Detecta riesgos adicionales y asigna colores al semáforo."""
    
    # Si viene con error del LLM, devolvemos eso
    if analysis_raw.get("error"):
        return analysis_raw

    riesgos = analysis_raw.get("riesgos", [])
    
    # Calcular nivel de severidad para el semáforo
    severidad_max = "BAJO"
    niveles_prioridad = {"ALTO": 3, "MEDIO": 2, "BAJO": 1}
    
    for r in riesgos:
        # Aceptar tanto "level" (del prompt LLM) como "nivel"
        nivel = r.get("level", r.get("nivel", "BAJO")).upper()
        # Normalizar: asegurar que el riesgo tenga ambos campos
        r["nivel"] = nivel
        r["level"] = nivel
        if niveles_prioridad.get(nivel, 0) > niveles_prioridad.get(severidad_max, 0):
            severidad_max = nivel
            
    # Inyectar el semáforo final en los datos
    analysis_raw["semaforo"] = severidad_max
    
    return analysis_raw
