"""Generador de reportes PDF profesionales para análisis de contratos EAFIT."""

from fpdf import FPDF
from datetime import datetime
import re


def _clean_text(text):
    """Limpia texto de emojis y caracteres no soportados por PDF."""
    if not text:
        return ""
    # Reemplazar emojis comunes con texto
    replacements = {
        '🟢': '[BAJO]', '🟡': '[MODERADO]', '🔴': '[ALTO]',
        '✅': '[OK]', '❌': '[X]', '⚠️': '[!]', '⚖️': '',
        '📄': '', '📋': '', '🔍': '', '📝': '', '🧠': '',
        '📊': '', '📥': '', '🕒': '', '🏗️': '', '✨': '',
        '🎯': '', '🛡️': '', '💡': '', '🐍': '', '☁️': '',
        '🌐': '', '©': '(c)', '—': '-', '–': '-',
    }
    for emoji, replacement in replacements.items():
        text = text.replace(emoji, replacement)
    # Eliminar emojis restantes (rangos Unicode)
    text = re.sub(r'[\U00010000-\U0010ffff]', '', text)
    return text.strip()


def _format_value(value):
    """Convierte valores complejos a texto plano."""
    if isinstance(value, list):
        return ", ".join([str(i) for i in value if str(i).strip()])
    if isinstance(value, bool):
        return "Si" if value else "No"
    if isinstance(value, dict):
        parts = []
        for k, v in value.items():
            k_clean = k.replace('_', ' ').title()
            v_clean = _format_value(v)
            parts.append(f"{k_clean}: {v_clean}")
        return " | ".join(parts)
    return str(value)


class ContractReportPDF(FPDF):
    """PDF personalizado con header/footer institucional EAFIT."""

    def header(self):
        self.set_font('Helvetica', 'B', 10)
        self.set_text_color(0, 51, 153)
        self.cell(0, 8, 'UNIVERSIDAD EAFIT - Secretaria General', 0, 0, 'L')
        self.set_font('Helvetica', '', 8)
        self.set_text_color(120, 120, 120)
        self.cell(0, 8, 'Copiloto Juridico Inteligente', 0, 1, 'R')
        self.set_draw_color(0, 51, 153)
        self.set_line_width(0.5)
        self.line(10, 18, 200, 18)
        self.ln(6)

    def footer(self):
        self.set_y(-20)
        self.set_draw_color(200, 200, 200)
        self.set_line_width(0.2)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(3)
        self.set_font('Helvetica', 'I', 7)
        self.set_text_color(150, 150, 150)
        self.cell(0, 5, 'Este analisis es de apoyo y no sustituye el criterio del abogado (Sentencia T-323/2024).', 0, 1, 'L')
        self.cell(0, 5, f'Generado el {datetime.now().strftime("%d/%m/%Y %H:%M")} | Pagina {self.page_no()}/{{nb}}', 0, 0, 'C')

    def section_title(self, title):
        self.set_font('Helvetica', 'B', 13)
        self.set_text_color(0, 51, 153)
        self.cell(0, 10, _clean_text(title), 0, 1, 'L')
        self.set_draw_color(0, 51, 153)
        self.set_line_width(0.3)
        self.line(10, self.get_y(), 80, self.get_y())
        self.ln(4)

    def subsection_title(self, title):
        self.set_font('Helvetica', 'B', 10)
        self.set_text_color(50, 50, 50)
        self.cell(0, 7, _clean_text(title), 0, 1, 'L')
        self.ln(1)

    def body_text(self, text):
        self.set_font('Helvetica', '', 9)
        self.set_text_color(33, 33, 33)
        self.multi_cell(0, 5, _clean_text(text))
        self.ln(2)

    def key_value(self, key, value):
        self.set_font('Helvetica', 'B', 9)
        self.set_text_color(80, 80, 80)
        self.cell(55, 6, _clean_text(key) + ':', 0, 0, 'L')
        self.set_font('Helvetica', '', 9)
        self.set_text_color(33, 33, 33)
        val_text = _clean_text(_format_value(value))
        if len(val_text) > 80:
            self.ln()
            self.set_x(20)
            self.multi_cell(170, 5, val_text)
        else:
            self.cell(0, 6, val_text, 0, 1, 'L')

    def risk_badge(self, level):
        colors = {
            'ALTO': (220, 53, 69), 'MEDIO': (255, 193, 7),
            'MODERADO': (255, 193, 7), 'BAJO': (40, 167, 69),
            'NO_APLICA': (150, 150, 150)
        }
        r, g, b = colors.get(level.upper(), (150, 150, 150))
        self.set_fill_color(r, g, b)
        text_color = (255, 255, 255) if level.upper() in ['ALTO', 'BAJO'] else (33, 33, 33)
        self.set_text_color(*text_color)
        self.set_font('Helvetica', 'B', 8)
        badge_w = self.get_string_width(level) + 8
        self.cell(badge_w, 6, level, 0, 0, 'C', fill=True)
        self.set_text_color(33, 33, 33)


