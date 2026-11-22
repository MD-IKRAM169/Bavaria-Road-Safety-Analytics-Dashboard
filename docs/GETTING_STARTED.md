# Getting started with the existing project archive

The original repository stored its materials as one file named `ROAD ACCIDENT.zip`. Its internal files have not yet been verified by this documentation update.

## 1. Download and inspect

On the [repository homepage](https://github.com/MD-IKRAM169/Bavaria-Road-Safety-Analytics-Dashboard), open `ROAD ACCIDENT.zip` and download it. Alternatively, after cloning the repository, keep the existing ZIP where it is.

Install Python 3.10+ if needed, then run from the repository root:

~~~bash
python tools/archive_inventory.py "ROAD ACCIDENT.zip" --output archive-inventory.json --sha256
~~~

The script reads only ZIP *metadata*: member names, counts, sizes and file types. It does **not** extract archive members or execute programs. Review warnings about unsafe file paths, symlinks, duplicates, encryption and unusually compressed files. This is **not** a complete malware scan.

## 2. Extract carefully

Only extract archives from trusted sources. Inspect archive member paths before extraction. Prefer using your operating system's ZIP viewer or a trusted archiver that prevents path traversal. Avoid running executables, scripts or macros until you know their provenance.

## 3. Identify how to open the dashboard

After inspection, the following common extensions *may* indicate the tool to use. This list does **not** assert that any of these files exist in the archive:

| Extension found | Typically opened with |
| --- | --- |
| `.pbix`, `.pbit` | Microsoft Power BI Desktop |
| `.twb`, `.twbx` | Tableau Desktop / compatible Tableau application |
| `.ipynb` | Jupyter Notebook or JupyterLab |
| `.py` | Python and project-specific dependencies |
| `.r`, `.rmd`, `.qmd` | R / RStudio / Quarto as appropriate |
| `.xlsx` | Excel or compatible spreadsheet software |
| `.html` | Web browser (after reviewing file and script safety) |

Some formats reference external data sources, local file paths or credentials. Do not commit any secrets while repairing these links.

## 4. Make the project reproducible

Once you know the actual format, document required application versions, file locations, data source and refresh steps. Add genuine screenshots and verified results. Follow [PUBLISHING_CHECKLIST.md](PUBLISHING_CHECKLIST.md).
