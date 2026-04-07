# Assignment 2 Report

## Assignment Cover Sheet

Insert the completed and signed official cover sheet from Moodle as page 1 of the final submitted report.

Fields to complete before submission:

- student name
- student number
- module name and code
- assignment title
- submission date
- signature

## Table of Contents

1. Introduction
   1.1 Country Overview
2. Data Set
   2.1 Data Source
   2.2 Indicator Selection
   2.3 Data Preparation and Structure
   2.4 Interesting Attributes of the Data
   2.5 Data Limitations
3. Visualisations and Analysis
   3.1 KPI Summary Cards
   3.2 GDP Growth Cycle
   3.3 GDP Scale Over Time
   3.4 Inflation and Unemployment
   3.5 Trade Openness Profile
   3.6 Growth-Inflation Regime Map
   3.7 Latest Position vs Historical Norm
   3.8 Indicator Heatmap
4. Conclusion
5. References

## Table of Figures

Figure 1. KPI summary cards  
Figure 2. GDP growth cycle  
Figure 3. GDP scale over time  
Figure 4. Inflation and unemployment comparison  
Figure 5. Trade openness profile  
Figure 6. Growth-inflation regime map  
Figure 7. Latest position vs historical norm  
Figure 8. Indicator heatmap

## Table of Tables

No separate statistical tables are required in this report. The discussion is based on the dashboard visuals and the processed Argentina indicator data.

## 1. Introduction

This report presents a Python dashboard that visualises selected economic indicators for **Argentina** using the World Bank **World Development Indicators (WDI)** data set [1]. Argentina is a particularly suitable country for dashboard analysis because it combines long-run macroeconomic volatility with repeated recovery episodes, making it possible to examine how growth, prices, labour-market pressure, and the external sector interact over time. Rather than presenting a single headline measure, the dashboard is designed to show Argentina as an economy shaped by instability, adjustment, and periodic recovery.

The dashboard focuses on three linked themes:

- macroeconomic stability
- trade and openness
- crisis and recovery

These themes were chosen because they provide a coherent analytical framework for interpreting Argentine performance between **2000 and 2024**. This period captures the aftermath of the 2001-2002 crisis, the later rebound, the pandemic shock in 2020, and the recent episode of severe inflationary pressure. Restricting the visual analysis to this window improves readability while preserving the most relevant modern economic events.

The data source used throughout the dashboard is the World Bank WDI full CSV release [2]:

