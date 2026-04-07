# Assignment 2 Report

## Table of Figures

Figure 1. KPI summary cards for Argentina's latest macroeconomic indicators.  
Figure 2. GDP growth cycle in Argentina, 2000-2024.  
Figure 3. Nominal GDP scale in Argentina, 2000-2024.  
Figure 4. GDP deflator inflation and unemployment in Argentina, 2000-2024.  
Figure 5. Exports and imports as shares of GDP in Argentina, 2000-2024.  
Figure 6. Growth-inflation regime map for Argentina, 2000-2024.  
Figure 7. Latest indicator position relative to Argentina's 2000-2024 historical norm.  
Figure 8. Normalized indicator heatmap for Argentina, 2000-2024.

## Table of Tables

Table 1. Indicators used in the dashboard.

## Introduction

The project presents a dashboard that visualises selected economic indicators for Argentina using the World Bank World Development Indicators (WDI) data set [1]. Argentina has long-running macroeconomic volatility with repeated recovery episodes, making it possible to examine how growth, prices, labour-market pressure, and the external sector interact over time. The dashboard is designed to show Argentina as an economy shaped by instability, adjustment, and periodic recovery.

The dashboard focuses on macroeconomic stability, trade and openness and crisis and recovery. These chosen areas provide a coherent analytical framework for interpreting Argentina's economic performance. The period from 2000 to 2024 was selected for analysis because it captures the aftermath of the 2001-2002 crisis, the later rebound, the pandemic shock in 2020, and the recent episode of severe inflationary pressure. Restricting the visual analysis to this period improves readability while preserving the most relevant modern economic events.

The data source used for the dashboard is the World Bank World Development Indicators [1]. The WDI source was selected because it is official, well documented, broad in coverage, and consistent in structure [1,3]. These qualities make it appropriate both for dashboard implementation and for analytical reporting, since the same source can support multiple visualisations without needing to reconcile conflicting definitions across providers.

## Country Overview

Argentina is one of Latin America's largest economies, but its modern economic history has been marked by pronounced volatility. Periods of contraction and recovery have been accompanied by high inflation, changing trade conditions, and recurrent external-sector stress. This makes Argentina a strong case study for visualisation because the data contains clear turning points and relationships that can be communicated more effectively through a dashboard than through isolated summary statistics.

The dashboard not only displays Argentina's indicators but also helps the viewer understand how multiple dimensions of economic performance interact. Growth alone does not explain conditions if price instability is extreme. Similarly, external trade and capital flows matter because domestic performance cannot be separated from external exposure.

## Data Set

This project uses the full World Bank World Development Indicators dataset, filtered to Argentina and a selected set of macroeconomic indicators [1,2]. The dashboard uses annual observations from 2000 to 2024.

## Data Sources

The original data source is the World Bank World Development Indicators (WDI) database [1]:

- World Bank WDI zip: https://databank.worldbank.org/data/download/WDI_CSV.zip
- World Bank WDI overview: https://datatopics.worldbank.org/world-development-indicators/
- World Bank API documentation: https://datahelpdesk.worldbank.org/knowledgebase/articles/889392-about-the-indicators-api-documentation

The raw WDI data is stored in a wide format in which each row corresponds to a country-indicator combination and each year appears as a separate column [2]. This structure is useful for archival distribution, but it is not optimal for interactive dashboard visualisation. As a result, the data was filtered, reshaped, and standardised into a tidy format suitable for Plotly and Dash [3].

## Indicator Selection

### 2.2.1 Table 1. Indicators used in the Dashboard

Table 1. Indicators used in the dashboard

| Indicator | Unit | Dashboard use |
| --- | --- | --- |
| GDP growth | Annual % | KPI cards, GDP growth chart, bubble chart |
| GDP (current US$) | Current US $ | GDP scale chart, bubble size encoding |
| GDP deflator inflation | Annual % | KPI cards, inflation-unemployment chart, bubble chart |
| Unemployment | % of total labour force | KPI cards, inflation-unemployment chart |
| Exports of goods and services | % of GDP | KPI cards, trade openness chart |
| Imports of goods and services | % of GDP | KPI cards, trade openness chart |
| Foreign direct investment, net inflows | % of GDP | KPI cards, latest-position chart, heatmap |
| Current account balance | % of GDP | Latest-position chart, heatmap |

These indicators were selected because they jointly capture three important dimensions of Argentina's economy.

- Domestic performance: GDP growth and unemployment show changes in output and labour-market stress.
- Price instability: GDP deflator inflation reflects macroeconomic pressure in the price system.
- External exposure: exports, imports, FDI, and current account balance show the extent to which domestic conditions interact with trade and external financing.

## Data Preparation and Structure

