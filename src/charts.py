from __future__ import annotations

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from config import (
    CHART_HEIGHTS,
    FONT_FAMILY,
    INDICATORS,
    INDICATOR_ORDER,
    KPI_INDICATORS,
    SERIES_COLORS_LIGHT,
    THEMES,
)


def format_value(value: float, unit: str) -> str:
    if pd.isna(value):
        return "N/A"
    if unit == "current US$":
        return f"${value / 1e9:,.1f}B"
    return f"{value:,.1f}"


def get_palette(theme: str) -> dict:
    return THEMES.get(theme, THEMES["dark"])


def get_series_color(indicator_code: str, theme: str) -> str:
    if theme == "light":
        color_key_by_indicator = {
            "NY.GDP.MKTP.KD.ZG": "gdp_growth",
            "NY.GDP.MKTP.CD": "gdp_usd",
            "NY.GDP.DEFL.KD.ZG": "inflation",
            "SL.UEM.TOTL.ZS": "unemployment",
            "NE.EXP.GNFS.ZS": "exports",
            "NE.IMP.GNFS.ZS": "imports",
            "BX.KLT.DINV.WD.GD.ZS": "fdi",
            "BN.CAB.XOKA.GD.ZS": "current_account",
        }
        return SERIES_COLORS_LIGHT[color_key_by_indicator[indicator_code]]
    return INDICATORS[indicator_code]["color"]


def apply_terminal_theme(fig: go.Figure, title: str, height: int, theme: str = "dark") -> go.Figure:
    palette = get_palette(theme)
    fig.update_layout(
        height=height,
        paper_bgcolor=palette["panel"],
        plot_bgcolor=palette["panel"],
        font={"family": FONT_FAMILY, "color": palette["text"]},
        margin={"l": 40, "r": 20, "t": 24, "b": 40},
        legend={
            "orientation": "h",
            "yanchor": "bottom",
            "y": 1.02,
            "xanchor": "right",
            "x": 1,
            "bgcolor": "rgba(0,0,0,0)",
        },
        hoverlabel={
            "bgcolor": palette["panel_alt"],
            "bordercolor": palette["border"],
            "font": {
                "family": FONT_FAMILY,
                "color": palette["text"],
                "size": 15,
            },
        },
    )
    fig.update_xaxes(
        showgrid=True,
        gridcolor=palette["grid"],
        zeroline=False,
        linecolor=palette["border"],
    )
    fig.update_yaxes(
        showgrid=True,
        gridcolor=palette["grid"],
        zeroline=False,
        linecolor=palette["border"],
    )
    return fig


def indicator_frame(df: pd.DataFrame, indicator_code: str) -> pd.DataFrame:
    return df.loc[df["indicator_code"] == indicator_code].copy()


def build_gdp_growth_line(df: pd.DataFrame, theme: str = "dark") -> go.Figure:
    palette = get_palette(theme)
    data = indicator_frame(df, "NY.GDP.MKTP.KD.ZG")
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=data["year"],
            y=data["value"],
            mode="lines+markers",
            name="GDP growth",
            line={"color": get_series_color("NY.GDP.MKTP.KD.ZG", theme), "width": 3},
            marker={"size": 7},
            hovertemplate="<b>Year:</b> %{x}<br><b>GDP growth:</b> %{y:.3f}%<extra></extra>",
        )
    )
    fig.add_hline(y=0, line_dash="dash", line_color=palette["muted_text"], opacity=0.6)
    fig.update_yaxes(title="%")
    return apply_terminal_theme(fig, "GDP Growth Cycle", CHART_HEIGHTS["standard"], theme)


def build_gdp_area(df: pd.DataFrame, theme: str = "dark") -> go.Figure:
    data = indicator_frame(df, "NY.GDP.MKTP.CD")
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=data["year"],
            y=data["value"],
            mode="lines",
            fill="tozeroy",
            name="GDP (current US$)",
            line={"color": get_series_color("NY.GDP.MKTP.CD", theme), "width": 3},
            fillcolor="rgba(116, 192, 252, 0.25)",
            hovertemplate="<b>Year:</b> %{x}<br><b>GDP:</b> %{y:.3f}<extra></extra>",
        )
    )
    fig.update_yaxes(title="US$")
    return apply_terminal_theme(fig, "GDP Scale Over Time", CHART_HEIGHTS["standard"], theme)


