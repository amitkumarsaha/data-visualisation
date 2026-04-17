from __future__ import annotations

import shutil
from pathlib import Path
from urllib.request import urlretrieve
from zipfile import BadZipFile, ZipFile, is_zipfile

import pandas as pd

from src.config import (
    ARGENTINA_SNAPSHOT_PATH,
    ARGENTINA_TIDY_PATH,
    COUNTRY_CODE,
    COUNTRY_NAME,
    END_YEAR,
    INDICATORS,
    INDICATOR_ORDER,
    PROCESSED_DATA_DIR,
    RAW_DATA_DIR,
    RAW_WDI_PATH,
    START_YEAR,
    YEAR_COLUMNS,
    WDI_ZIP_URL,
    RAW_WDI_ZIP_PATH,
)


def load_wdi_data(path: Path = RAW_WDI_PATH) -> pd.DataFrame:
    return pd.read_csv(path, low_memory=False)


def filter_argentina_indicators(df: pd.DataFrame) -> pd.DataFrame:
    return df.loc[
        (df["Country Code"] == COUNTRY_CODE)
        & (df["Indicator Code"].isin(INDICATOR_ORDER)),
        ["Country Name", "Country Code", "Indicator Name", "Indicator Code", *YEAR_COLUMNS],
    ].copy()


def reshape_to_tidy(df: pd.DataFrame) -> pd.DataFrame:
    tidy = df.melt(
        id_vars=["Country Name", "Country Code", "Indicator Name", "Indicator Code"],
        value_vars=YEAR_COLUMNS,
        var_name="year",
        value_name="value",
    )
    tidy["year"] = tidy["year"].astype(int)
    tidy["value"] = pd.to_numeric(tidy["value"], errors="coerce")
    tidy = tidy.dropna(subset=["value"])
    tidy = tidy.loc[tidy["year"].between(START_YEAR, END_YEAR)].copy()
    return tidy


def enrich_with_metadata(df: pd.DataFrame) -> pd.DataFrame:
    enriched = df.rename(
        columns={
            "Country Name": "country_name",
            "Country Code": "country_code",
            "Indicator Name": "indicator_name",
            "Indicator Code": "indicator_code",
        }
    ).copy()

    enriched["country_name"] = COUNTRY_NAME
    enriched["topic"] = enriched["indicator_code"].map(
        lambda code: INDICATORS[code]["topic"]
    )
    enriched["unit"] = enriched["indicator_code"].map(lambda code: INDICATORS[code]["unit"])
    enriched["indicator_name"] = enriched["indicator_code"].map(
        lambda code: INDICATORS[code]["name"]
    )

    column_order = [
        "country_name",
        "country_code",
        "indicator_name",
        "indicator_code",
        "topic",
        "unit",
        "year",
        "value",
    ]
    enriched = enriched[column_order]
    enriched["indicator_code"] = pd.Categorical(
        enriched["indicator_code"], categories=INDICATOR_ORDER, ordered=True
    )
    enriched = enriched.sort_values(["indicator_code", "year"]).reset_index(drop=True)
    enriched["indicator_code"] = enriched["indicator_code"].astype(str)
    return enriched


def build_latest_snapshot(df: pd.DataFrame) -> pd.DataFrame:
    rows = []

    for indicator_code in INDICATOR_ORDER:
        indicator_df = df.loc[df["indicator_code"] == indicator_code].sort_values("year")
        if indicator_df.empty:
            continue

        latest_row = indicator_df.iloc[-1]
        previous_df = indicator_df.loc[indicator_df["year"] < latest_row["year"]]
        previous_row = previous_df.iloc[-1] if not previous_df.empty else None

        latest_value = float(latest_row["value"])
        previous_value = float(previous_row["value"]) if previous_row is not None else None
        absolute_change = (
            latest_value - previous_value if previous_value is not None else None
        )
        percent_change = (
            (absolute_change / abs(previous_value) * 100)
            if previous_value not in (None, 0)
            else None
        )

        rows.append(
            {
                "indicator_name": latest_row["indicator_name"],
                "indicator_code": indicator_code,
                "topic": latest_row["topic"],
                "unit": latest_row["unit"],
                "latest_year": int(latest_row["year"]),
                "latest_value": latest_value,
                "previous_year": int(previous_row["year"]) if previous_row is not None else None,
                "previous_value": previous_value,
                "absolute_change": absolute_change,
                "percent_change": percent_change,
            }
        )

    snapshot = pd.DataFrame(rows)
    snapshot["indicator_code"] = pd.Categorical(
        snapshot["indicator_code"], categories=INDICATOR_ORDER, ordered=True
    )
    snapshot = snapshot.sort_values("indicator_code").reset_index(drop=True)
    snapshot["indicator_code"] = snapshot["indicator_code"].astype(str)
    return snapshot


