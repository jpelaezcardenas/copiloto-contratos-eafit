"""Estilos CSS personalizados para la interfaz Streamlit."""


def get_custom_css() -> str:
    """Retorna el CSS personalizado para la aplicación."""
    return """
    <style>
    /* ── Google Font ─────────────────────────────────── */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

    /* ── Global ──────────────────────────────────────── */
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    .stApp {
        background: linear-gradient(135deg, #0f0f1a 0%, #1a1a2e 50%, #16213e 100%);
    }

    /* ── Header ──────────────────────────────────────── */
    .main-header {
        text-align: center;
        padding: 2rem 0 1rem;
        margin-bottom: 1.5rem;
    }

    .main-header h1 {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.8rem;
        font-weight: 800;
        margin-bottom: 0.3rem;
        letter-spacing: -0.03em;
    }

    .main-header p {
        color: #94a3b8;
        font-size: 1.1rem;
        font-weight: 300;
    }

    /* ── Cards ────────────────────────────────────────── */
    .glass-card {
        background: rgba(255, 255, 255, 0.04);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        transition: all 0.3s ease;
    }

    .glass-card:hover {
        border-color: rgba(102, 126, 234, 0.3);
        box-shadow: 0 8px 32px rgba(102, 126, 234, 0.1);
        transform: translateY(-1px);
    }

    .glass-card h3 {
        color: #e2e8f0;
        font-weight: 600;
        margin-bottom: 0.8rem;
        font-size: 1.1rem;
    }

    .glass-card p, .glass-card li {
        color: #94a3b8;
        font-size: 0.9rem;
        line-height: 1.6;
    }

    /* ── Semáforo ─────────────────────────────────────── */
    .semaforo-container {
        text-align: center;
        padding: 2rem;
        border-radius: 20px;
        margin: 1rem 0;
    }

    .semaforo-emoji {
        font-size: 4rem;
        margin-bottom: 0.5rem;
    }

    .semaforo-label {
        font-size: 1.5rem;
        font-weight: 700;
        margin-bottom: 0.3rem;
    }

    .semaforo-desc {
        font-size: 0.95rem;
        opacity: 0.8;
    }

    /* ── Risk Cards ───────────────────────────────────── */
    .risk-card {
        background: rgba(255, 255, 255, 0.03);
        border-left: 4px solid;
        border-radius: 0 12px 12px 0;
        padding: 1.2rem 1.5rem;
        margin-bottom: 0.8rem;
    }

    .risk-card.alto { border-left-color: #ef4444; }
    .risk-card.medio { border-left-color: #f59e0b; }
    .risk-card.bajo { border-left-color: #10b981; }

    .risk-card .risk-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 0.5rem;
    }

    .risk-card .risk-title {
        color: #e2e8f0;
        font-weight: 600;
        font-size: 1rem;
    }

    .risk-card .risk-desc {
        color: #94a3b8;
        font-size: 0.88rem;
        line-height: 1.5;
        margin-bottom: 0.5rem;
    }

    .risk-card .risk-ref {
        color: #667eea;
        font-size: 0.8rem;
        font-style: italic;
    }

    .risk-card .risk-rec {
        background: rgba(102, 126, 234, 0.1);
        border-radius: 8px;
        padding: 0.6rem 1rem;
        color: #a5b4fc;
        font-size: 0.85rem;
        margin-top: 0.5rem;
    }

    /* ── Metrics ──────────────────────────────────────── */
    .metric-row {
        display: flex;
        gap: 1rem;
        margin-bottom: 1rem;
    }

    .metric-card {
        flex: 1;
        background: rgba(255, 255, 255, 0.04);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 14px;
        padding: 1.2rem;
        text-align: center;
    }

    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea, #764ba2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .metric-label {
        color: #94a3b8;
        font-size: 0.8rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-top: 0.3rem;
    }

    /* ── Info Section ─────────────────────────────────── */
    .info-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 0.8rem;
    }

    .info-item {
        background: rgba(255, 255, 255, 0.03);
        border-radius: 10px;
        padding: 0.8rem 1rem;
    }

    .info-label {
        color: #64748b;
        font-size: 0.75rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 0.2rem;
    }

    .info-value {
        color: #e2e8f0;
        font-size: 0.95rem;
        font-weight: 500;
    }

    /* ── Upload Area ──────────────────────────────────── */
    .upload-area {
        background: rgba(102, 126, 234, 0.05);
        border: 2px dashed rgba(102, 126, 234, 0.3);
        border-radius: 20px;
        padding: 3rem 2rem;
        text-align: center;
        transition: all 0.3s ease;
    }

    .upload-area:hover {
        border-color: rgba(102, 126, 234, 0.6);
        background: rgba(102, 126, 234, 0.08);
    }

    .upload-icon {
        font-size: 3rem;
        margin-bottom: 1rem;
    }

    .upload-text {
        color: #94a3b8;
        font-size: 1rem;
    }

    /* ── Disclaimer ───────────────────────────────────── */
    .disclaimer {
        background: rgba(245, 158, 11, 0.08);
        border: 1px solid rgba(245, 158, 11, 0.2);
        border-radius: 12px;
        padding: 1rem 1.5rem;
        margin-top: 2rem;
        margin-bottom: 1rem;
    }

    .disclaimer p {
        color: #fbbf24;
        font-size: 0.8rem;
        line-height: 1.5;
        margin: 0;
    }

    /* ── Sidebar Styling ─────────────────────────────── */
    section[data-testid="stSidebar"] {
        background: rgba(15, 15, 26, 0.95);
        border-right: 1px solid rgba(255, 255, 255, 0.06);
    }

    /* ── Animations ───────────────────────────────────── */
    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }

    .animate-in {
        animation: fadeInUp 0.5s ease-out;
    }

    /* ── Streamlit Overrides ──────────────────────────── */
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.6rem 2rem;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
        width: 100%;
    }

    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.35);
    }

    .stFileUploader {
        border-radius: 16px;
    }

    div[data-testid="stExpander"] {
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid rgba(255, 255, 255, 0.06);
        border-radius: 12px;
    }

    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }

    .stTabs [data-baseweb="tab"] {
        background: rgba(255, 255, 255, 0.04);
        border-radius: 10px 10px 0 0;
        border: 1px solid rgba(255, 255, 255, 0.06);
        color: #94a3b8;
        padding: 0.5rem 1.5rem;
    }

    .stTabs [aria-selected="true"] {
        background: rgba(102, 126, 234, 0.15);
        border-color: rgba(102, 126, 234, 0.3);
        color: #a5b4fc;
    }

    /* ── Spinner ──────────────────────────────────────── */
    .analyzing-container {
        text-align: center;
        padding: 3rem;
    }

    .analyzing-container .pulse {
        display: inline-block;
        animation: pulse 1.5s ease-in-out infinite;
    }

    @keyframes pulse {
        0%, 100% { transform: scale(1); opacity: 1; }
        50% { transform: scale(1.1); opacity: 0.7; }
    }
    </style>
    """