- World Bank WDI ZIP: [https://databank.worldbank.org/data/download/WDI_CSV.zip](https://databank.worldbank.org/data/download/WDI_CSV.zip)

The WDI source was selected because it is official, well documented, broad in coverage, and consistent in structure [1,3]. These qualities make it appropriate both for dashboard implementation and for analytical reporting, since the same source can support multiple visualisations without needing to reconcile conflicting definitions across providers.

### 1.1 Country Overview

Argentina is one of Latin America's largest economies, but its modern economic history has been marked by pronounced volatility. Periods of contraction and recovery have been accompanied by high inflation, changing trade conditions, and recurrent external-sector stress. This makes Argentina a strong case study for visualisation because the data contains clear turning points, regime shifts, and relationships that can be communicated more effectively through a dashboard than through isolated summary statistics.

The purpose of the dashboard is therefore not simply to display Argentina's indicators, but to help the viewer understand how multiple dimensions of economic performance interact. Growth alone does not explain conditions if price instability is extreme; similarly, external trade and capital flows matter because domestic performance cannot be separated from external exposure.

## 2. Data Set

This project uses the **World Bank World Development Indicators** full CSV download and filters it to Argentina and a selected set of macroeconomic indicators [1,2]. The dashboard uses annual observations from **2000 to 2024**.

### 2.1 Data Source

The original data source is the World Bank WDI bulk CSV package:

- World Bank WDI ZIP: [https://databank.worldbank.org/data/download/WDI_CSV.zip](https://databank.worldbank.org/data/download/WDI_CSV.zip)
- World Bank WDI overview: [https://datatopics.worldbank.org/world-development-indicators/](https://datatopics.worldbank.org/world-development-indicators/)
- World Bank API documentation: [https://datahelpdesk.worldbank.org/knowledgebase/articles/889392-about-the-indicators-api-documentation](https://datahelpdesk.worldbank.org/knowledgebase/articles/889392-about-the-indicators-api-documentation)

The raw WDI data is stored in a wide format in which each row corresponds to a country-indicator combination and each year appears as a separate column. This structure is useful for archival distribution, but it is not optimal for interactive dashboard visualisation. As a result, the data was filtered, reshaped, and standardised into a tidy format suitable for Plotly and Dash [3].

### 2.2 Indicator Selection

The dashboard uses eight indicators:

- GDP growth (annual %) `NY.GDP.MKTP.KD.ZG`
- GDP (current US$) `NY.GDP.MKTP.CD`
- Inflation, GDP deflator (annual %) `NY.GDP.DEFL.KD.ZG`
- Unemployment, total (% of total labor force) `SL.UEM.TOTL.ZS`
- Exports of goods and services (% of GDP) `NE.EXP.GNFS.ZS`
- Imports of goods and services (% of GDP) `NE.IMP.GNFS.ZS`
- Foreign direct investment, net inflows (% of GDP) `BX.KLT.DINV.WD.GD.ZS`
- Current account balance (% of GDP) `BN.CAB.XOKA.GD.ZS`

These indicators were selected because they jointly capture three important dimensions of the Argentine economy.

- **Domestic performance:** GDP growth and unemployment show changes in output and labour-market stress.
- **Price instability:** GDP deflator inflation reflects macroeconomic pressure in the price system.
- **External exposure:** exports, imports, FDI, and current account balance show the extent to which domestic conditions interact with trade and external financing.

This combination is analytically useful because it avoids an overly narrow dashboard. A dashboard based only on GDP or inflation would miss the way external adjustment, trade openness, and financing pressures contribute to economic instability.

### 2.3 Data Preparation and Structure

The dashboard uses a processed tidy file with the following fields:

- `country_name`
- `country_code`
- `indicator_name`
- `indicator_code`
- `topic`
- `unit`
- `year`
- `value`

This reshaping step was necessary because tidy data is much better suited to interactive visualisation. In Dash and Plotly, a long-format table supports filtering, chart switching, and multi-visual reuse more effectively than the original wide file. The dashboard also uses a second helper file containing the latest available value and year-on-year change for KPI cards.

The preparation workflow therefore involved:

1. downloading or reusing the official WDI ZIP
2. extracting the raw CSV files
3. filtering Argentina and the selected indicators
4. restricting the period to 2000-2024
5. reshaping the data into a tidy structure
6. producing a latest-snapshot helper data set for KPI cards

This workflow is appropriate because it preserves the raw data source while creating a cleaner analytical layer for visualisation.

### 2.4 Interesting Attributes of the Data

Several features of the data set are especially relevant for visual analysis.

First, the data spans a sufficiently long period to show multiple economic phases rather than a single short episode. This makes it possible to compare crisis years, recovery years, and more stable years within a single analytical framework.

Second, the selected indicators have **mixed units**:

- percentages
- percentages of GDP
- current US dollars

This characteristic is important because it affects which visualisations are appropriate. Some indicators can be shown directly in time-series charts, while others cannot be compared in raw form within the same chart without misleading the viewer. This is why the dashboard uses standardisation in the "Latest Position vs Historical Norm" chart and normalization in the heatmap.

Third, the data is thematically broad. It includes domestic performance, price pressure, labour conditions, trade openness, and external financing. This breadth supports a richer dashboard because it allows the analysis to move beyond one-dimensional commentary.

Finally, Argentina itself is an interesting case because the data contains clear turning points. This makes annotations, phase-based interpretation, and crisis markers genuinely meaningful rather than decorative.

### 2.5 Data Limitations

Although the WDI data set is strong, it also has limitations that need to be recognised [1,3].

- The frequency is annual rather than monthly or quarterly, so short-term volatility is smoothed.
- The indicators do not all measure the same type of phenomenon, which means direct raw comparison across charts can be misleading.
- Some values in WDI may reflect modelled estimates or harmonised series rather than purely direct observations.
- GDP in current US dollars is nominal and therefore affected by inflation and exchange-rate movements as well as real output changes.
- The GDP deflator is a useful inflation proxy for complete time coverage, but it is not the same as consumer price inflation and should not be interpreted as a household cost-of-living measure.

Identifying these limitations is important because it justifies the visual design choices used in the dashboard. For example, the mixed-unit problem explains why the heatmap is normalized within each indicator and why the latest-position chart uses z-scores rather than raw values.

## 3. Visualisations and Analysis

### 3.1 Figure 1: KPI Summary Cards

The KPI cards provide a concise summary of the latest available values for six core indicators: GDP growth, inflation, unemployment, exports, imports, and FDI. This visual form is appropriate because dashboard users need an immediate overview before examining historical trends in detail. The cards therefore serve as the first analytical layer in the dashboard.

The cards are useful because they answer a simple but important question: what does Argentina look like at the latest observation? In this dashboard, the answer is that the macroeconomic picture remains pressured. Inflation is elevated, growth remains weak, and external-sector indicators are needed to interpret whether current conditions are purely domestic or linked to wider external adjustment.

The KPI design also supports clarity by separating current level from historical trend. Rather than forcing a time series into a compact space, the cards act as a headline summary and direct the viewer to the more detailed visuals below.

### 3.2 Figure 2: GDP Growth Cycle

The GDP growth visual uses a line chart because GDP growth is a time-series indicator and the main analytical aim is to show contraction, rebound, and turning points. A line chart is the most suitable form for this task because it reveals sequence, direction, and volatility more clearly than bars or summary cards.

This chart shows that Argentina's economic path is highly cyclical. The 2001-2002 crisis produces a severe contraction, followed by recovery, while the 2020 pandemic shock creates a later collapse in output. Negative-growth years are highlighted to make recession periods more visible, and annotations are used to identify important turning points rather than leaving the interpretation entirely to the reader.

The intended analytical message is that Argentina should not be understood as an economy with steady incremental growth. Instead, growth performance is interrupted by major shocks, and recovery needs to be interpreted as part of a broader cycle rather than as evidence of stable long-run progression.

### 3.3 Figure 3: GDP Scale Over Time

The GDP scale chart uses an area chart in current US dollars to show the changing size of the economy over time. This visual complements the GDP growth chart. Whereas GDP growth highlights rate of change, the GDP scale chart highlights magnitude. Using a visually distinct area chart avoids repeating the same design while reinforcing a different analytical point.

The chart shows that Argentina remains a large economy in nominal scale even when growth performance is unstable. This distinction matters. A country can have a large economy and still experience severe macroeconomic instability. The visual therefore prevents the reader from equating economic size with economic stability.

Expressing GDP in billions of current US dollars improves readability and makes the chart more suitable for dashboard presentation. It also reinforces the need to interpret the visual carefully, since nominal GDP can rise even when underlying macroeconomic conditions remain fragile.

### 3.4 Figure 4: Inflation and Unemployment

This chart compares GDP deflator inflation with unemployment using a dual-axis line chart. The choice of a dual-axis format is justified because both indicators are central to macroeconomic stability, but their scales differ substantially. A single shared axis would make one series visually unreadable.

The chart shows that recent Argentine stress is driven especially strongly by price instability. Unemployment matters, but the inflation series diverges much more sharply in recent years. This distinction is important because it highlights that macroeconomic deterioration is not only about labour-market weakness. The inflation surge represents a broader destabilisation of the economic environment.

The GDP deflator was selected instead of consumer price inflation because it provided complete historical coverage across the chosen period in the available WDI extract [1,2]. This should be understood as an informed substitution rather than an identical measure. The visual still succeeds analytically because the purpose is to show broad price-system instability over time.

### 3.5 Figure 5: Trade Openness Profile

The trade chart compares exports and imports directly as shares of GDP using two lines. This is a more appropriate design than a stacked area chart because the main analytical goal is comparison rather than cumulative composition. The viewer can therefore judge whether exports and imports move together, diverge, or adjust differently during stress periods.

This visual supports the dashboard's second theme, trade and openness. It shows that Argentina's external-sector position changes over time and that widening distance between exports and imports can reveal periods of external adjustment or changing exposure. In other words, the domestic macro story cannot be fully understood without reference to the external sector.

The visual is also useful because it keeps the trade indicators in the same unit, `% of GDP`, which makes direct comparison valid without additional transformation.

### 3.6 Figure 6: Growth-Inflation Regime Map

The bubble chart plots GDP growth on one axis and GDP deflator inflation on the other, while bubble size represents GDP scale. This chart was chosen because it provides a more relational form of analysis than a standard time-series plot. It allows the viewer to examine how years cluster into broad macroeconomic regimes rather than only how one variable changes over time.

The color scheme groups years into:

- crisis
- recovery
- recent instability
- baseline

This is analytically useful because it gives structure to the relationship between growth and inflation. Instead of treating every year as a disconnected point, the chart suggests that Argentina's macroeconomic history can be interpreted as movement across distinct regimes. Crisis years tend to combine weak growth with stress, recovery years occupy a different part of the chart, and recent instability appears as a separate configuration with very high inflation pressure.

This visual is especially valuable because it supports inference. It encourages the viewer to think about clusters, exceptions, and transitions, which is closer to analytical reasoning than simple descriptive display.

### 3.7 Figure 7: Latest Position vs Historical Norm

This horizontal bar chart shows how unusual the latest available values are relative to Argentina's own recent history. The indicators are standardized using z-scores, so each value is expressed as its distance from its own historical mean. This design was necessary because the dashboard includes mixed units that cannot be compared directly in raw form.

The visual is effective because it avoids a common dashboard mistake: comparing values with different units on the same raw scale. By standardising each series, the chart instead asks a more meaningful question: which indicators are currently most unusual relative to their own historical behaviour?

This makes the chart particularly useful for identifying current pressure points. It also demonstrates a better understanding of the data's properties, because the visual model has been adapted to the structure of the indicators rather than forcing them into an invalid comparison.

### 3.8 Figure 8: Indicator Heatmap

The heatmap provides a compact summary of all indicators across the 2000-2024 period. Each indicator is normalized to its own history so that mixed units remain comparable. This makes the heatmap one of the most analytically powerful visuals in the dashboard, because it allows multiple indicators and multiple years to be considered together without collapsing them into a single summary number.

The purpose of the heatmap is to reveal periods in which several indicators simultaneously depart from their usual levels. Crisis markers are included to draw attention to key years, but the main value of the chart lies in pattern recognition. The viewer can identify whether stress is concentrated in one indicator, one period, or across the system more broadly.

This chart is particularly effective for dashboard analysis because it models the mixed-unit problem appropriately. Rather than pretending GDP in dollars, inflation in percentages, and current account balance as a share of GDP are directly comparable, the heatmap compares each series against its own baseline. That design choice makes the visual more defensible and better aligned with the properties of the data.

## 4. Conclusion

The dashboard shows that Argentina's economic performance between 2000 and 2024 is best understood as a combination of instability, adjustment, and uneven recovery. GDP growth identifies repeated contraction and rebound cycles, inflation highlights severe price-system stress, unemployment adds labour-market context, and the trade and external-sector indicators show that domestic conditions are closely tied to external exposure.

The WDI data set was an appropriate source because it offered broad coverage, consistent definitions, and enough historical depth to support a multi-panel dashboard [1,3]. At the same time, the report has identified important limitations, including annual frequency, mixed units, nominal measures, and the use of GDP deflator inflation as a proxy for price pressure. These limitations were not ignored; instead, they directly informed the visual design choices used in the dashboard.

Overall, the dashboard supports the conclusion that Argentina's economy cannot be adequately described by one headline number. A more convincing interpretation emerges only when growth, prices, labour conditions, trade, and external balance are examined together. The dashboard therefore succeeds not only as a technical visualisation exercise, but also as a structured analytical account of Argentina's modern economic instability and recovery cycles.

## 5. References

1. World Bank. World Development Indicators [Internet]. Washington (DC): World Bank; [cited 2026 Apr 6]. Available from: https://datatopics.worldbank.org/world-development-indicators/
2. World Bank. WDI bulk CSV download [Internet]. Washington (DC): World Bank; [cited 2026 Apr 6]. Available from: https://databank.worldbank.org/data/download/WDI_CSV.zip
3. World Bank. About the indicators API documentation [Internet]. Washington (DC): World Bank; [cited 2026 Apr 6]. Available from: https://datahelpdesk.worldbank.org/knowledgebase/articles/889392-about-the-indicators-api-documentation
