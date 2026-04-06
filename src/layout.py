from __future__ import annotations

from dash import dcc, html

from charts import (
    build_bubble_chart,
    build_gdp_area,
    build_gdp_growth_line,
    build_heatmap,
    build_inflation_unemployment_chart,
    build_kpi_records,
    build_latest_position_chart,
    build_trade_chart,
)
from src.config import APP_SUBTITLE, APP_TITLE, FONT_FAMILY, FONT_MONO, SOURCE_LABEL, THEMES


def get_palette(theme: str) -> dict:
    return THEMES.get(theme, THEMES["dark"])


def build_kpi_card(record: dict, theme: str) -> html.Div:
    palette = get_palette(theme)
    unit_label = record["unit"].replace("annual ", "").strip()
    direction_colors = {
        "up": "#2D8A34" if theme == "light" else "#7AE582",
        "down": "#BE245A" if theme == "light" else "#FF5D73",
        "flat": palette["muted_text"],
    }
    return html.Div(
        [
            html.Div(record["label"], style={"color": palette["text"], "fontWeight": "600", "fontSize": "1.1rem"}),
            html.Div(
                [
                    html.Span(record["value"]),
                    html.Span(
                        f" {unit_label}",
                        style={
                            "color": palette["muted_text"],
                            "fontSize": "0.90rem",
                            "fontFamily": FONT_FAMILY,
                            "fontWeight": "500",
                            "marginLeft": "0.25rem",
                        },
                    ),
                ],
                style={
                    "color": record["color"],
                    "fontSize": "2rem",
                    "fontFamily": FONT_MONO,
                    "fontWeight": "700",
                    "marginTop": "0.35rem",
                    "display": "inline-flex",
                    "alignItems": "baseline",
                    "gap": "0.1rem",
                },
            ),
            html.Div(
                [
                    html.Span(
                        record.get("direction_cue", "•"),
                        style={
                            "color": direction_colors.get(record.get("direction", "flat"), palette["muted_text"]),
                            "fontSize": "1.15rem",
                            "fontWeight": "900",
                            "display": "inline-block",
                            "minWidth": "1rem",
                            "textAlign": "center",
                            "textShadow": (
                                "0 0 0.7px rgba(24, 36, 61, 0.95), 0 0 2px rgba(24, 36, 61, 0.6)"
                                if theme == "light"
                                else "0 0 0.7px rgba(243, 246, 251, 0.85), 0 0 2px rgba(243, 246, 251, 0.45)"
                            ),
                        },
                    ),
                    html.Span(
                        f" {record['year']} | change {record['change']}",
                        style={
                            "color": palette["muted_text"],
                            "fontSize": "0.85rem",
                            "fontWeight": "600",
                        },
                    ),
                ],
                style={"display": "flex", "alignItems": "center", "gap": "0.35rem"},
            ),
        ],
        className=f"kpi-card theme-{theme}",
        style={
            "backgroundColor": palette["panel"],
            "border": f"1px solid {palette['border']}",
            "borderRadius": "16px",
            "padding": "1rem 1.1rem",
            "boxShadow": palette["card_shadow"],
            "minWidth": "0",
            "transition": "transform 180ms ease, box-shadow 180ms ease, border-color 180ms ease",
            "cursor": "default",
        },
    )


def chart_panel(title: str, figure, theme: str, subtitle: str | None = None) -> html.Div:
    palette = get_palette(theme)
    return html.Div(
        [
            html.Div(
                [
                    html.Div(
                        title,
                        style={
                            "color": palette["text"],
                            "fontSize": "0.95rem",
                            "fontWeight": "500",
                            "letterSpacing": "0.05em",
                            "textTransform": "uppercase",
                        },
                    ),
                    html.Div(
                        subtitle,
                        style={
                            "color": palette["muted_text"],
                            "fontSize": "0.78rem",
                            "marginTop": "0.25rem",
                        },
                    )
                    if subtitle
                    else None,
                ],
                style={"padding": "0.9rem 1rem 0"},
            ),
            dcc.Graph(figure=figure, config={"displayModeBar": False}),
        ],
        className=f"chart-panel theme-{theme}",
        style={
            "backgroundColor": palette["panel"],
            "border": f"1px solid {palette['border']}",
            "borderRadius": "18px",
            "overflow": "hidden",
            "boxShadow": palette["shadow"],
            "transition": "transform 180ms ease, box-shadow 180ms ease, border-color 180ms ease",
        },
    )


