# Does economic development explain fertility decline?

**Advanced Math project — Gajveer Singh (VUB)**

Website: _coming soon (GitHub Pages)_

## Question

Fertility has fallen in almost every country since 1960. Richer countries have fewer
children, but income moves together with education, urbanisation and child survival.

**Main question:** How much of the cross-country variation in fertility is explained by
income (GDP per capita), and does income still matter once we control for female
education, urbanisation and infant mortality?

**Sub-question:** Do countries today reach low fertility at lower income levels than
countries did in the past?

## Data

All data comes from the [World Bank World Development Indicators](https://data.worldbank.org/)
via its public API, 1960–2024, for all countries (regional aggregates removed).

| Column | Indicator | WB code |
|---|---|---|
| `fertility` | Births per woman | SP.DYN.TFRT.IN |
| `gdp_pc` | GDP per capita, constant 2015 US$ | NY.GDP.PCAP.KD |
| `female_sec_enrol` | Secondary enrolment, female (% gross) | SE.SEC.ENRR.FE |
| `urban_pct` | Urban population (% of total) | SP.URB.TOTL.IN.ZS |
| `infant_mortality` | Infant deaths per 1,000 live births | SP.DYN.IMRT.IN |
| `female_lfp` | Female labour force participation (%) | SL.TLF.CACT.FE.ZS |

To reproduce the dataset:

```bash
pip install -r requirements.txt
python src/get_data.py
```

## Analyses

1. **Regression** — fertility on log GDP per capita, then a multiple regression adding the
   other development indicators. _(in progress)_
2. **Second analysis** — _to be decided: clustering of development profiles, or comparing
   the income level at which countries crossed a fertility threshold over time._

## Main findings

_To be written._

## Repository structure

```
README.md            this file
requirements.txt     Python packages
data/raw/            raw World Bank downloads (created by src/get_data.py)
data/processed/      cleaned analysis dataset
src/get_data.py      downloads the raw data
notebooks/           analysis notebooks
figures/             exported figures (PDF)
docs/                website source (served by GitHub Pages)
```