def generate_pdf_report(data: dict) -> bytes:
    """Genera un reporte PDF profesional a partir de los datos de análisis."""
    pdf = ContractReportPDF()
    pdf.alias_nb_pages()
    pdf.add_page()

    # ── TITULO PRINCIPAL ──
    pdf.set_font('Helvetica', 'B', 20)
    pdf.set_text_color(0, 51, 153)
    pdf.cell(0, 12, 'REPORTE DE ANALISIS LEGAL', 0, 1, 'C')
    pdf.set_font('Helvetica', '', 11)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 7, 'Secretaria General - Universidad EAFIT', 0, 1, 'C')
    pdf.ln(3)

    # ── SEMAFORO ──
    semaforo = data.get('semaforo', 'BAJO').upper()
    label_map = {
        'ALTO': 'RIESGO CRITICO DETECTADO',
        'MODERADO': 'RIESGO MODERADO - REVISION REQUERIDA',
        'MEDIO': 'RIESGO MODERADO - REVISION REQUERIDA',
        'BAJO': 'CONTRATO SEGURO - RIESGOS MINIMOS'
    }
    colors = {'ALTO': (220, 53, 69), 'MODERADO': (255, 193, 7), 'MEDIO': (255, 193, 7), 'BAJO': (40, 167, 69)}
    r, g, b = colors.get(semaforo, (150, 150, 150))

    pdf.set_fill_color(r, g, b)
    text_c = (255, 255, 255) if semaforo in ['ALTO', 'BAJO'] else (33, 33, 33)
    pdf.set_text_color(*text_c)
    pdf.set_font('Helvetica', 'B', 16)
    pdf.cell(0, 12, f'NIVEL DE RIESGO: {semaforo}', 0, 1, 'C', fill=True)
    pdf.set_text_color(100, 100, 100)
    pdf.set_font('Helvetica', '', 9)
    pdf.cell(0, 6, label_map.get(semaforo, ''), 0, 1, 'C')
    pdf.ln(6)

    # ── RESUMEN EJECUTIVO ──
    pdf.section_title('Concepto Juridico')
    pdf.body_text(data.get('resumen_ejecutivo', 'Sin resumen disponible.'))

    # ── IDENTIFICACIÓN ──
    pdf.section_title('Identificacion del Contrato')
    ident = data.get('identificacion', {})
    for k, v in ident.items():
        key_clean = k.replace('_', ' ').title()
        pdf.key_value(key_clean, v)
    pdf.ln(3)

    # ── EVALUACIÓN PRINCIPIOS EAFIT ──
    principios = data.get('evaluacion_principios_eafit', {})
    if principios:
        pdf.section_title('Evaluacion Principios EAFIT')
        for k, v in principios.items():
            key_clean = k.replace('_', ' ').title()
            pdf.key_value(key_clean, v)
        pdf.ln(3)

    # ── OBLIGACIONES ──
    pdf.section_title('Obligaciones')
    obli = data.get('obligaciones', {})

    contratante_obli = obli.get('contratante', [])
    if contratante_obli:
        pdf.subsection_title('Del Contratante:')
        for o in (contratante_obli if isinstance(contratante_obli, list) else [contratante_obli]):
            pdf.set_font('Helvetica', '', 9)
            pdf.set_text_color(33, 33, 33)
            pdf.set_x(15)
            pdf.multi_cell(180, 5, f'  - {_clean_text(str(o))}')

    contratista_obli = obli.get('contratista', [])
    if contratista_obli:
        pdf.subsection_title('Del Contratista:')
        for o in (contratista_obli if isinstance(contratista_obli, list) else [contratista_obli]):
            pdf.set_font('Helvetica', '', 9)
            pdf.set_text_color(33, 33, 33)
            pdf.set_x(15)
            pdf.multi_cell(180, 5, f'  - {_clean_text(str(o))}')

    if obli.get('hay_desequilibrio'):
        pdf.ln(2)
        pdf.set_font('Helvetica', 'B', 9)
        pdf.set_text_color(220, 53, 69)
        pdf.cell(0, 6, 'ALERTA: Desequilibrio detectado en obligaciones', 0, 1)
        pdf.body_text(obli.get('nota_desequilibrio', ''))
    pdf.ln(3)

    # ── MATRIZ DE RIESGOS ──
    pdf.add_page()
    pdf.section_title('Matriz de Riesgos Detectados')

    riesgos = data.get('riesgos', [])
    if not riesgos:
        pdf.body_text('No se identificaron riesgos que requieran atencion inmediata.')
    else:
        for i, r in enumerate(riesgos, 1):
            nivel = r.get('level', r.get('nivel', 'BAJO')).upper()
            categoria = r.get('categoria', 'Riesgo').replace('_', ' ').title()

            # Verificar espacio en página
            if pdf.get_y() > 240:
                pdf.add_page()

            # Línea de color por nivel
            nivel_colors = {'ALTO': (220, 53, 69), 'MEDIO': (255, 193, 7), 'BAJO': (40, 167, 69)}
            rc, gc, bc = nivel_colors.get(nivel, (150, 150, 150))
            pdf.set_draw_color(rc, gc, bc)
            pdf.set_line_width(1)
            y_start = pdf.get_y()
            pdf.line(10, y_start, 10, y_start + 4)

            # Header del riesgo
            pdf.set_font('Helvetica', 'B', 10)
            pdf.set_text_color(33, 33, 33)
            pdf.cell(150, 6, f'{i}. {_clean_text(categoria)}', 0, 0)
            pdf.risk_badge(nivel)
            pdf.ln(7)

            # Descripción
            desc = r.get('descripcion', '')
            if desc:
                pdf.set_font('Helvetica', '', 9)
                pdf.set_text_color(60, 60, 60)
                pdf.set_x(15)
                pdf.multi_cell(180, 5, _clean_text(desc))

            # Cláusula afectada
            clausula = r.get('clausula_afectada', '')
            if clausula:
                pdf.set_font('Helvetica', 'I', 8)
                pdf.set_text_color(100, 100, 100)
                pdf.set_x(15)
                pdf.multi_cell(180, 4, f'Clausula: {_clean_text(clausula)}')

            # Referencia legal
            ref = r.get('referencia_legal', '')
            if ref:
                pdf.set_font('Helvetica', '', 8)
                pdf.set_text_color(0, 51, 153)
                pdf.set_x(15)
                pdf.cell(0, 5, f'Ref. Legal: {_clean_text(ref)}', 0, 1)

            # Recomendación
            rec = r.get('recomendacion', '')
            if rec:
                pdf.set_fill_color(245, 245, 250)
                pdf.set_font('Helvetica', 'B', 8)
                pdf.set_text_color(0, 51, 153)
                pdf.set_x(15)
                pdf.cell(180, 5, 'Recomendacion:', 0, 1, fill=True)
                pdf.set_font('Helvetica', '', 8)
                pdf.set_text_color(33, 33, 33)
                pdf.set_x(15)
                pdf.multi_cell(180, 4, _clean_text(rec))

            pdf.ln(5)

    # ── NOTAS ADICIONALES ──
    notas = data.get('notas_adicionales', '')
    if notas:
        if pdf.get_y() > 250:
            pdf.add_page()
        pdf.section_title('Notas Adicionales')
        pdf.body_text(notas)

    # ── DISCLAIMER FINAL ──
    if pdf.get_y() > 250:
        pdf.add_page()
    pdf.ln(8)
    pdf.set_fill_color(240, 240, 245)
    pdf.set_font('Helvetica', 'I', 8)
    pdf.set_text_color(100, 100, 100)
    pdf.multi_cell(0, 4,
        'AVISO LEGAL: Este reporte fue generado por el Copiloto Juridico Inteligente de la '
        'Universidad EAFIT como herramienta de apoyo para la Secretaria General. '
        'Los resultados son orientativos y no constituyen concepto juridico vinculante. '
        'Todo analisis requiere validacion por un profesional del derecho. '
        'Alineado con Sentencia T-323 de 2024 de la Corte Constitucional de Colombia.',
        fill=True
    )

    return pdf.output()
