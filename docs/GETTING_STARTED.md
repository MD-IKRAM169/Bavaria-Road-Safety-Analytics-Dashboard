# Getting started with the actual project

The original [ROAD ACCIDENT.zip](../ROAD%20ACCIDENT.zip) contains the complete original project folder:

~~~text
ROAD ACCIDENT/
├── Road_Accident_Analysing_Model.pbix
├── Road Accident Data.xlsx
├── Background For Power BI Project.pptx
├── Background For Power BI Project.jpg
└── png/  (11 image assets)
~~~

## Open the report

1. Download and safely extract the original ZIP.
2. Use Microsoft **Power BI Desktop** to open **Road_Accident_Analysing_Model.pbix**.
3. If the Excel data-source path no longer exists, update it to the included **Road Accident Data.xlsx** in Power Query or data-source settings, then refresh.
4. Inspect the report page, filters, DAX measures and map visual.
5. Export a real screenshot **after** loading the report (the JPG background alone is not a dashboard screenshot).
6. Review [Data Audit](DATA_AUDIT.md) before publishing numeric results. The data is UK/Great Britain-geographic despite the Bavaria repository name, and weekdays conflict with stored dates.

The report was not run in Power BI Desktop during this repository review; model refresh and final displayed measures have not been verified.

## Without Power BI: metadata tools

Python 3.10+ and standard-library modules are sufficient:

~~~bash
python tools/archive_inventory.py "ROAD ACCIDENT.zip" --output archive-inventory.json --sha256
python tools/inspect_pbix.py "ROAD ACCIDENT.zip" --output pbix-layout.json
python -m unittest discover -s tests -v
~~~

The tools do not extract or execute arbitrary files, decode the binary data model or render Power BI visuals. They are **not malware scanners**.
