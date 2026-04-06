from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

WDI_ZIP_URL = "https://databank.worldbank.org/data/download/WDI_CSV.zip"

RAW_WORLD_BANK_DIR = BASE_DIR / "data" / "raw" / "world-bank"
RAW_WDI_ZIP_PATH = RAW_WORLD_BANK_DIR / "WDI_CSV.zip"
RAW_DATA_DIR = RAW_WORLD_BANK_DIR / "wdi_csv"
PROCESSED_DATA_DIR = BASE_DIR / "data" / "processed"
RAW_WDI_PATH = RAW_DATA_DIR / "WDICSV.csv"
RAW_SERIES_PATH = RAW_DATA_DIR / "WDISeries.csv"
ARGENTINA_TIDY_PATH = PROCESSED_DATA_DIR / "argentina_macro_tidy.csv"
ARGENTINA_SNAPSHOT_PATH = PROCESSED_DATA_DIR / "argentina_latest_snapshot.csv"

APP_TITLE = "Argentina Economic Dashboard"
APP_SUBTITLE = (
    "Macroeconomic Stability, Trade and Openness, Crisis and Recovery (2000-2024)"
)
SOURCE_LABEL = "Source: World Bank World Development Indicators"

COUNTRY_CODE = "ARG"
COUNTRY_NAME = "Argentina"
START_YEAR = 2000
END_YEAR = 2024
YEAR_COLUMNS = [str(year) for year in range(START_YEAR, END_YEAR + 1)]

THEME_ORDER = [
    "Macroeconomic Stability",
    "Trade and Openness",
    "External Sector and Recovery",
]

THEMES = {
    "dark": {
        "background": "#0B1020",
        "panel": "#121A2B",
        "panel_alt": "#172033",
        "border": "#2A3754",
        "text": "#E8EEF9",
        "muted_text": "#9FB0D0",
        "grid": "#23314D",
        "shadow": "0 18px 26px rgba(0, 0, 0, 0.15)",
        "card_shadow": "0 14px 24px rgba(0, 0, 0, 0.18)",
        "accent": "#8FB8FF",
    },
    "light": {
        "background": "#F3F6FB",
        "panel": "#FFFFFF",
        "panel_alt": "#E9EEF8",
        "border": "#CDD8EC",
        "text": "#18243D",
        "muted_text": "#2b2e33",
        "grid": "#D7E0EF",
        "shadow": "0 12px 24px rgba(23, 36, 61, 0.10)",
        "card_shadow": "0 10px 18px rgba(23, 36, 61, 0.08)",
        "accent": "#245DFF",
    },
}

SERIES_COLORS = {
    "gdp_growth": "#4DA3FF",
    "gdp_usd": "#74C0FC",
    "inflation": "#FF8A4C",
    "unemployment": "#FFD166",
    "exports": "#2EC4B6",
    "imports": "#7B9ACC",
    "fdi": "#7AE582",
    "current_account": "#FF5D73",
}

SERIES_COLORS_LIGHT = {
    "gdp_growth": "#0A5BC4",
    "gdp_usd": "#006DAD",
    "inflation": "#CC4B00",
    "unemployment": "#9A6700",
    "exports": "#0D8B78",
    "imports": "#4E68C7",
    "fdi": "#2D8A34",
    "current_account": "#BE245A",
}

COLOR_PALETTE = THEMES["dark"] | SERIES_COLORS

FONT_FAMILY = "IBM Plex Sans, Segoe UI, sans-serif"
FONT_MONO = "IBM Plex Mono, Consolas, monospace"

CHART_HEIGHTS = {
    "kpi": 130,
    "standard": 360,
    "tall": 430,
}

INDICATORS = {
    "NY.GDP.MKTP.KD.ZG": {
        "name": "GDP growth (annual %)",
        "topic": "Macroeconomic Stability",
        "unit": "%",
        "color": SERIES_COLORS["gdp_growth"],
        "short_label": "GDP growth",
    },
    "NY.GDP.MKTP.CD": {
        "name": "GDP (current US$)",
        "topic": "Macroeconomic Stability",
        "unit": "current US$",
        "color": SERIES_COLORS["gdp_usd"],
        "short_label": "GDP (current US$)",
    },
    "NY.GDP.DEFL.KD.ZG": {
        "name": "Inflation, GDP deflator (annual %)",
        "topic": "Macroeconomic Stability",
        "unit": "%",
        "color": SERIES_COLORS["inflation"],
        "short_label": "Inflation (GDP deflator)",
    },
    "SL.UEM.TOTL.ZS": {
        "name": "Unemployment, total (% of total labor force)",
        "topic": "Macroeconomic Stability",
        "unit": "%",
        "color": SERIES_COLORS["unemployment"],
        "short_label": "Unemployment",
    },
    "NE.EXP.GNFS.ZS": {
        "name": "Exports of goods and services (% of GDP)",
        "topic": "Trade and Openness",
        "unit": "% of GDP",
        "color": SERIES_COLORS["exports"],
        "short_label": "Exports",
    },
    "NE.IMP.GNFS.ZS": {
        "name": "Imports of goods and services (% of GDP)",
        "topic": "Trade and Openness",
        "unit": "% of GDP",
        "color": SERIES_COLORS["imports"],
        "short_label": "Imports",
    },
    "BX.KLT.DINV.WD.GD.ZS": {
        "name": "Foreign direct investment, net inflows (% of GDP)",
        "topic": "External Sector and Recovery",
        "unit": "% of GDP",
        "color": SERIES_COLORS["fdi"],
        "short_label": "FDI",
    },
    "BN.CAB.XOKA.GD.ZS": {
        "name": "Current account balance (% of GDP)",
        "topic": "External Sector and Recovery",
        "unit": "% of GDP",
        "color": SERIES_COLORS["current_account"],
        "short_label": "Current account",
    },
}

INDICATOR_ORDER = list(INDICATORS.keys())

KPI_INDICATORS = [
    "NY.GDP.MKTP.KD.ZG",
    "NY.GDP.DEFL.KD.ZG",
    "SL.UEM.TOTL.ZS",
    "NE.EXP.GNFS.ZS",
    "NE.IMP.GNFS.ZS",
    "BX.KLT.DINV.WD.GD.ZS",
]
