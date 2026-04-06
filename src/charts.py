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


KEY_EVENT_YEARS = {
    2002: "2001-02 crisis low",
    2020: "Pandemic shock",
    2024: "Recent instability",
}

REGIME_COLORS_DARK = {
    "Crisis": "#FF5D73",
    "Recovery": "#2EC4B6",
    "Recent instability": "#FF8A4C",
    "Baseline": "#4DA3FF",
}

REGIME_COLORS_LIGHT = {
    "Crisis": "#BE245A",
    "Recovery": "#0D8B78",
    "Recent instability": "#CC4B00",
    "Baseline": "#0A5BC4",
}


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


def get_regime_colors(theme: str) -> dict[str, str]:
    return REGIME_COLORS_LIGHT if theme == "light" else REGIME_COLORS_DARK


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


def add_event_annotations(
    fig: go.Figure,
    data: pd.DataFrame,
    x_col: str,
    y_col: str,
    years: list[int],
    color: str,
    theme: str,
) -> go.Figure:
    palette = get_palette(theme)
    points = data.loc[data[x_col].isin(years), [x_col, y_col]].dropna()
    for _, row in points.iterrows():
        year = int(row[x_col])
        fig.add_annotation(
            x=year,
            y=row[y_col],
            text=KEY_EVENT_YEARS.get(year, str(year)),
            showarrow=True,
            arrowhead=2,
            arrowsize=1,
            arrowwidth=1.5,
            arrowcolor=color,
            ax=0,
            ay=-40,
            font={"size": 11, "color": palette["text"]},
            bgcolor=palette["panel_alt"],
            bordercolor=color,
            borderwidth=1.5,
            borderpad=4,
            opacity=0.96,
        )
    return fig


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
    negative_periods = data.loc[data["value"] < 0, "year"].tolist()
    for year in negative_periods:
        fig.add_vrect(
            x0=year - 0.5,
            x1=year + 0.5,
            fillcolor=get_series_color("NY.GDP.DEFL.KD.ZG", theme),
            opacity=0.08,
            line_width=0,
        )
    add_event_annotations(
        fig,
        data,
        "year",
        "value",
        [2002, 2020, 2024],
        get_series_color("NY.GDP.MKTP.KD.ZG", theme),
        theme,
    )
    fig.update_yaxes(title="%")
    return apply_terminal_theme(fig, "GDP Growth Cycle", CHART_HEIGHTS["standard"], theme)


def build_gdp_area(df: pd.DataFrame, theme: str = "dark") -> go.Figure:
    data = indicator_frame(df, "NY.GDP.MKTP.CD")
    data["gdp_billions"] = data["value"] / 1e9
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=data["year"],
            y=data["gdp_billions"],
            mode="lines",
            fill="tozeroy",
            name="GDP (current US$)",
            line={"color": get_series_color("NY.GDP.MKTP.CD", theme), "width": 3},
            fillcolor="rgba(116, 192, 252, 0.25)",
            hovertemplate="<b>Year:</b> %{x}<br><b>GDP:</b> $%{y:.3f}B<extra></extra>",
        )
    )
    fig.update_yaxes(title="Current US$ (billions)", tickprefix="$", ticksuffix="B")
    return apply_terminal_theme(fig, "GDP Scale Over Time", CHART_HEIGHTS["standard"], theme)


def build_inflation_unemployment_chart(df: pd.DataFrame, theme: str = "dark") -> go.Figure:
    palette = get_palette(theme)
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
            line={"color": get_series_color("SL.UEM.TOTL.ZS", theme), "width": 3, "dash": "dot"},
            hovertemplate="<b>Year:</b> %{x}<br><b>Unemployment:</b> %{y:.3f}%<extra></extra>",
        ),
        secondary_y=True,
    )
    inflation_spike = inflation.sort_values("value", ascending=False).head(1)
    if not inflation_spike.empty:
        row = inflation_spike.iloc[0]
        fig.add_annotation(
            x=row["year"],
            y=row["value"],
            text="Deflator spike",
            showarrow=True,
            arrowhead=2,
            arrowwidth=1.5,
            arrowcolor=get_series_color("NY.GDP.DEFL.KD.ZG", theme),
            ax=24,
            ay=-32,
            font={"size": 11, "color": palette["text"]},
            bgcolor=palette["panel_alt"],
            bordercolor=get_series_color("NY.GDP.DEFL.KD.ZG", theme),
            borderwidth=1.5,
            borderpad=4,
            opacity=0.96,
        )
    fig.update_yaxes(title_text="Inflation, GDP deflator (%)", secondary_y=False)
    fig.update_yaxes(title_text="Unemployment (%)", secondary_y=True)
    return apply_terminal_theme(
        fig, "GDP Deflator Inflation and Labour Pressure", CHART_HEIGHTS["standard"], theme
    )


