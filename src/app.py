from pathlib import Path

from dash import Dash, Input, Output, State, dcc, html

import pandas as pd

from src.config import ARGENTINA_SNAPSHOT_PATH, ARGENTINA_TIDY_PATH, FONT_FAMILY, THEMES
from src.init_data import save_processed_datasets
from src.layout import build_layout


def load_or_build_processed_data() -> tuple[pd.DataFrame, pd.DataFrame]:
    if not ARGENTINA_TIDY_PATH.exists() or not ARGENTINA_SNAPSHOT_PATH.exists():
        save_processed_datasets()
    tidy_df = pd.read_csv(ARGENTINA_TIDY_PATH)
    snapshot_df = pd.read_csv(ARGENTINA_SNAPSHOT_PATH)
    return tidy_df, snapshot_df


tidy_data, snapshot_data = load_or_build_processed_data()
ASSETS_DIR = Path(__file__).resolve().parent.parent / "assets"

app = Dash(__name__, assets_folder=str(ASSETS_DIR))
app.title = "Economic Dashboard of Argentina"
app.layout = html.Div(
    [
        dcc.Store(id="theme-store", data="light"),
        html.Div(
            children=html.Button(
                "\u263E",
                id="theme-switcher",
                className="theme-toggle-button",
                title="Switch theme",
                n_clicks=0,
                style={
                    "width": "23px",
                    "height": "23px",
                    "borderRadius": "999px",
                    "border": "none",
                    "fontSize": "0.7rem",
                    "cursor": "pointer",
                    "display": "flex",
                    "alignItems": "center",
                    "justifyContent": "center",
                    "padding": 0,
                },
            ),
            id="theme-switcher-panel",
            style={
                "position": "fixed",
                "top": "1rem",
                "right": "1rem",
                "zIndex": 10,
                "padding": "0.2rem",
                "borderRadius": "999px",
                "fontFamily": FONT_FAMILY,
            },
        ),
        html.Div(id="dashboard-container"),
    ],
    id="app-shell",
    style={"fontFamily": FONT_FAMILY},
)

server = app.server


@app.callback(
    Output("theme-store", "data"),
    Input("theme-switcher", "n_clicks"),
    State("theme-store", "data"),
    prevent_initial_call=True,
)
def toggle_theme(_n_clicks: int, current_theme: str):
    return "dark" if current_theme == "light" else "light"


@app.callback(
    Output("dashboard-container", "children"),
    Output("app-shell", "style"),
    Output("theme-switcher-panel", "style"),
    Output("theme-switcher", "children"),
    Output("theme-switcher", "style"),
    Input("theme-store", "data"),
)
def update_theme(theme: str):
    palette = THEMES.get(theme, THEMES["dark"])
    shell_style = {
        "fontFamily": FONT_FAMILY,
        "backgroundColor": palette["background"],
        "minHeight": "100vh",
        "overflow": "auto",
    }
    switcher_style = {
        "position": "fixed",
        "top": "1rem",
        "right": "1rem",
        "zIndex": 10,
        "padding": "0.2rem",
        "borderRadius": "999px",
        "fontFamily": FONT_FAMILY,
        "backgroundColor": palette["panel"],
        "border": f"1px solid {palette['border']}",
        "boxShadow": palette["card_shadow"],
        "color": palette["text"],
    }
    button_style = {
        "width": "23px",
        "height": "23px",
        "borderRadius": "999px",
        "border": "none",
        "cursor": "pointer",
        "display": "flex",
        "alignItems": "center",
        "justifyContent": "center",
        "padding": 0,
        "backgroundColor": palette["panel_alt"],
        "color": palette["text"],
    }
    icon = "\u263E" if theme == "light" else "\u2600"
    return (
        build_layout(tidy_data, snapshot_data, theme),
        shell_style,
        switcher_style,
        icon,
        button_style,
    )


if __name__ == "__main__":
    app.run(debug=True)
