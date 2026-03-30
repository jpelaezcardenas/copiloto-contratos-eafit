"""Módulo de detección y clasificación de riesgos legales."""

from config.settings import RISK_CATEGORIES


def classify_risk_level(semaforo: str) -> dict:
    """Devuelve la información visual del semáforo de riesgo.

    Args:
        semaforo: Nivel del semáforo (BAJO, MODERADO, ALTO).

    Returns:
        dict con color, emoji, label y descripción.
    """
    levels = {
        "BAJO": {
            "color": "#10b981",
            "bg_color": "rgba(16, 185, 129, 0.15)",
            "border_color": "rgba(16, 185, 129, 0.3)",
            "emoji": "🟢",
            "label": "Riesgo Bajo",
            "description": "Contrato sólido con riesgos menores.",
        },
        "MODERADO": {
            "color": "#f59e0b",
            "bg_color": "rgba(245, 158, 11, 0.15)",
            "border_color": "rgba(245, 158, 11, 0.3)",
            "emoji": "🟡",
            "label": "Riesgo Moderado",
            "description": "Requiere revisión en algunos puntos clave.",
        },
        "ALTO": {
            "color": "#ef4444",
            "bg_color": "rgba(239, 68, 68, 0.15)",
            "border_color": "rgba(239, 68, 68, 0.3)",
            "emoji": "🔴",
            "label": "Riesgo Alto",
            "description": "Requiere atención inmediata. Riesgos críticos detectados.",
        },
    }
    return levels.get(semaforo, levels["MODERADO"])


def get_risk_stats(risks: list) -> dict:
    """Calcula estadísticas de los riesgos detectados.

    Args:
        risks: Lista de riesgos del análisis.

    Returns:
        dict con conteos por nivel y categoría.
    """
    stats = {
        "total": len(risks),
        "por_nivel": {"ALTO": 0, "MEDIO": 0, "BAJO": 0, "NO_APLICA": 0},
        "por_categoria": {},
        "criticos": [],
    }

    for risk in risks:
        nivel = risk.get("nivel", "MEDIO")
        categoria = risk.get("categoria", "otro")

        stats["por_nivel"][nivel] = stats["por_nivel"].get(nivel, 0) + 1
        stats["por_categoria"][categoria] = stats["por_categoria"].get(categoria, 0) + 1

        if nivel == "ALTO":
            stats["criticos"].append(risk)

    return stats


def get_risk_category_info(categoria: str) -> dict:
    """Obtiene la información de una categoría de riesgo.

    Args:
        categoria: Clave de la categoría.

    Returns:
        dict con la información de la categoría.
    """
    return RISK_CATEGORIES.get(
        categoria,
        {
            "label": categoria.replace("_", " ").title(),
            "icon": "⚪",
            "description": "",
            "referencia": "",
        },
    )


def get_risk_nivel_badge(nivel: str) -> str:
    """Devuelve un badge HTML para el nivel de riesgo."""
    colors = {
        "ALTO": ("#ef4444", "#fee2e2"),
        "MEDIO": ("#f59e0b", "#fef3c7"),
        "BAJO": ("#10b981", "#d1fae5"),
        "NO_APLICA": ("#6b7280", "#f3f4f6"),
    }
    text_color, bg_color = colors.get(nivel, ("#6b7280", "#f3f4f6"))
    return (
        f'<span style="background:{bg_color}; color:{text_color}; '
        f'padding:2px 10px; border-radius:12px; font-size:0.8em; '
        f'font-weight:600;">{nivel}</span>'
    )