def build_trade_chart(df: pd.DataFrame, theme: str = "dark") -> go.Figure:
    palette = get_palette(theme)
    exports = indicator_frame(df, "NE.EXP.GNFS.ZS")
    imports = indicator_frame(df, "NE.IMP.GNFS.ZS")
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=exports["year"],
            y=exports["value"],
            mode="lines+markers",
            name="Exports",
            line={"color": get_series_color("NE.EXP.GNFS.ZS", theme), "width": 3},
            hovertemplate="<b>Year:</b> %{x}<br><b>Exports:</b> %{y:.3f}% of GDP<extra></extra>",
        )
    )
    fig.add_trace(
        go.Scatter(
            x=imports["year"],
            y=imports["value"],
            mode="lines+markers",
            name="Imports",
            line={"color": get_series_color("NE.IMP.GNFS.ZS", theme), "width": 3, "dash": "dash"},
            hovertemplate="<b>Year:</b> %{x}<br><b>Imports:</b> %{y:.3f}% of GDP<extra></extra>",
        )
    )
    trade_gap = exports.merge(imports, on="year", suffixes=("_exports", "_imports"))
    trade_gap["gap"] = (trade_gap["value_exports"] - trade_gap["value_imports"]).abs()
    widest_gap = trade_gap.sort_values("gap", ascending=False).head(1)
    if not widest_gap.empty:
        row = widest_gap.iloc[0]
        fig.add_annotation(
            x=row["year"],
            y=row["value_exports"],
            text="Wide trade gap",
            showarrow=True,
            arrowhead=2,
            arrowwidth=1.5,
            arrowcolor=get_series_color("NE.EXP.GNFS.ZS", theme),
            ax=16,
            ay=-34,
            font={"size": 11, "color": palette["text"]},
            bgcolor=palette["panel_alt"],
            bordercolor=get_series_color("NE.EXP.GNFS.ZS", theme),
            borderwidth=1.5,
            borderpad=4,
            opacity=0.96,
        )
    fig.update_yaxes(title="% of GDP")
    return apply_terminal_theme(fig, "Trade Openness Profile", CHART_HEIGHTS["standard"], theme)