def build_processed_datasets() -> tuple[pd.DataFrame, pd.DataFrame]:
    raw = load_wdi_data()
    filtered = filter_argentina_indicators(raw)
    tidy = enrich_with_metadata(reshape_to_tidy(filtered))
    snapshot = build_latest_snapshot(tidy)
    return tidy, snapshot


def save_processed_datasets() -> tuple[Path, Path]:
    PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)
    tidy, snapshot = build_processed_datasets()
    tidy.to_csv(ARGENTINA_TIDY_PATH, index=False)
    snapshot.to_csv(ARGENTINA_SNAPSHOT_PATH, index=False)
    return ARGENTINA_TIDY_PATH, ARGENTINA_SNAPSHOT_PATH


def download_full_wdi_zip(
    url: str = WDI_ZIP_URL,
    destination: Path = RAW_WDI_ZIP_PATH,
    force: bool = False,
) -> Path:
    destination.parent.mkdir(parents=True, exist_ok=True)
    if destination.exists() and not force:
        print(f"Reusing existing WDI ZIP: {destination}")
        return destination
    print(f"Downloading WDI ZIP from {url}")
    urlretrieve(url, destination)
    print(f"Download complete: {destination}")
    return destination


def ensure_valid_wdi_zip(zip_path: Path = RAW_WDI_ZIP_PATH, force_redownload: bool = False) -> Path:
    if force_redownload and zip_path.exists():
        print(f"Removing invalid WDI ZIP: {zip_path}")
        zip_path.unlink()

    if not zip_path.exists():
        return download_full_wdi_zip(force=True)

    if not is_zipfile(zip_path):
        print(f"Existing WDI ZIP is invalid: {zip_path}")
        zip_path.unlink(missing_ok=True)
        return download_full_wdi_zip(force=True)

    return zip_path


def extract_full_wdi_zip(
    zip_path: Path = RAW_WDI_ZIP_PATH,
    extract_dir: Path = RAW_DATA_DIR,
    normalised_dir: Path = RAW_DATA_DIR,
    force: bool = False,
) -> Path:
    zip_path = ensure_valid_wdi_zip(zip_path)

    extracted_source_dir = extract_dir / "WDI_csv"
    if force:
        print("Clearing previous extracted WDI files")
        shutil.rmtree(extracted_source_dir, ignore_errors=True)
        shutil.rmtree(normalised_dir, ignore_errors=True)

    print(f"Extracting WDI ZIP to {extract_dir}")
    try:
        with ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall(extract_dir)
    except BadZipFile as exc:
        print("ZIP validation failed during extraction, retrying download once")
        zip_path = ensure_valid_wdi_zip(zip_path, force_redownload=True)
        with ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall(extract_dir)

    if extracted_source_dir.exists():
        if normalised_dir.exists():
            shutil.rmtree(normalised_dir)
        shutil.move(str(extracted_source_dir), str(normalised_dir))
    print(f"Extraction complete: {normalised_dir}")

    return normalised_dir


def initialise_dashboard_data(force_download: bool = False) -> tuple[Path, Path]:
    print("Initialising dashboard data")
    if force_download:
        download_full_wdi_zip(force=True)
    else:
        ensure_valid_wdi_zip()
    extract_full_wdi_zip(force=force_download)
    print("Building processed Argentina dashboard datasets")
    tidy_path, snapshot_path = save_processed_datasets()
    print(f"Dataset preparation complete:\n- {tidy_path}\n- {snapshot_path}")
    return tidy_path, snapshot_path


if __name__ == "__main__":
    tidy_path, snapshot_path = initialise_dashboard_data()
    print(f"Saved tidy data to {tidy_path}")
    print(f"Saved snapshot data to {snapshot_path}")