The dashboard uses a processed tidy file with the following fields: country name, country code, indicator name, indicator code, topic, unit, year and value.

This data preparation step is necessary because in Dash and Plotly, a long-format table supports filtering, chart switching, and multi-visual reuse more effectively than the original wide file. The dashboard also uses a second helper file containing the latest available value and year-on-year change for KPI cards.

This preparation process, including the required filters and tidy structure, preserves the raw data source while creating a cleaner analytical layer for visualisation.

## Interesting Attributes

The data spans across a sufficiently long period to show multiple economic phases rather than a single short episode. This makes it possible to compare crisis years, recovery years, and more stable years within a single analytical framework.

The selected indicators have mixed units like percentages, percentages of GDP and current US dollars. This characteristic affects which visualisations are appropriate for different indicators. Some indicators can be shown directly in time-series charts, while others cannot be compared in raw form within the same chart.

The data includes domestic performance, price pressure, labour conditions, trade openness, and external financing. This breadth supports a richer dashboard as it allows the analysis to move beyond one-dimensional commentary.

Finally, Argentina itself is an interesting case because the data contains clear turning points. This makes annotations, phase-based interpretation, and crisis markers genuinely meaningful.

## Visualisations and Analysis

### Visualisation 1: KPI Summary Cards

The KPI summary cards provide a concise summary of the latest available values for six core indicators: GDP growth, inflation, unemployment, exports, imports and FDI. This visual form is appropriate because it gives the dashboard users an immediate overview before examining historical trends in detail. The cards therefore serve as the first analytical layer in the dashboard.

At a glance, the cards show that Argentina's macroeconomic picture remains under pressure, inflation is elevated, growth remains weak, and external-sector indicators are needed to interpret whether current conditions are purely domestic or linked to wider external adjustment.

The KPI design also supports clarity by separating current level from historical trend. The cards act as a headline summary and direct the viewer to the more detailed visuals below.

Figure 1. KPI summary cards for Argentina's latest macroeconomic indicators.

### Visualisation 2: GDP Growth Cycle

The GDP growth visual uses a line chart because GDP growth is a time-series indicator and the main analytical aim is to show contraction, rebound, and turning points. A line chart is the most suitable form for this task because it reveals sequence, direction, and volatility more clearly than bars or summary cards.

This chart shows that Argentina's economic path is highly cyclical. The 2001-2002 crisis produces a severe contraction, followed by recovery, while the 2020 pandemic shock creates a later collapse in output. Negative-growth years are highlighted to make recession periods more visible, and annotations are used to identify important turning points.

The intended analytical message is that Argentina should not be understood as an economy with steady incremental growth. Instead, growth performance is interrupted by major shocks, and recovery needs to be interpreted as part of a broader cycle rather than as evidence of stable long-run progression.

Figure 2. GDP growth cycle in Argentina, 2000-2024.

### Visualisation 3: GDP Scale Over Time

The GDP scale chart uses an area chart in current US dollars to show the changing size of the economy over time. This visualisation complements the GDP growth chart. The GDP growth chart highlights the rate of change, whereas the GDP scale chart highlights economic magnitude.

The chart shows that Argentina remains a large economy in nominal scale even when growth performance is unstable. A country with a large economy but severe macroeconomic instability. The visual, therefore, prevents the viewer from equating economic size with economic stability.

Expressing GDP in billions of current US dollars improves readability and makes the chart more suitable for dashboard presentation. It also reinforces the need to interpret the visual carefully, since nominal GDP can rise even when underlying macroeconomic conditions remain fragile.

Figure 3. Nominal GDP scale in Argentina, 2000-2024.

### Visualisation 4: Inflation and Unemployment

This chart compares GDP deflator inflation with unemployment using a dual-axis line chart. The choice of a dual-axis format is justified because both indicators are central to macroeconomic stability, but their scales differ substantially. A single shared axis would make one series visually unreadable.

The chart shows that recent Argentine stress is driven especially strongly by price instability. Unemployment matters, but the inflation series diverges much more sharply in recent years. This distinction is important because it highlights that macroeconomic deterioration is not only about labour-market weakness. The inflation surge represents a broader destabilisation of the economic environment.

The GDP deflator was selected instead of consumer price inflation because it provided complete historical coverage across the chosen period in the available WDI data extract [1,2]. The visual still succeeds analytically because the purpose is to show broad price-system instability over time.

Figure 4. GDP deflator inflation and unemployment in Argentina, 2000-2024.

### Visualisation 5: Trade Openness Profile

The trade chart compares exports and imports directly as shares of GDP using two lines. This is a more appropriate design than a stacked area chart because the main analytical goal is comparison rather than cumulative composition. The viewer can therefore judge whether exports and imports move together, diverge, or adjust differently during stress periods.

