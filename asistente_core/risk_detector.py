"""Lógica para clasificar riesgos y determinar el semáforo final."""

def process_analysis_results(analysis_raw: dict) -> dict:
    """Detecta riesgos adicionales y asigna colores al semáforo."""
    
    # Si viene con error del LLM, devolvemos eso
    if analysis_raw.get("error"):
        return analysis_raw

    riesgos = analysis_raw.get("riesgos", [])
    
    # Calcular nivel de severidad para el semáforo
    # Respetamos el semáforo del LLM si ya es ALTO
    llm_semaforo = str(analysis_raw.get("semaforo", "BAJO")).upper()
    severidad_max = llm_semaforo if llm_semaforo in ["ALTO", "MODERADO", "MEDIO"] else "BAJO"
    
    niveles_prioridad = {"ALTO": 3, "MEDIO": 2, "MODERADO": 2, "BAJO": 1}
    
    for r in riesgos:
        # Aceptar tanto "level" como "nivel"
        nivel = r.get("level", r.get("nivel", "BAJO")).upper()
        # Normalizar
        r["nivel"] = nivel
        r["level"] = nivel
        if niveles_prioridad.get(nivel, 0) > niveles_prioridad.get(severidad_max, 0):
            severidad_max = nivel
            
    # Si el semáforo es ALTO o MEDIO pero no hay riesgos en la lista,
    # inyectamos un riesgo informativo para que el usuario no vea la tabla vacía
    if severidad_max in ["ALTO", "MODERADO", "MEDIO"] and not riesgos:
        riesgos.append({
            "categoria": "Riesgos en Concepto",
            "nivel": severidad_max,
            "descripcion": "Se detectaron riesgos críticos mencionados en el resumen ejecutivo que requieren atención.",
            "clausula": "Ver Resumen",
            "referencia_legal": "Múltiples",
            "recomendacion": "Revisar el 'Concepto Jurídico' arriba para detalles específicos de los riesgos detectados por la IA."
        })
        analysis_raw["riesgos"] = riesgos

    # Inyectar el semáforo final
    analysis_raw["semaforo"] = severidad_max
    
    return analysis_raw
