# Dashboard portfolio publishing checklist

The original project ZIP is preserved. Review the source archive before converting it into a public, editable project repository.

## Phase 1 — project inventory

- [ ] Run `python tools/archive_inventory.py "ROAD ACCIDENT.zip" --output archive-inventory.json --sha256`
- [ ] Record actual files, formats, tools used and the project entry point.
- [ ] Verify whether the archive includes raw data, screenshots, reports, dashboard project files or executable code.
- [ ] Confirm nothing contains sensitive contact details, credentials, restricted information or license violations.

## Phase 2 — technical reproducibility

- [ ] Move reusable editable project files into a descriptive folder, retaining original filenames where appropriate.
- [ ] Document application version, extensions, dependencies and any environment-specific data connections.
- [ ] Add a minimal sample dataset **only if redistribution is permitted**.
- [ ] Include refresh instructions for local file paths and BI connections.
- [ ] Confirm the dashboard opens on a clean environment without private credentials.

## Phase 3 — analytical documentation

- [ ] Verify provider, source URL, dataset version, years, districts and fields.
- [ ] Document transformations, filters, exclusions and metric formulas.
- [ ] Export real dashboard screenshots, with descriptive captions and alt text.
- [ ] Include **only verified** findings with caveats about uncertainty and population exposure.
- [ ] Credit external maps, icons, images and basemaps according to their usage terms.

## Phase 4 — publication

- [ ] Update README to identify the confirmed dashboard tool and how to open it.
- [ ] Add a meaningful overview screenshot to the README.
- [ ] Attach a release with the editable project artifact if it is too large for ordinary source control.
- [ ] Confirm the license applies to your original work; distinguish third-party data and visual assets.
- [ ] Run the project's tests and manually open the dashboard before labeling a release stable.

**Next needed evidence:** a copy of the extracted dashboard file(s), a project screenshot, and provenance for the source data. Without these, project-specific feature claims should not be added.