This visual supports the dashboard's trade and openness theme. It shows that Argentina's external-sector position changes over time and that widening distance between exports and imports can reveal periods of external adjustment or changing exposure. In other words, the domestic macro story cannot be fully understood without reference to the external sector.

The visual is also useful because it keeps the trade indicators in the same unit, % of GDP, which makes direct comparison valid without additional transformation.

Figure 5. Exports and imports as shares of GDP in Argentina, 2000-2024.

### Visualisation 6: Growth-Inflation Regime Map

The bubble chart plots GDP growth on one axis and GDP deflator inflation on the other, while bubble size represents GDP scale. This chart was chosen because it provides a more relational form of analysis than a standard time-series plot. It allows the viewer to examine how years cluster into broad macroeconomic regimes rather than only how one variable changes over time.

The colour scheme groups years into crisis, recovery, recent instability and baseline. This is analytically useful because it gives structure to the relationship between growth and inflation. Instead of treating every year as a disconnected point, the chart suggests that Argentina's macroeconomic history can be interpreted as movement across distinct regimes. Crisis years tend to combine weak growth with stress, recovery years occupy a different part of the chart, and recent instability appears as a separate configuration with very high inflation pressure.

This visual is especially valuable because it supports inference. It encourages the viewer to think about clusters, exceptions, and transitions, which is closer to analytical reasoning than simple descriptive display.

Figure 6. Growth-inflation regime map for Argentina, 2000-2024.

### Visualisation 7: Latest Position vs Historical Norm

This horizontal bar chart shows how unusual the latest available values are relative to Argentina's own recent history. The indicators are standardized using z-scores, so each value is expressed as its distance from its own historical mean. This design was necessary because the dashboard includes mixed units that cannot be compared directly in raw form.

This visual avoids comparing values with different units on the same raw scale. By standardising each series, the chart instead tries to answer which indicators are currently most unusual relative to their own historical behaviour.

This makes the chart particularly useful for identifying current pressure points. It also demonstrates a better understanding of the data properties.

Figure 7. Latest indicator position relative to Argentina's 2000-2024 historical norm.

### Visualisation 8: Indicator Heatmap

The heatmap provides a compact summary of all indicators across the 2000-2024 period. Each indicator is normalized to its own history so that mixed units remain comparable. This makes the heatmap one of the most analytically powerful visuals in the dashboard, because it allows multiple indicators and multiple years to be considered together without collapsing them into a single summary number.

The purpose of the heatmap is to reveal periods in which several indicators simultaneously depart from their usual levels. Crisis markers are included to draw attention to key years, but the main value of the chart lies in pattern recognition. The viewer can identify whether stress is concentrated in one indicator, one period, or across the system more broadly.

This chart is particularly effective for dashboard analysis because it models the mixed-unit problem appropriately. Rather than pretending GDP in dollars, inflation in percentages, and current account balance as a share of GDP are directly comparable, the heatmap compares each series against its own baseline.

Figure 8. Normalized indicator heatmap for Argentina, 2000-2024.

## Conclusion

The dashboard shows that Argentina's economic performance between 2000 and 2024 is best understood as a combination of instability, adjustment, and uneven recovery. GDP growth identifies repeated contraction and rebound cycles, inflation highlights severe price-system stress, unemployment adds labour-market context, and the trade and external-sector indicators show that domestic conditions are closely tied to external exposure.

The WDI data set was an appropriate source because it offered broad coverage, consistent definitions, and enough historical depth to support a multi-panel dashboard [1,3]. At the same time, the report has identified important limitations, including annual frequency, mixed units, nominal measures, and the use of GDP deflator inflation as a proxy for price pressure. These limitations were not ignored; instead, they directly informed the visual design choices used in the dashboard.

Overall, the dashboard supports the conclusion that Argentina's economy cannot be adequately described by one headline number. A more convincing interpretation emerges only when growth, prices, labour conditions, trade, and external balance are examined together. The dashboard therefore succeeds not only as a technical visualisation exercise, but also as a structured analytical account of Argentina's modern economic instability and recovery cycles.

## References

1. World Bank. World Development Indicators [Internet]. Washington (DC): World Bank; [cited 2026 Apr 6]. Available from: https://datatopics.worldbank.org/world-development-indicators/
2. World Bank. WDI bulk CSV download [Internet]. Washington (DC): World Bank; [cited 2026 Apr 6]. Available from: https://databank.worldbank.org/data/download/WDI_CSV.zip
3. World Bank. About the indicators API documentation [Internet]. Washington (DC): World Bank; [cited 2026 Apr 6]. Available from: https://datahelpdesk.worldbank.org/knowledgebase/articles/889392-about-the-indicators-api-documentation
