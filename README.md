# Economic Dashboard of Argentina

This project contains a Python Dash dashboard for exploring Argentina's economic performance using the **World Bank World Development Indicators (WDI)** dataset.

The dashboard focuses on three connected themes:
- Macroeconomic stability
- Trade and openness
- Crisis and recovery

It uses a polished financial-terminal visual style and presents Argentina's economic trends across the `2000-2024` period.

## Features
- KPI cards for the latest key macroeconomic indicators
- GDP growth line chart
- GDP area chart
- GDP deflator inflation vs unemployment comparison chart
- Trade openness chart for exports and imports
- Bubble chart for growth and GDP deflator inflation regimes
- Treemap for thematic indicator summary
- Heatmap for cross-indicator historical patterns

## Data Source
Source: [World Bank World Development Indicators (WDI)](https://databank.worldbank.org/data/download/WDI_CSV.zip)

### Extracted raw files are expected in:
`data/raw/world-bank/wdi_csv/`

#### Important raw files:
- `WDICSV.csv`
- `WDISeries.csv`
- `WDICountry.csv`

### Processed files are generated in:
`data/processed/`

### Generated outputs:
- `argentina_macro_tidy.csv`
- `argentina_latest_snapshot.csv`

## Project Structure

```text
data-visualisation/
  requirements.txt
  README.md
  data/
    raw/
      world-bank/
        WDI_CSV.zip
  src/
    app.py
    config.py
    init_data.py
    charts.py
    layout.py
```

## Requirements

- Python 3.10+
- `pip`

Install dependencies with:

```bash
pip install -r requirements.txt
```

## How To Run

1. Install the project dependencies.
2. Run the one-time data initialisation step:

```bash
python -m src.init_data
```

This setup step will:
- download the full WDI ZIP from the World Bank source only if it is not already present in `data/raw/world-bank/`
- extract it into `data/raw/world-bank/wdi_csv/`
- prepare the processed Argentina dashboard datasets in `data/processed/`

**NOTE:**
If the full WDI ZIP does not exist or automated download fails, manually download the file from [World Bank WDI ZIP](https://databank.worldbank.org/data/download/WDI_CSV.zip)
and place it in `data/raw/world-bank/` and  rerun:

```bash
python -m src.init_data
```


3. Start the dashboard:

```bash
python app.py
```

4. Open the local Dash URL shown in the terminal, usually:

`http://127.0.0.1:8050/`

## Data Processing

The dashboard depends on prepared Argentina-only processed CSV files.

Initialisation and processing steps:

- load the raw WDI dataset
- filter for Argentina only
- keep the selected economic indicators
- restrict the data to `2000-2024`
- reshape the data into long/tidy format
- generate a latest-value KPI snapshot

Run the setup and processing step with:

```bash
python -m src.init_data
```

## Selected Indicators
- GDP growth (annual %) `NY.GDP.MKTP.KD.ZG`
- GDP (current US$) `NY.GDP.MKTP.CD`
- Inflation, GDP deflator (annual %) `NY.GDP.DEFL.KD.ZG`
- Unemployment, total (% of total labor force) `SL.UEM.TOTL.ZS`
- Exports of goods and services (% of GDP) `NE.EXP.GNFS.ZS`
- Imports of goods and services (% of GDP) `NE.IMP.GNFS.ZS`
- Foreign direct investment, net inflows (% of GDP) `BX.KLT.DINV.WD.GD.ZS`
- Current account balance (% of GDP) `BN.CAB.XOKA.GD.ZS`

## Notes
- The raw WDI data is kept unchanged in wide format.
- The dashboard uses processed tidy data for easier filtering and chart generation.
- Indicator coverage in the processed dashboard dataset is aligned to the selected `2000-2024` series used in the app.

## Troubleshooting

If the dashboard does not start:

- make sure `python -m src.init_data` has been run at least once
- check that the processed CSV files exist in `data/processed/`
- make sure dependencies were installed successfully
- confirm that `python app.py` is being run from the project root

If processed files need to be regenerated, delete the files in `data/processed/` and run:

```bash
python -m src.init_data
```