def build_bubble_chart(df: pd.DataFrame, theme: str = "dark") -> go.Figure:
    palette = get_palette(theme)
    regime_colors = get_regime_colors(theme)
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
    bubble_df["regime"] = "Baseline"
    bubble_df.loc[bubble_df["year"].isin([2001, 2002, 2020]), "regime"] = "Crisis"
    bubble_df.loc[bubble_df["year"].isin([2003, 2004, 2005, 2021, 2022]), "regime"] = "Recovery"
    bubble_df.loc[bubble_df["year"].isin([2023, 2024]), "regime"] = "Recent instability"
    fig = px.scatter(
        bubble_df,
        x="gdp_growth",
        y="inflation",
        size="gdp_usd",
        color="regime",
        size_max=35,
        color_discrete_map=regime_colors,
        labels={
            "gdp_growth": "GDP growth (annual %)",
            "inflation": "Inflation, GDP deflator (%)",
            "regime": "Economic regime",
        },
        hover_data={"gdp_usd": ":.3f", "year": True},
    )
    fig.update_traces(
        marker={"opacity": 0.75, "line": {"width": 1, "color": palette["text"]}},
        hovertemplate=(
            "<b>Year:</b> %{customdata[1]}<br>"
            "<b>Regime:</b> %{fullData.name}<br>"
            "<b>GDP growth:</b> %{x:.3f}%<br>"
            "<b>Inflation, GDP deflator:</b> %{y:.3f}%<br>"
            "<b>GDP (current US$):</b> %{customdata[0]:.3f}<extra></extra>"
        ),
    )
    labeled_years = bubble_df.loc[bubble_df["year"].isin([2002, 2020, 2024])].copy()
    fig.add_trace(
        go.Scatter(
            x=labeled_years["gdp_growth"],
            y=labeled_years["inflation"],
            mode="text",
            text=labeled_years["year"].astype(str),
            textposition="top center",
            textfont={"size": 11, "color": palette["text"]},
            showlegend=False,
            hoverinfo="skip",
        )
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
    latest["abs_z_score"] = latest["z_score"].abs()
    latest = latest.sort_values("abs_z_score", ascending=True)

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
    fig.update_xaxes(title="Standard deviations from 2000-2024 average (z-score)")
    fig.update_yaxes(title="")
    return apply_terminal_theme(fig, "Latest Position vs Historical Norm", CHART_HEIGHTS["standard"], theme)


def build_heatmap(df: pd.DataFrame, theme: str = "dark") -> go.Figure:
    palette = get_palette(theme)
    heatmap_df = (
        df.pivot(index="indicator_code", columns="year", values="value")
        .reindex(INDICATOR_ORDER)
        .astype(float)
    )
    year_values = heatmap_df.columns.astype(int).tolist()

    normalized = heatmap_df.copy()
    for indicator_code in normalized.index:
        row = normalized.loc[indicator_code]
        std = row.std(ddof=0)
        normalized.loc[indicator_code] = (
            (row - row.mean()) / std if std and not pd.isna(std) else 0
        )

    normalized = normalized.fillna(0.0)
    zmax = float(normalized.abs().to_numpy().max())
    zmax = max(zmax, 1.0)
    y_labels = [INDICATORS[code]["short_label"] for code in heatmap_df.index]
    customdata = []
    for indicator_code in heatmap_df.index:
        indicator_custom = []
        for year in heatmap_df.columns:
            indicator_custom.append(
                [
                    INDICATORS[indicator_code]["short_label"],
                    int(year),
                    float(heatmap_df.loc[indicator_code, year]),
                    INDICATORS[indicator_code]["unit"],
                ]
            )
        customdata.append(indicator_custom)
    fig = go.Figure(
        data=
        go.Heatmap(
            z=normalized.values,
            x=year_values,
            y=y_labels,
            zmid=0,
            zmin=-zmax,
            zmax=zmax,
            colorscale=[
                [0.0, get_series_color("NY.GDP.MKTP.KD.ZG", theme)],
                [0.5, palette["panel_alt"]],
                [0.75, get_series_color("NY.GDP.DEFL.KD.ZG", theme)],
                [1.0, get_series_color("BN.CAB.XOKA.GD.ZS", theme)],
            ],
            customdata=customdata,
            hovertemplate=(
                "<b>%{customdata[0]}</b><br>"
                "Year: %{customdata[1]}<br>"
                "Raw value: %{customdata[2]:.3f} %{customdata[3]}<br>"
                "Normalized score: %{z:.3f}<extra></extra>"
            ),
            colorbar={
                "title": {"text": "Z-score", "font": {"color": palette["text"]}},
                "tickfont": {"color": palette["text"]},
            },
        )
    )
    fig.update_xaxes(
        type="linear",
        tickmode="array",
        tickvals=year_values,
        ticktext=[str(year) for year in year_values],
        range=[min(year_values) - 0.5, max(year_values) + 0.5],
    )
    for year in [2002, 2020, 2024]:
        fig.add_vline(
            x=year,
            line_dash="dot",
            line_width=1,
            line_color=palette["text"],
            opacity=0.55,
        )
    fig.add_annotation(
        xref="paper",
        yref="paper",
        x=1,
        y=1.12,
        text="Normalized values; warmer colors indicate stronger relative pressure",
        showarrow=False,
        xanchor="right",
        font={"size": 11, "color": palette["muted_text"]},
        bgcolor=palette["panel_alt"],
        bordercolor=palette["border"],
        borderwidth=1,
        borderpad=4,
        opacity=0.9,
    )
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
        absolute_change = row["absolute_change"]
        direction = "flat"
        cue = "•"
        if pd.notna(absolute_change):
            if absolute_change > 0:
                direction = "up"
                cue = "↑"
            elif absolute_change < 0:
                direction = "down"
                cue = "↓"
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
                "direction": direction,
                "direction_cue": cue,
            }
        )
    return records
