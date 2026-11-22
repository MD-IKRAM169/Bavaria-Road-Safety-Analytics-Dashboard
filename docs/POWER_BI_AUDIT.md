# Power BI report: inspected layout and features

**Source:** Original upload, ROAD ACCIDENT.zip → ROAD ACCIDENT/Road_Accident_Analysing_Model.pbix

The report contains **one page** named **Page 1**, with a **1280 × 720** design canvas. Its Report/Layout metadata contains **31 visual containers**; 26 declare a visual type. This report has **not been rendered in Power BI Desktop**, so metadata alone cannot verify the displayed values.

| Visual | Data fields from report metadata |
| --- | --- |
| KPI cards | Data.CY Accident; Data.CY Casualties; Data.YOY Casualities |
| Multi-row card | Data.Vehicle_Type (groups); Data.CY Casualties |
| Stacked-area chart | Calender.Month; Sum(Data.Number_of_Casualties); year hierarchy |
| Donut chart | Data.Urban_or_Rural_Area; Data.CY Casualties |
| Donut chart | Data.Light_Conditions (groups); Data.CY Casualties |
| Bar chart | Data.Road_Type; Sum(Data.Number_of_Casualties) |
| Map | Data.Longitude; Data.Latitude; Data.Local_Authority_(District); sums of casualties and vehicles as tooltips |
| Slicer | Data.Weather_Conditions (groups) |
| Slicer | Data.Road_Surface_Conditions (groups) |

Other elements include six image visuals and textboxes, including the title **ROAD ACCIDENT ANALYSIS**.

The field spellings **YOY Casualities** and **Calender** are reproduced from the report. Do not rename them without updating related DAX and Power BI relationships.

## What's included in the original ZIP

- Road_Accident_Analysing_Model.pbix (Power BI report; ~15 MB)
- Road Accident Data.xlsx (Excel workbook; ~36 MB)
- Background For Power BI Project.pptx and .jpg
- 11 PNG icons/illustrations

Only the project archive is tracked as a large binary file. We do not duplicate its images, report or workbook as separately committed files.

## Inspect the PBIX metadata

~~~bash
python tools/inspect_pbix.py "ROAD ACCIDENT.zip" --output pbix-layout.json
~~~

This command reads the metadata safely without extracting or executing the binary Power BI data model. It does **not** verify measures, refresh the dataset, generate dashboard screenshots or reconstruct Power Query transformations.