def build_inflation_unemployment_chart(df: pd.DataFrame, theme: str = "dark") -> go.Figure:
    inflation = indicator_frame(df, "NY.GDP.DEFL.KD.ZG")
    unemployment = indicator_frame(df, "SL.UEM.TOTL.ZS")
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(
        go.Scatter(
            x=inflation["year"],
            y=inflation["value"],
            mode="lines+markers",
            name="Inflation (GDP deflator)",
            line={"color": get_series_color("NY.GDP.DEFL.KD.ZG", theme), "width": 3},
            hovertemplate="<b>Year:</b> %{x}<br><b>Inflation, GDP deflator:</b> %{y:.3f}%<extra></extra>",
        ),
        secondary_y=False,
    )
    fig.add_trace(
        go.Scatter(
            x=unemployment["year"],
            y=unemployment["value"],
            mode="lines+markers",
            name="Unemployment",
            line={"color": get_series_color("SL.UEM.TOTL.ZS", theme), "width": 3},
            hovertemplate="<b>Year:</b> %{x}<br><b>Unemployment:</b> %{y:.3f}%<extra></extra>",
        ),
        secondary_y=True,
    )
    fig.update_yaxes(title_text="Inflation, GDP deflator (%)", secondary_y=False)
    fig.update_yaxes(title_text="Unemployment (%)", secondary_y=True)
    return apply_terminal_theme(
        fig, "GDP Deflator Inflation and Labour Pressure", CHART_HEIGHTS["standard"], theme
    )


def build_trade_chart(df: pd.DataFrame, theme: str = "dark") -> go.Figure:
    exports = indicator_frame(df, "NE.EXP.GNFS.ZS")
    imports = indicator_frame(df, "NE.IMP.GNFS.ZS")
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=exports["year"],
            y=exports["value"],
            mode="lines",
            stackgroup="trade",
            name="Exports",
            line={"color": get_series_color("NE.EXP.GNFS.ZS", theme), "width": 2},
            groupnorm="",
            hovertemplate="<b>Year:</b> %{x}<br><b>Exports:</b> %{y:.3f}% of GDP<extra></extra>",
        )
    )
    fig.add_trace(
        go.Scatter(
            x=imports["year"],
            y=imports["value"],
            mode="lines",
            stackgroup="trade",
            name="Imports",
            line={"color": get_series_color("NE.IMP.GNFS.ZS", theme), "width": 2},
            hovertemplate="<b>Year:</b> %{x}<br><b>Imports:</b> %{y:.3f}% of GDP<extra></extra>",
        )
    )
    fig.update_yaxes(title="% of GDP")
    return apply_terminal_theme(fig, "Trade Openness Profile", CHART_HEIGHTS["standard"], theme)


def build_bubble_chart(df: pd.DataFrame, theme: str = "dark") -> go.Figure:
    palette = get_palette(theme)
    growth = indicator_frame(df, "NY.GDP.MKTP.KD.ZG")[["year", "value"]].rename(
        columns={"value": "gdp_growth"}
    )
    inflation = indicator_frame(df, "NY.GDP.DEFL.KD.ZG")[["year", "value"]].rename(
        columns={"value": "inflation"}
    )
    gdp = indicator_frame(df, "NY.GDP.MKTP.CD")[["year", "value"]].rename(
        columns={"value": "gdp_usd"}
    )
    bubble_df = growth.merge(inflation, on="year").merge(gdp, on="year")
    fig = px.scatter(
        bubble_df,
        x="gdp_growth",
        y="inflation",
        size="gdp_usd",
        color="year",
        size_max=35,
        color_continuous_scale=[
            get_series_color("NY.GDP.MKTP.KD.ZG", theme),
            get_series_color("NE.EXP.GNFS.ZS", theme),
            palette["accent"],
            get_series_color("BN.CAB.XOKA.GD.ZS", theme),
        ],
        labels={
            "gdp_growth": "GDP growth (annual %)",
            "inflation": "Inflation, GDP deflator (%)",
            "year": "Year",
        },
        hover_data={"gdp_usd": ":.3f", "year": True},
    )
    fig.update_traces(
        marker={"opacity": 0.75, "line": {"width": 1, "color": palette["text"]}},
        hovertemplate=(
            "<b>Year:</b> %{marker.color}<br>"
            "<b>GDP growth:</b> %{x:.3f}%<br>"
            "<b>Inflation, GDP deflator:</b> %{y:.3f}%<br>"
            "<b>GDP (current US$):</b> %{customdata[0]:.3f}<extra></extra>"
        ),
    )
    return apply_terminal_theme(
        fig, "Growth vs GDP Deflator Inflation Regimes", CHART_HEIGHTS["standard"], theme
    )


