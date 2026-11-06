"""
Download the raw data for this project from the World Bank API.

Run from the repository root:
    python src/get_data.py

Output:
    data/raw/worldbank_raw.csv   one row per country-year, one column per indicator
    data/raw/countries.csv       country metadata (region, income group)

Only real countries are kept: World Bank aggregates such as "World" or
"Euro area" are dropped using the country metadata (aggregates have region "Aggregates").
"""

from pathlib import Path

import pandas as pd
import requests

BASE_URL = "https://api.worldbank.org/v2"
START_YEAR, END_YEAR = 1960, 2024

# World Bank indicator code -> short column name used in the rest of the project
INDICATORS = {
    "SP.DYN.TFRT.IN": "fertility",          # births per woman
    "NY.GDP.PCAP.KD": "gdp_pc",             # GDP per capita, constant 2015 US$
    "SE.SEC.ENRR.FE": "female_sec_enrol",   # secondary school enrolment, female (% gross)
    "SP.URB.TOTL.IN.ZS": "urban_pct",       # urban population (% of total)
    "SP.DYN.IMRT.IN": "infant_mortality",   # infant deaths per 1,000 live births
    "SL.TLF.CACT.FE.ZS": "female_lfp",      # female labour force participation (% ages 15+)
}

RAW_DIR = Path(__file__).resolve().parents[1] / "data" / "raw"


def fetch_indicator(code: str) -> pd.DataFrame:
    """Download one indicator for all countries and years, return long-format DataFrame."""
    url = f"{BASE_URL}/country/all/indicator/{code}"
    params = {"format": "json", "date": f"{START_YEAR}:{END_YEAR}", "per_page": 20000}
    rows, page, pages = [], 1, 1
    while page <= pages:
        resp = requests.get(url, params={**params, "page": page}, timeout=60)
        resp.raise_for_status()
        meta, data = resp.json()
        pages = meta["pages"]
        for r in data or []:
            rows.append({"iso3": r["countryiso3code"], "year": int(r["date"]), "value": r["value"]})
        page += 1
    return pd.DataFrame(rows)


def fetch_countries() -> pd.DataFrame:
    """Country metadata; used to drop aggregates and to label regions/income groups."""
    resp = requests.get(f"{BASE_URL}/country", params={"format": "json", "per_page": 400}, timeout=60)
    resp.raise_for_status()
    _, data = resp.json()
    df = pd.DataFrame(
        {
            "iso3": c["id"],
            "country": c["name"],
            "region": c["region"]["value"],
            "income_group": c["incomeLevel"]["value"],
        }
        for c in data
    )
    return df[df["region"] != "Aggregates"].reset_index(drop=True)


def main() -> None:
    RAW_DIR.mkdir(parents=True, exist_ok=True)

    countries = fetch_countries()
    countries.to_csv(RAW_DIR / "countries.csv", index=False)
    print(f"countries: {len(countries)}")

    frames = []
    for code, name in INDICATORS.items():
        df = fetch_indicator(code)
        df = df.rename(columns={"value": name}).set_index(["iso3", "year"])
        frames.append(df)
        print(f"{name:18s} {df[name].notna().sum():6d} non-missing values")

    wide = pd.concat(frames, axis=1).reset_index()
    wide = wide[wide["iso3"].isin(countries["iso3"])]          # drop aggregates
    wide = wide.merge(countries, on="iso3", how="left")
    wide = wide.sort_values(["iso3", "year"])
    wide.to_csv(RAW_DIR / "worldbank_raw.csv", index=False)
    print(f"saved {len(wide)} country-year rows to {RAW_DIR / 'worldbank_raw.csv'}")


if __name__ == "__main__":
    main()
