"""Ejemplos de contratos para demostración y evaluación de riesgos."""

DEMO_CASES = {
    "Consultoría Jurídica (Riesgosa)": {
        "description": "Contrato de consultoría con prórrogas automáticas, cesión total de IP y penalidades asimétricas.",
        "text": """CONTRATO DE PRESTACIÓN DE SERVICIOS DE CONSULTORÍA

    Entre los suscritos, UNIVERSIDAD EAFIT (en adelante la Universidad) y el CONSULTOR JURÍDICO EXTERNO (en adelante el Consultor), se ha convenido el presente contrato:

    CLÁUSULA PRIMERA. OBJETO: El Consultor realizará la revisión de procesos legales internos.
    CLÁUSULA SEGUNDA. VIGENCIA Y PRÓRROGA: El término inicial es de 6 meses. Este contrato se prorrogará automáticamente por periodos iguales de forma indefinida, a menos que una de las partes notifique su intención de no prorrogarlo con al menos 180 días de antelación mediante correo certificado.
    CLÁUSULA TERCERA. PROPIEDAD INTELECTUAL: El Consultor cede de forma total, perpetua e irrevocable a favor de la Universidad todos los derechos de propiedad intelectual sobre los entregables, así como sobre cualquier metodología, desarrollo previo o herramienta utilizada por el Consultor para la ejecución del servicio.
    CLÁUSULA CUARTA. CONFIDENCIALIDAD: Toda información compartida tendrá carácter confidencial de forma perpetua e ilimitada, sin importar si está marcada como tal o no.
    CLÁUSULA QUINTA. NO COMPETENCIA: El Consultor se obliga a no prestar servicios similares a otras universidades en el país por un periodo de 2 años tras la terminación. El incumplimiento generará una penalidad equivalente al doble del valor total del contrato.
    CLÁUSULA SEXTA. AJUSTE DE PRECIO: Los honorarios se reajustarán automáticamente cada año con base en el IPC + 8 puntos porcentuales.
    CLÁUSULA SÉPTIMA. MODIFICACIÓN: La Universidad podrá modificar unilateralmente el alcance del servicio hasta en un 40% sin necesidad de ajustar el valor del contrato.
    CLÁUSULA OCTAVA. TERMINACIÓN: La Universidad podrá terminar el contrato en cualquier momento con aviso de 30 días. El Consultor solo podrá terminar con aviso de 180 días y el pago de una penalidad de 10 salarios mínimos.
    CLÁUSULA NOVENA. JURISDICCIÓN: Cualquier controversia se resolverá en los juzgados de la ciudad de Bogotá, asumiendo ambas partes los costos judiciales por igual.
    """
    },
    "Arrendamiento de Inmueble (Riesgoso)": {
        "description": "Contrato de arrendamiento con incrementos altos, renuncia a vicios ocultos y toma de posesión inmediata.",
        "text": """CONTRATO DE ARRENDAMIENTO DE LOCAL COMERCIAL

    CLÁUSULA 1. CANON: El canon mensual será de $5.000.000.
    CLÁUSULA 2. INCREMENTO: El incremento anual será del 10% mínimo garantizado, incluso si el IPC es inferior.
    CLÁUSULA 3. VICIOS OCULTOS: El Arrendatario acepta el inmueble en el estado en que se encuentra y renuncia a cualquier reclamación futura por vicios ocultos, filtraciones o problemas de habitabilidad descubiertos posteriormente.
    CLÁUSULA 4. DEPÓSITO: Se entrega un depósito equivalente a 3 cánones, el cual podrá ser retenido automáticamente por el Arrendador como cláusula penal ante cualquier mora, sin necesidad de proceso judicial.
    CLÁUSULA 5. TOMA DE POSESIÓN: La mora de 5 días en el pago del canon facultará al Arrendador para realizar la toma de posesión inmediata del inmueble, cambio de guardas y retiro de bienes, sin requerir orden judicial o administrativa.
    CLÁUSULA 6. COSTOS PROCESALES: Todos los costos procesales y honorarios de abogados derivados de reclamaciones serán asumidos por el Arrendatario, independientemente del resultado del proceso.
    CLÁUSULA 7. SEGUROS: El Arrendador contratará seguros cuya prima tendrá un recargo administrativo del 30% a cargo del Arrendatario.
    CLÁUSULA 8. TERMINACIÓN ASIMÉTRICA: El Arrendador podrá terminar con 60 días de aviso. El Arrendatario requiere 180 días de aviso y el pago de 3 meses de penalidad adicional.
    CLÁUSULA 9. JURISDICCIÓN: Las partes acuerdan como sede exclusiva de juzgamiento la ciudad de Cartagena de Indias.
    """
    },
    "Servicios Tecnológicos / SaaS (Riesgoso)": {
        "description": "Contrato tecnológico con vendor lock-in, SLA débil y uso de datos para entrenamiento.",
        "text": """SOFTWARE AS A SERVICE AGREEMENT (SaaS)

    1. PROPIEDAD INTELECTUAL: Toda la propiedad intelectual, incluyendo código fuente, documentación, algoritmos y mejoras sugeridas por el Cliente (EAFIT), son propiedad exclusiva del PROVEEDOR. El Cliente recibe una licencia limitada, no exclusiva, no transferible y revocable.
    2. ACUERDO DE NIVEL DE SERVICIO (SLA): Se garantiza una disponibilidad del 95%. Se excluyen fallos de infraestructura cloud, ventanas de mantenimiento programado de 72 horas mensuales y actualizaciones críticas.
    3. PENALIDADES: En caso de disponibilidad inferior al 85%, el Cliente podrá solicitar un crédito del 5%, siempre que realice el reclamo formal en los 5 días siguientes al incidente. El Proveedor decide unilateralmente la severidad de los incidentes.
    4. RESPONSABILIDAD: La responsabilidad total del Proveedor está limitada a lo que sea menor entre: a) El valor de 3 meses del servicio, o b) $50.000.000 Pesos.
    5. TERMINACIÓN Y SALIDA: Al terminar el contrato, el Proveedor no tiene obligación de entregar código fuente, documentación técnica o bases de datos relacionales. Los costos de transición serán del 150% de la tarifa mensual por 90 días.
    6. INFRAESTRUCTURA: Se aplicará un cargo administrativo del 25% sobre los costos de infraestructura Cloud (AWS/Azure) que el Proveedor traslade al Cliente.
    7. DATOS: El Proveedor podrá utilizar los datos del Cliente (incluso si no están anonimizados) para el entrenamiento de sus modelos de Inteligencia Artificial, analytics y mejora de productos de terceros.
    """
    }
}