def build_layout(tidy_df, snapshot_df, theme: str = "dark") -> html.Div:
    palette = get_palette(theme)
    kpi_records = build_kpi_records(snapshot_df, theme)
    return html.Div(
        [
            html.Div(
                [
                    html.Div(
                        [
                            html.Div(
                                "ARGENTINA MACRO MONITOR",
                                style={
                                    "color": palette["accent"],
                                    "fontSize": "0.85rem",
                                    "fontWeight": "700",
                                    "letterSpacing": "0.18em",
                                    "textTransform": "uppercase",
                                },
                            ),
                            html.H1(
                                APP_TITLE,
                                style={
                                    "color": palette["text"],
                                    "margin": "0.35rem 0",
                                    "fontWeight": "700",
                                },
                            ),
                            html.P(
                                APP_SUBTITLE,
                                style={
                                    "color": palette["muted_text"],
                                    "margin": 0,
                                    "maxWidth": "780px",
                                },
                            ),
                        ]
                    ),
                    html.Div(
                        SOURCE_LABEL,
                        style={
                            "color": palette["muted_text"],
                            "fontSize": "0.9rem",
                            "paddingTop": "0.5rem",
                        },
                    ),
                ],
                style={"marginBottom": "1.5rem"},
            ),
            html.Div(
                [build_kpi_card(record, theme) for record in kpi_records],
                style={
                    "display": "grid",
                    "gridTemplateColumns": "repeat(auto-fit, minmax(180px, 1fr))",
                    "gap": "1rem",
                    "marginBottom": "1.5rem",
                },
            ),
            html.Div(
                [
                    chart_panel(
                        "GDP growth",
                        build_gdp_growth_line(tidy_df, theme),
                        theme,
                        "Recession years are shaded and major turning points are annotated.",
                    ),
                    chart_panel(
                        "GDP scale",
                        build_gdp_area(tidy_df, theme),
                        theme,
                        "Nominal GDP in current US$ shown in billions.",
                    ),
                ],
                style={
                    "display": "grid",
                    "gridTemplateColumns": "repeat(auto-fit, minmax(320px, 1fr))",
                    "gap": "1rem",
                    "marginBottom": "1rem",
                },
            ),
            html.Div(
                [
                    chart_panel(
                        "GDP deflator inflation and unemployment",
                        build_inflation_unemployment_chart(tidy_df, theme),
                        theme,
                        "Dual-axis view comparing price pressure with labour market conditions.",
                    ),
                    chart_panel(
                        "Trade openness",
                        build_trade_chart(tidy_df, theme),
                        theme,
                        "Exports and imports are compared directly as shares of GDP.",
                    ),
                ],
                style={
                    "display": "grid",
                    "gridTemplateColumns": "repeat(auto-fit, minmax(320px, 1fr))",
                    "gap": "1rem",
                    "marginBottom": "1rem",
                },
            ),
            html.Div(
                [
                    chart_panel(
                        "Growth and GDP deflator inflation regime map",
                        build_bubble_chart(tidy_df, theme),
                        theme,
                        "Bubble size reflects GDP scale; key years are labelled directly.",
                    ),
                    chart_panel(
                        "Latest position vs history",
                        build_latest_position_chart(tidy_df, theme),
                        theme,
                        "Each bar shows how far the latest value sits from its 2000-2024 average.",
                    ),
                ],
                style={
                    "display": "grid",
                    "gridTemplateColumns": "repeat(auto-fit, minmax(320px, 1fr))",
                    "gap": "1rem",
                    "marginBottom": "1rem",
                },
            ),
            chart_panel(
                "Indicator heatmap",
                build_heatmap(tidy_df, theme),
                theme,
                "Values are normalized within each indicator to make mixed units comparable.",
            ),
        ],
        className=f"dashboard-page theme-{theme}",
        style={
            "backgroundColor": palette["background"],
            "minHeight": "100vh",
            "padding": "2rem",
            "fontFamily": FONT_FAMILY,
        },
    )
