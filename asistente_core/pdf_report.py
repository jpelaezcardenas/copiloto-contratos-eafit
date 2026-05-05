"""Generador de reportes PDF profesionales para análisis de contratos EAFIT."""

from fpdf import FPDF
from datetime import datetime
import re

# ── Constantes de layout ──────────────────────────────────────────────────────
L_MARGIN = 10   # margen izquierdo (mm)
R_MARGIN = 10   # margen derecho  (mm)
PAGE_W   = 210  # A4 ancho        (mm)
CONTENT_W = PAGE_W - L_MARGIN - R_MARGIN  # 190 mm disponibles


def _clean(text):
    """Elimina emojis y caracteres no soportados por FPDF."""
    if not text:
        return ""
    subs = {
        '🟢': '[BAJO]', '🟡': '[MOD]', '🔴': '[ALTO]',
        '✅': '[OK]', '❌': '[X]', '⚠️': '[!]', '©': '(c)',
        '—': '-', '–': '-', '→': '->', '•': '-',
    }
    for k, v in subs.items():
        text = text.replace(k, v)
    text = re.sub(r'[\U00010000-\U0010ffff]', '', text)
    return text.strip()


def _fmt(value):
    """Convierte cualquier valor a texto plano."""
    if isinstance(value, list):
        return "; ".join(str(i) for i in value if str(i).strip())
    if isinstance(value, bool):
        return "Si" if value else "No"
    if isinstance(value, dict):
        return " | ".join(f"{k.replace('_',' ').title()}: {_fmt(v)}" for k, v in value.items())
    return str(value)


class _PDF(FPDF):
    """PDF con header/footer institucional EAFIT."""

    def header(self):
        self.set_x(L_MARGIN)
        self.set_font('Helvetica', 'B', 10)
        self.set_text_color(0, 51, 153)
        # Dos células en la misma línea con anchos fijos (total = CONTENT_W)
        self.cell(120, 8, 'UNIVERSIDAD EAFIT - Secretaria General', 0, 0, 'L')
        self.set_font('Helvetica', '', 8)
        self.set_text_color(120, 120, 120)
        self.cell(70, 8, 'Asistente Juridico para Analisis Contractual', 0, 1, 'R')
        self.set_draw_color(0, 51, 153)
        self.set_line_width(0.5)
        self.line(L_MARGIN, 18, PAGE_W - R_MARGIN, 18)
        self.ln(4)

    def footer(self):
        self.set_y(-20)
        self.set_draw_color(200, 200, 200)
        self.set_line_width(0.2)
        self.line(L_MARGIN, self.get_y(), PAGE_W - R_MARGIN, self.get_y())
        self.ln(2)
        self.set_x(L_MARGIN)
        self.set_font('Helvetica', 'I', 7)
        self.set_text_color(150, 150, 150)
        self.cell(CONTENT_W, 4,
                  'Este analisis es de apoyo y no sustituye el criterio del abogado (Sentencia T-323/2024).',
                  0, 1, 'L')
        self.set_x(L_MARGIN)
        self.cell(CONTENT_W, 4,
                  f'Generado el {datetime.now().strftime("%d/%m/%Y %H:%M")} | Pag. {self.page_no()}/{{nb}}',
                  0, 0, 'C')

    # ── Helpers con reset garantizado ────────────────────────────────────────

    def _reset(self):
        """Siempre vuelve al margen izquierdo."""
        self.set_x(L_MARGIN)

    def titulo_seccion(self, txt):
        self._reset()
        self.set_font('Helvetica', 'B', 13)
        self.set_text_color(0, 51, 153)
        self.cell(CONTENT_W, 10, _clean(txt), 0, 1, 'L')
        self._reset()
        self.set_draw_color(0, 51, 153)
        self.set_line_width(0.3)
        self.line(L_MARGIN, self.get_y(), L_MARGIN + 70, self.get_y())
        self.ln(4)

    def titulo_sub(self, txt):
        self._reset()
        self.set_font('Helvetica', 'B', 10)
        self.set_text_color(50, 50, 50)
        self.cell(CONTENT_W, 7, _clean(txt), 0, 1, 'L')
        self.ln(1)

    def parrafo(self, txt):
        self._reset()
        self.set_font('Helvetica', '', 9)
        self.set_text_color(33, 33, 33)
        self.multi_cell(CONTENT_W, 5, _clean(txt))
        self.ln(2)

    def clave_valor(self, key, value):
        self._reset()
        self.set_font('Helvetica', 'B', 9)
        self.set_text_color(80, 80, 80)
        self.cell(55, 6, _clean(key) + ':', 0, 0, 'L')  # 55 mm para la etiqueta
        self.set_font('Helvetica', '', 9)
        self.set_text_color(33, 33, 33)
        val = _clean(_fmt(value))
        # Siempre multi_cell con ancho restante fijo
        self.multi_cell(CONTENT_W - 55, 6, val, 0, 'L')
        self._reset()
        self.ln(1)

    def badge_nivel(self, nivel):
        colores = {
            'ALTO': (220, 53, 69), 'MEDIO': (255, 193, 7),
            'MODERADO': (255, 193, 7), 'BAJO': (40, 167, 69),
        }
        r, g, b = colores.get(nivel.upper(), (150, 150, 150))
        self.set_fill_color(r, g, b)
        tc = (255, 255, 255) if nivel.upper() in ('ALTO', 'BAJO') else (33, 33, 33)
        self.set_text_color(*tc)
        self.set_font('Helvetica', 'B', 8)
        w = self.get_string_width(nivel) + 8
        self.cell(w, 6, nivel, 0, 0, 'C', fill=True)
        self.set_text_color(33, 33, 33)


