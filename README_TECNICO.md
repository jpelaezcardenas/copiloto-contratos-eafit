# 📝 Documentación Técnica Integral — Asistente Jurídico para Análisis Contractual EAFIT

**Equipo:** Antigravity  
**Versión:** 2.0 (Edición Final Premium)  
**App en producción:** [https://copiloto-contratos-eafit-iwjozruh8foqgyk8ecygff.streamlit.app/](https://copiloto-contratos-eafit-iwjozruh8foqgyk8ecygff.streamlit.app/)

---

## 🎯 Descripción de la Solución
El **Asistente Jurídico para Análisis Contractual** es una herramienta de IA avanzada diseñada específicamente para la **Secretaría General de la Universidad EAFIT**. No busca reemplazar el criterio jurídico, sino potenciar la capacidad de revisión de los abogados, automatizando la extracción de datos críticos y la detección proactiva de riesgos basados en el **Reglamento de Contratación** de la institución.

### Capacidades Principales
- **Análisis Profundo:** Identificación automática de partes, objeto, valor, plazos, vigencia y obligaciones cruzadas.
- **Auditoría Normativa:** Contraste automático contra el Reglamento de Contratación de EAFIT y normativa colombiana.
- **Matriz de 10 Categorías de Riesgo:** Cobertura expandida que incluye Propiedad Intelectual, Anticorrupción, ESG y Equilibrio Económico.
- **Comparación Inteligente:** Diferenciación semántica entre dos versiones de un contrato con evaluación de impacto.
- **Reportes Profesionales:** Generación de informes en PDF con branding institucional para archivo y toma de decisiones.

> [!IMPORTANT]
> El sistema opera bajo el principio de "Human-in-the-loop", alineado con la **Sentencia T-323 de 2024**. La IA asiste, pero la validación final siempre reside en el profesional del derecho.

---

## 🛠️ Herramientas y Tecnologías Utilizadas

### Stack Tecnológico Principal
| Capa | Tecnología | Función |
| :--- | :--- | :--- |
| **Frontend/UI** | Streamlit | Interfaz premium con *glassmorphism*, animaciones y modo oscuro institucional. |
| **Backend** | Python 3.10+ | Orquestación lógica, procesamiento de datos y manejo de sesiones. |
| **Extracción PDF** | PyMuPDF + pdfplumber | Sistema híbrido para captura precisa de texto y tablas complejas. |
| **Generación PDF** | FPDF2 | Creación de reportes dinámicos con fuentes personalizadas y logos. |
| **Hosting** | Streamlit Cloud | Infraestructura serverless de alta disponibilidad. |

### Orquestación de IA (Failover Multi-Proveedor)
Para garantizar 100% de disponibilidad, el sistema utiliza una arquitectura de redundancia:
1.  **Groq (LPU):** Motor primario para inferencia instantánea (Llama 3.3 70B).
2.  **Cerebras:** Alternativa de baja latencia.
3.  **Mistral AI:** Especialista en razonamiento jurídico complejo.
4.  **Google Gemini 2.0:** Motor de respaldo de alto rendimiento.
5.  **OpenRouter:** Línea de defensa final con acceso a modelos globales.

---

## 🤖 Implementación de la IA y Lógica Jurídica

### 1. Ingesta y Sanitización
- **Arquitectura Híbrida de Extracción:** Combina la velocidad de `fitz` para párrafos y la precisión de `pdfplumber` para tablas de pagos y cronogramas.
- **Seguridad (Anti-Prompt Injection):** Capa activa que detecta intentos de manipulación del modelo, filtrando caracteres de control y patrones de "override".

### 2. Prompt Engineering de Grado Jurídico
- **Contexto RAG-lite:** El sistema integra el **Reglamento de Contratación de EAFIT** directamente en las instrucciones del sistema, permitiendo que la IA evalúe si un contrato cumple con los principios de transparencia, economía y responsabilidad de la universidad.
- **Chain-of-Thought (CoT):** Obliga a la IA a razonar primero sobre la cláusula antes de emitir una calificación de riesgo.

### 3. Matriz de Riesgos (10 Dimensiones)
El análisis ahora cubre un espectro completo de riesgos institucionales:
1.  **Ambigüedad y Lenguaje:** Identificación de términos vagos (Art. 1624 C.C.).
2.  **Cláusulas Económicas:** Revisión de precios, impuestos y formas de pago.
3.  **Propiedad Intelectual:** Protección de activos intangibles de la Universidad.
4.  **Ruptura de Equilibrio / SLAs:** Protección ante incumplimientos técnicos.
5.  **Cláusulas Abusivas / Jurisdicción:** Cumplimiento con Ley 1480 y competencia legal.
6.  **Anticorrupción y Cumplimiento:** Alineación con leyes SARLAFT/SAGRILAFT.
7.  **Protección de Datos (Habeas Data):** Cumplimiento con Ley 1581 de 2012.
8.  **Sostenibilidad y ESG:** Criterios de impacto ambiental y social.
9.  **Vigencia y Terminación:** Condiciones de salida y prórrogas.
10. **Principios EAFIT:** Evaluación cualitativa de alineación con valores institucionales.

---

## 🏗️ Arquitectura del Proyecto
```text
asistente-contratos/
├── app.py                      → Punto de entrada alternativo
├── streamlit_app.py            → Orquestador principal de la UI
├── .streamlit/config.toml      → Configuración de tema Dark forzado
├── eafit-fondo.png             → Imagen de fondo premium (Parallax)
├── asistente_core/
│   ├── pdf_extractor.py        → Extracción + Sanitización Anti-Injection
│   ├── llm_analyzer.py         → Cerebro IA con lógica de Failover
│   ├── pdf_report.py           → Motor de generación de reportes PDF
│   ├── prompts.py              → Templates jurídicos y Reglamento EAFIT
│   └── risk_detector.py        → Clasificador de riesgos y semáforo
├── asistente_ui/
│   ├── styles.py               → Sistema de diseño (Glassmorphism, CSS)
│   └── components.py           → Componentes (Dashboard, comparación, footer)
└── requirements.txt            → Dependencias (fpdf2, groq, pymupdf, etc.)
```

---

## ✨ Funcionalidades Destacadas (Actualizadas)

| Funcionalidad | Detalle Técnico |
| :--- | :--- |
| **Tablero de Control** | Visualización en tiempo real del nivel de riesgo con semáforo dinámico. |
| **Comparador Semántico** | Analiza diferencias no solo textuales, sino de intención jurídica entre documentos. |
| **Exportación PDF** | Botón dedicado para generar un informe profesional con firma y sellos institucionales. |
| **Seguridad de Acceso** | Login mediante contraseña corporativa para proteger la confidencialidad. |
| **Diseño Premium 2.0** | Fondo del campus de Medellín con efecto de profundidad y tarjetas translúcidas. |

---

## ⚖️ Marco Normativo Integrado
El Asistente evalúa los documentos bajo la luz de:
- **Constitución Política de Colombia** (Sentencia T-323 de 2024).
- **Código Civil y Código de Comercio de Colombia**.
- **Ley 1480 de 2011** (Estatuto del Consumidor).
- **Reglamento Interno de Contratación de la Universidad EAFIT**.

---
**Documentación generada por el Equipo Antigravity para la Secretaría General de la Universidad EAFIT.**
