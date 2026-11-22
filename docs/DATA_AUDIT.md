# Excel data audit: findings and limitations

**File:** ROAD ACCIDENT.zip → ROAD ACCIDENT/Road Accident Data.xlsx, worksheet **Data**.

All observations below derive from a read-only scan of the submitted workbook. They are **not independently verified against an official public dataset**.

## Verified workbook profile

| Item | Observation |
| --- | ---: |
| Rows including header | 307,974 |
| Data records | **307,973** |
| Columns | **21** (A–U) |
| Distinct Accident_Index values | 307,973 |
| Interpreted dates | 2021-01-01 through 2022-12-31 |
| Data rows dated 2021 | 163,554 |
| Data rows dated 2022 | 144,419 |
| Distinct local authorities | 422 |
| Distinct police forces | 51 |
| Distinct vehicle types | 15 |
| Latitude range | 49.914488 to 60.598055 |
| Longitude range | −7.516225 to 1.759398 |

The date interpretation assumes Excel's standard 1900 date system. The workbook includes accident date, weekday, severity, coordinates, district, police force, weather, surface, road type, casualty count and vehicle count fields.

## Geography does not match the repository name

The district labels include Birmingham, Leeds, Manchester, Kensington and Chelsea, Cornwall, Westminster and Highland; police forces include Metropolitan Police, West Midlands and Greater Manchester. The coordinates and place labels **indicate UK / Great Britain coverage, not Bavaria**.

The upstream source and exact coverage terms are not identified in the archive, so this should not be presented as a Bavarian accident dataset without different source material.

## Data-quality flags

| Check | Finding | Action |
| --- | --- | --- |
| Accident Date vs Day_of_Week | **307,973/307,973** rows have inconsistent weekday labels under standard Excel-date conversion | Check source format, day offset and Power Query transformations before interpreting time trends |
| Severity category | Slight **263,280**, Serious **40,740**, Fatal **3,904**, **Fetal 49** | Confirm whether Fetal is a data entry/classification error; do not silently relabel |
| Missing values | **3** blanks in Carriageway_Hazards; **17** blanks in Time | Define a missing-data treatment |
| Provider / dataset license | Not verified | Record authoritative source link, release version and reuse permissions |

A raw sum of the Number_of_Casualties column is **417,883**, but this has not been checked against authoritative published statistics or the Power BI DAX calculations. Do not present it as an official national statistic.

## Suggested validation workflow

1. Locate the original dataset provider and documentation.
2. Verify the intended geography, time convention, unique key definition and severity categories.
3. Determine why Accident Date and Day_of_Week differ throughout the workbook.
4. Compare DAX measures to direct workbook calculations after corrections.
5. Save a *new versioned and documented* cleaned dataset, keeping the original ZIP for provenance.
6. Review data-licensing and privacy restrictions before publishing extracted records.

**Do not correct the source dataset silently.** Any cleaning decisions should be explained and reproducible.