# ── Función principal ─────────────────────────────────────────────────────────

def generate_pdf_report(data: dict) -> bytes:
    """Genera el reporte PDF institucional EAFIT."""
    pdf = _PDF()
    pdf.alias_nb_pages()
    pdf.set_margins(L_MARGIN, 25, R_MARGIN)
    pdf.set_auto_page_break(auto=True, margin=25)
    pdf.add_page()

    semaforo = data.get('semaforo', 'BAJO').upper()
    label_map = {
        'ALTO':     'RIESGO CRITICO DETECTADO',
        'MODERADO': 'RIESGO MODERADO - REVISION REQUERIDA',
        'MEDIO':    'RIESGO MODERADO - REVISION REQUERIDA',
        'BAJO':     'CONTRATO SEGURO - RIESGOS MINIMOS',
    }
    sem_colors = {
        'ALTO': (220, 53, 69), 'MODERADO': (255, 193, 7),
        'MEDIO': (255, 193, 7), 'BAJO': (40, 167, 69),
    }

    # ── Título principal ──────────────────────────────────────────────────────
    pdf._reset()
    pdf.set_font('Helvetica', 'B', 20)
    pdf.set_text_color(0, 51, 153)
    pdf.cell(CONTENT_W, 12, 'REPORTE DE ANALISIS CONTRACTUAL', 0, 1, 'C')
    pdf._reset()
    pdf.set_font('Helvetica', '', 11)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(CONTENT_W, 7, 'Secretaria General - Universidad EAFIT', 0, 1, 'C')
    pdf.ln(4)

    # ── Semáforo ──────────────────────────────────────────────────────────────
    r, g, b = sem_colors.get(semaforo, (150, 150, 150))
    pdf._reset()
    pdf.set_fill_color(r, g, b)
    tc = (255, 255, 255) if semaforo in ('ALTO', 'BAJO') else (33, 33, 33)
    pdf.set_text_color(*tc)
    pdf.set_font('Helvetica', 'B', 16)
    pdf.cell(CONTENT_W, 12, f'NIVEL DE RIESGO: {semaforo}', 0, 1, 'C', fill=True)
    pdf._reset()
    pdf.set_text_color(100, 100, 100)
    pdf.set_font('Helvetica', '', 9)
    pdf.cell(CONTENT_W, 6, label_map.get(semaforo, ''), 0, 1, 'C')
    pdf.ln(6)

    # ── Concepto jurídico ─────────────────────────────────────────────────────
    pdf.titulo_seccion('Concepto Juridico')
    pdf.parrafo(data.get('resumen_ejecutivo', 'Sin resumen disponible.'))

    # ── Identificación ────────────────────────────────────────────────────────
    pdf.titulo_seccion('Identificacion del Contrato')
    for k, v in data.get('identificacion', {}).items():
        pdf.clave_valor(k.replace('_', ' ').title(), v)
    pdf.ln(3)

    # ── Principios EAFIT ──────────────────────────────────────────────────────
    principios = data.get('evaluacion_principios_eafit', {})
    if principios:
        pdf.titulo_seccion('Evaluacion Principios EAFIT')
        for k, v in principios.items():
            pdf.clave_valor(k.replace('_', ' ').title(), v)
        pdf.ln(3)

    # ── Obligaciones ──────────────────────────────────────────────────────────
    pdf.titulo_seccion('Obligaciones')
    obli = data.get('obligaciones', {})

    for parte, label in [('contratante', 'Del Contratante:'), ('contratista', 'Del Contratista:')]:
        items = obli.get(parte, [])
        if items:
            pdf.titulo_sub(label)
            for o in (items if isinstance(items, list) else [items]):
                pdf._reset()
                pdf.set_x(L_MARGIN + 5)
                pdf.set_font('Helvetica', '', 9)
                pdf.set_text_color(33, 33, 33)
                pdf.multi_cell(CONTENT_W - 5, 5, f'- {_clean(str(o))}')
                pdf._reset()
                pdf.ln(1)

    desequilibrio = obli.get('desequilibrio', obli.get('nota_desequilibrio', ''))
    if desequilibrio and 'no detectado' not in desequilibrio.lower():
        pdf.ln(2)
        pdf._reset()
        pdf.set_font('Helvetica', 'B', 9)
        pdf.set_text_color(220, 53, 69)
        pdf.cell(CONTENT_W, 6, 'ALERTA: Desequilibrio detectado en obligaciones', 0, 1, 'L')
        pdf.parrafo(desequilibrio)
    pdf.ln(3)

    # ── Matriz de riesgos ─────────────────────────────────────────────────────
    pdf.add_page()
    pdf.titulo_seccion('Matriz de Riesgos Detectados')

    riesgos = data.get('riesgos', [])
    if not riesgos:
        pdf.parrafo('No se identificaron riesgos que requieran atencion inmediata.')
    else:
        for i, r_item in enumerate(riesgos, 1):
            nivel = r_item.get('level', r_item.get('nivel', 'BAJO')).upper()
            categoria = _clean(r_item.get('categoria', 'Riesgo').replace('_', ' ').title())

            if pdf.get_y() > 240:
                pdf.add_page()

            # Línea de color lateral
            nc = {'ALTO': (220, 53, 69), 'MEDIO': (255, 193, 7), 'BAJO': (40, 167, 69)}
            rc2, gc2, bc2 = nc.get(nivel, (150, 150, 150))
            pdf.set_draw_color(rc2, gc2, bc2)
            pdf.set_line_width(1)
            y0 = pdf.get_y()
            pdf.line(L_MARGIN, y0, L_MARGIN, y0 + 4)

            # Título del riesgo + badge
            pdf._reset()
            pdf.set_font('Helvetica', 'B', 10)
            pdf.set_text_color(33, 33, 33)
            pdf.cell(CONTENT_W - 30, 6, f'{i}. {categoria}', 0, 0, 'L')
            pdf.badge_nivel(nivel)
            pdf.ln(7)

            # Descripción
            desc = r_item.get('descripcion', '')
            if desc:
                pdf._reset()
                pdf.set_x(L_MARGIN + 5)
                pdf.set_font('Helvetica', '', 9)
                pdf.set_text_color(60, 60, 60)
                pdf.multi_cell(CONTENT_W - 5, 5, _clean(desc))
                pdf._reset()
                pdf.ln(1)

            # Cláusula
            clausula = r_item.get('clausula', r_item.get('clausula_afectada', ''))
            if clausula:
                pdf._reset()
                pdf.set_x(L_MARGIN + 5)
                pdf.set_font('Helvetica', 'I', 8)
                pdf.set_text_color(100, 100, 100)
                pdf.multi_cell(CONTENT_W - 5, 4, f'Clausula: {_clean(clausula)}')
                pdf._reset()
                pdf.ln(1)

            # Referencia legal
            ref = r_item.get('referencia_legal', '')
            if ref:
                pdf._reset()
                pdf.set_x(L_MARGIN + 5)
                pdf.set_font('Helvetica', '', 8)
                pdf.set_text_color(0, 51, 153)
                pdf.multi_cell(CONTENT_W - 5, 4, f'Ref. Legal: {_clean(ref)}')
                pdf._reset()
                pdf.ln(1)

            # Recomendación
            rec = r_item.get('recomendacion', '')
            if rec:
                pdf._reset()
                pdf.set_x(L_MARGIN + 5)
                pdf.set_fill_color(245, 245, 250)
                pdf.set_font('Helvetica', 'B', 8)
                pdf.set_text_color(0, 51, 153)
                pdf.cell(CONTENT_W - 5, 5, 'Recomendacion:', 0, 1, 'L', fill=True)
                pdf._reset()
                pdf.set_x(L_MARGIN + 5)
                pdf.set_font('Helvetica', '', 8)
                pdf.set_text_color(33, 33, 33)
                pdf.multi_cell(CONTENT_W - 5, 4, _clean(rec))
                pdf._reset()

            pdf.ln(5)

    # ── Disclaimer ────────────────────────────────────────────────────────────
    if pdf.get_y() > 250:
        pdf.add_page()
    pdf.ln(6)
    pdf._reset()
    pdf.set_fill_color(240, 240, 245)
    pdf.set_font('Helvetica', 'I', 8)
    pdf.set_text_color(100, 100, 100)
    pdf.multi_cell(CONTENT_W, 4,
        'AVISO LEGAL: Este reporte fue generado por el Asistente Juridico para Analisis '
        'Contractual de la Universidad EAFIT como herramienta de apoyo para la Secretaria '
        'General. Los resultados son orientativos y no constituyen concepto juridico '
        'vinculante. Todo analisis requiere validacion por un profesional del derecho. '
        'Alineado con Sentencia T-323 de 2024 de la Corte Constitucional de Colombia.',
        fill=True
    )

    return bytes(pdf.output())
