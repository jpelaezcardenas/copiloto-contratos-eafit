"""Extracción de texto de documentos PDF.

Usa PyMuPDF para texto general y pdfplumber para tablas.
Incluye sanitización anti prompt-injection.
"""

import fitz  # PyMuPDF
import pdfplumber
import re
from typing import Optional


def extract_text_from_pdf(pdf_bytes: bytes) -> dict:
    """Extrae texto y tablas de un PDF.

    Args:
        pdf_bytes: Contenido del PDF en bytes.

    Returns:
        dict con 'text' (texto completo), 'pages' (lista de textos por página),
        'tables' (tablas encontradas), 'metadata' (metadatos del PDF),
        'page_count' (número de páginas).
    """
    result = {
        "text": "",
        "pages": [],
        "tables": [],
        "metadata": {},
        "page_count": 0,
    }

    # ── Extracción con PyMuPDF (texto general) ────────────
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    result["page_count"] = len(doc)
    result["metadata"] = {
        "title": doc.metadata.get("title", ""),
        "author": doc.metadata.get("author", ""),
        "creation_date": doc.metadata.get("creationDate", ""),
    }

    page_texts = []
    for page in doc:
        text = page.get_text("text")
        page_texts.append(text)
    doc.close()

    result["pages"] = page_texts
    result["text"] = "\n\n".join(page_texts)

    # ── Extracción de tablas con pdfplumber ────────────────
    try:
        with pdfplumber.open(stream=pdf_bytes) as pdf:
            for i, page in enumerate(pdf.pages):
                tables = page.extract_tables()
                for table in tables:
                    if table:
                        result["tables"].append(
                            {"page": i + 1, "data": table}
                        )
    except Exception:
        pass  # Si falla pdfplumber, al menos tenemos el texto de PyMuPDF

    return result


def sanitize_extracted_text(text: str) -> str:
    """Limpia texto extraído para prevenir prompt injection.

    Elimina:
    - Caracteres de control invisibles
    - Secuencias sospechosas que podrían ser instrucciones ocultas
    - Texto en fuente de tamaño 0 o colores blancos (no aplica al texto plano)
    """
    # Eliminar caracteres de control Unicode (excepto newlines y tabs)
    text = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\x9f]", "", text)

    # Eliminar secuencias de zero-width characters
    text = re.sub(r"[\u200b\u200c\u200d\u200e\u200f\ufeff]", "", text)

    # Detectar y marcar posibles instrucciones inyectadas
    injection_patterns = [
        r"(?i)ignor[ae]\s+(todas?\s+)?las?\s+instrucciones?",
        r"(?i)ignore\s+(all\s+)?(previous\s+)?instructions?",
        r"(?i)olvida\s+todo\s+lo\s+anterior",
        r"(?i)forget\s+(all\s+)?previous",
        r"(?i)system\s*prompt",
        r"(?i)new\s+instructions?:",
        r"(?i)override\s+mode",
    ]

    for pattern in injection_patterns:
        if re.search(pattern, text):
            text = re.sub(
                pattern,
                "[⚠️ CONTENIDO SOSPECHOSO ELIMINADO]",
                text,
            )

    # Normalizar espacios blancos excesivos
    text = re.sub(r"\n{4,}", "\n\n\n", text)
    text = re.sub(r" {3,}", "  ", text)

    return text.strip()


def get_document_summary(extraction: dict) -> str:
    """Genera un resumen rápido del documento extraído."""
    text = extraction["text"]
    word_count = len(text.split())
    table_count = len(extraction["tables"])

    return (
        f"📄 **Documento procesado**\n"
        f"- Páginas: {extraction['page_count']}\n"
        f"- Palabras: {word_count:,}\n"
        f"- Tablas encontradas: {table_count}\n"
    )
