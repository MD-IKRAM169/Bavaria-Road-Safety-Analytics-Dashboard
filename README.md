# Road Accident Analysis — Power BI Dashboard

**Power BI · Road safety analytics · 2026**

This repository contains an existing Microsoft Power BI dashboard project, its Excel dataset and design resources in [ROAD ACCIDENT.zip](ROAD%20ACCIDENT.zip). The source materials have now been inspected rather than described from the filename alone.

> **Important geography note:** Although this repository is named *Bavaria Road Safety Analytics Dashboard*, the Excel file contains local-authority labels such as **Birmingham, Leeds, Manchester, Kensington and Chelsea, and Highland**, alongside UK police-force names and geographic coordinates. These records represent **Great Britain / UK locations, not verified Bavaria data**. The original repository name is retained for continuity until the owner decides whether to rename it.

## Verified project overview

| Property | Finding from the original files |
| --- | --- |
| Dashboard software | **Microsoft Power BI Desktop** |
| Editable report | **Road_Accident_Analysing_Model.pbix** |
| Data source | **Road Accident Data.xlsx**, worksheet **Data** |
| Data size | **307,973 records**, **21 fields**, plus a header row |
| Stored dates | **2021–2022** using the standard Excel 1900-date convention |
| Report pages | **1**, with KPI cards, category charts, map and slicers |
| Original project | **ROAD ACCIDENT.zip** (preserved unchanged) |
| Design assets | PPTX/JPG Power BI background and 11 PNG images |

## Dashboard visuals

The Power BI report metadata identifies the following components:

- KPI cards referring to **CY Accident**, **CY Casualties** and **YOY Casualities** measures.
- A **monthly stacked-area chart** using casualty totals and a year hierarchy.
- Donut charts for **urban versus rural** area and **light conditions**.
- A bar chart of **casualties by road type**.
- A **map** of longitude/latitude and local-authority district with casualty and vehicle tooltips.
- Weather-condition and road-surface-condition **slicers**.
- A vehicle-type card, image decorations and a report title.

See [Power BI audit](docs/POWER_BI_AUDIT.md) for the exact data-field references. The report has not been opened or refreshed in Power BI Desktop during this review, so final rendered KPI values and DAX formula definitions remain unverified.

## How to use the project

1. Download [ROAD ACCIDENT.zip](ROAD%20ACCIDENT.zip) and extract it locally.
2. Open **ROAD ACCIDENT/Road_Accident_Analysing_Model.pbix** in **Power BI Desktop**.
3. If prompted to reconnect data, update the workbook path to **ROAD ACCIDENT/Road Accident Data.xlsx** in Power Query / data source settings, and refresh.
4. Inspect the dashboard and filters, then verify metrics against the original data and its definitions.

For extraction and inspection instructions see [Getting started](docs/GETTING_STARTED.md).

## Source data — quality considerations

| Workbook audit | Observed value |
| --- | ---: |
| 2021 data rows | 163,554 |
| 2022 data rows | 144,419 |
| Distinct accident record IDs | 307,973 |
| Distinct local-authority names | 422 |
| Distinct police-force names | 51 |

**Two issues need investigation before you publish statistical findings:**

1. The stored **Day_of_Week** does not match the weekday implied by **Accident Date** for **307,973 out of 307,973** records (assuming standard Excel serial dates). This suggests a systemic date-conversion or alignment problem, so temporal charts require verification.
2. **Accident_Severity** contains **49 records labeled “Fetal”** as well as **3,904 records labeled “Fatal”**. The source must confirm whether that is a typo; the original data has not been modified.

The upstream dataset provider and original usage rights have **not been verified**. See [Workbook data audit](docs/DATA_AUDIT.md). Counts here describe the supplied file only, not certified government statistics.

## Project structure

~~~text
Bavaria-Road-Safety-Analytics-Dashboard/
├── ROAD ACCIDENT.zip
├── README.md
├── LICENSE
├── docs/
│   ├── GETTING_STARTED.md
│   ├── POWER_BI_AUDIT.md
│   ├── DATA_AUDIT.md
│   └── PUBLISHING_CHECKLIST.md
├── tools/
│   ├── archive_inventory.py
│   └── inspect_pbix.py
├── tests/
└── .github/workflows/quality.yml
~~~

Both metadata tools use Python's standard library. To inspect the ZIP and PBIX without executing the dashboard:

~~~bash
python tools/archive_inventory.py "ROAD ACCIDENT.zip" --output archive-inventory.json --sha256
python tools/inspect_pbix.py "ROAD ACCIDENT.zip" --output pbix-layout.json
python -m unittest discover -s tests -v
~~~

## Next steps

- [x] Inspect the real archive, workbook and Power BI layout.
- [x] Document verified visuals, table structure and data-quality risks.
- [x] Add a metadata inspection utility and automated tests.
- [ ] Decide whether to **rename the repository** to match the Great Britain / UK data or use an actual Bavaria dataset.
- [ ] Record the authoritative data source, licensing terms and query/data transformations.
- [ ] Investigate weekday/date mismatch and the severity spelling issue.
- [ ] Export a **real screenshot** from Power BI Desktop after confirming the report displays correctly.
- [ ] Validate DAX measures, geographic coverage and published analytical findings.

**License:** This repository includes Apache-2.0, but datasets, maps and third-party images may have separate redistribution requirements.
