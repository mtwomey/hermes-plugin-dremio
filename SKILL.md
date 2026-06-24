---
name: dremio
description: >
  Dremio Cloud catalog navigation and SQL execution.
  Connects to the user's Prod project (405f90b7-8bc5-4c8d-aa6d-843f4e01dfcd).
tags: [dremio, dremio-cloud, sql, catalog, data-platform, data-science]
triggers:
  - "query Dremio"
  - "run SQL on Dremio"
  - "list Dremio catalogs"
  - "browse Dremio catalog"
  - "fetch schema from Dremio"
  - "navigate Dremio catalog tree"
  - "get Dremio dataset fields"
---

# Dremio Cloud Plugin

## Account Identity

- **Project:** Prod
- **Project ID:** 405f90b7-8bc5-4c8d-aa6d-843f4e01dfcd
- **API base:** `https://api.dremio.cloud/v0/projects/405f90b7-8bc5-4c8d-aa6d-843f4e01dfcd`
- **Credentials:** macOS Keychain, service `hermes-dremio-cloud`, keys `pat` + `project_id`
- **Setup:** `python ~/Git_Repos/hermes-plugin-dremio/setup.py credentials configure`

## Routing Note

Use this plugin for **all Dremio Cloud operations** (catalog browsing, schema inspection, SQL queries). For Databricks Unity Catalog, use the `databricks` plugin instead. For a side-by-side comparison, see the `databricks-dremio-comparison` skill.

## Common Patterns

| Task | Tool | Key params |
|------|------|-----------|
| Test connectivity | `dremio_ping` | - |
| List top-level sources/spaces | `dremio_catalog_list` | - |
| Browse a folder or source | `dremio_browse` | `path="Prod/src-staffing-crm/salesforce2/sfdc"` |
| Get column schema for a table | `dremio_get_schema` | `path="Prod/src-staffing-crm/salesforce2/sfdc/account"` |
| Run a SQL query | `dremio_run_sql` | `sql="SELECT ..."`, `max_rows=100` |

## Known Catalog Structure

```
Prod/
  src-staffing-crm/
    salesforce2/
      sfdc/          <- 25 PHYSICAL_DATASETs (canonical SF source)
      heroku/        <- historical opportunity snapshots
      dm3/           <- DM3 environment (26 tables)
      dm2/           <- DM2 environment (25 tables)
  cldsi-prod/
    pipeline/
      raw/           <- 13 VIRTUAL_DATASETs (sf__* views)
      intermediate/  <- 42 VIRTUAL_DATASETs (feat__* feature engineering)
      marts/         <- fomod_feature_store (309 cols), 6 arc__* views
```

## SQL Path Convention

Each path segment must be double-quoted:
```sql
SELECT COUNT(*) FROM "Prod"."src-staffing-crm"."salesforce2"."sfdc"."account"
```

## Pitfalls

- **Credentials load lazily** - if the keychain entry is missing, the first tool call returns `{"error": "... not set. Run: python setup.py credentials configure"}`.
- **SQL is always async** - `dremio_run_sql` polls internally; you don't need to manage job IDs manually.
- **Path segments are slash-separated, not dot-separated** - `"Prod/src-staffing-crm/salesforce2/sfdc/account"`, NOT `"Prod.src-staffing-crm..."`.
- **SQL paths use double-quotes per segment** - not backticks, not single quotes.
- **`_state` dict caches credentials for the process lifetime** - if credentials are rotated, restart Hermes.
- **Results are capped at `max_rows`** - default 100. Pass a higher value for larger result sets.