def build_latest_position_chart(df: pd.DataFrame, theme: str = "dark") -> go.Figure:
    palette = get_palette(theme)
    stats = (
        df.groupby(["indicator_code", "indicator_name", "unit"], as_index=False)["value"]
        .agg(hist_mean="mean", hist_std="std")
    )
    latest = df.sort_values("year").groupby("indicator_code", as_index=False).tail(1)
    latest = latest.merge(stats, on=["indicator_code", "indicator_name", "unit"], how="left")
    latest["z_score"] = latest.apply(
        lambda row: 0
        if pd.isna(row["hist_std"]) or row["hist_std"] == 0
        else (row["value"] - row["hist_mean"]) / row["hist_std"],
        axis=1,
    )
    latest["short_label"] = latest["indicator_code"].map(
        lambda code: INDICATORS[code]["short_label"]
    )
    latest["color"] = latest["indicator_code"].map(lambda code: get_series_color(code, theme))
    latest = latest.sort_values("z_score", ascending=True)

    fig = go.Figure(
        go.Bar(
            x=latest["z_score"],
            y=latest["short_label"],
            orientation="h",
            marker={"color": latest["color"], "line": {"color": palette["border"], "width": 1}},
            customdata=latest[["value", "hist_mean", "unit", "year"]].to_numpy(),
            hovertemplate=(
                "<b>%{y}</b><br>"
                "Latest year: %{customdata[3]}<br>"
                "Latest value: %{customdata[0]:.3f} %{customdata[2]}<br>"
                "Historical mean: %{customdata[1]:.3f} %{customdata[2]}<br>"
                "Deviation: %{x:.3f} standard deviations<extra></extra>"
            ),
        )
    )
    fig.add_vline(x=0, line_dash="dash", line_color=palette["muted_text"], opacity=0.8)
    fig.update_xaxes(title="Latest value relative to 2000-2024 historical average (z-score)")
    fig.update_yaxes(title="")
    return apply_terminal_theme(fig, "Latest Position vs Historical Norm", CHART_HEIGHTS["standard"], theme)


def build_heatmap(df: pd.DataFrame, theme: str = "dark") -> go.Figure:
    palette = get_palette(theme)
    heatmap_df = (
        df.pivot(index="indicator_code", columns="year", values="value")
        .reindex(INDICATOR_ORDER)
        .astype(float)
    )

    normalized = heatmap_df.apply(
        lambda row: (row - row.mean()) / row.std(ddof=0) if row.std(ddof=0) else row * 0,
        axis=1,
    )
    y_labels = [INDICATORS[code]["short_label"] for code in normalized.index]
    fig = go.Figure(
        data=
        go.Heatmap(
            z=normalized.values,
            x=normalized.columns.tolist(),
            y=y_labels,
            colorscale=[
                [0.0, get_series_color("NY.GDP.MKTP.KD.ZG", theme)],
                [0.5, palette["panel_alt"]],
                [0.75, get_series_color("NY.GDP.DEFL.KD.ZG", theme)],
                [1.0, get_series_color("BN.CAB.XOKA.GD.ZS", theme)],
            ],
            colorbar={
                "title": {"text": "Z-score", "font": {"color": palette["text"]}},
                "tickfont": {"color": palette["text"]},
            },
        )
    )
    fig.update_xaxes(type="category")
    return apply_terminal_theme(fig, "Indicator Heatmap (Normalized)", CHART_HEIGHTS["tall"], theme)


def build_kpi_records(snapshot_df: pd.DataFrame, theme: str = "dark") -> list[dict[str, str]]:
    records = []
    snapshot_indexed = snapshot_df.set_index("indicator_code")
    for indicator_code in KPI_INDICATORS:
        if indicator_code not in snapshot_indexed.index:
            continue
        if indicator_code not in INDICATORS:
            continue
        row = snapshot_indexed.loc[indicator_code]
        records.append(
            {
                "label": INDICATORS[indicator_code]["short_label"],
                "value": format_value(row["latest_value"], row["unit"]),
                "change": (
                    f"{row['absolute_change']:+.1f}"
                    if pd.notna(row["absolute_change"])
                    else "N/A"
                ),
                "year": str(int(row["latest_year"])),
                "color": get_series_color(indicator_code, theme),
                "unit": row["unit"],
                "indicator_code": indicator_code,
            }
        )
    return records
