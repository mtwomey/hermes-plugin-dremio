---
name: dremio
description: >
  Dremio Cloud catalog navigation and SQL execution via the dremio native plugin.
  This is a redirect stub - load the full skill with skill_view(name="dremio:dremio").
category: data-science
triggers:
  - "dremio"
  - "dremio_ping"
  - "dremio_catalog_list"
  - "dremio_browse"
  - "dremio_get_schema"
  - "dremio_run_sql"
  - "query Dremio"
  - "browse Dremio"
---

# dremio - redirect stub

The full skill lives inside the `dremio` plugin and is registered at runtime.

**Load it with:**

```
skill_view(name="dremio:dremio")
```

## Key Pitfalls (local copy — patch the plugin skill if possible)

- **LIKE with spaces returns 0 rows** — table names use underscores. Use `LIKE '%feature%store%'` not `LIKE '%feature store%'`.
- **INFORMATION_SCHEMA covers `dlcldsi.cldsi-dev` only** — it does NOT enumerate `Prod/cldsi-prod/`. Use `dremio_browse` to traverse production paths.
- **INFORMATION_SCHEMA only covers `dlcldsi`/`cldsi-dev`**, not `Prod/cldsi-prod/`. Use `dremio_browse` for prod paths.
- **Running tools outside Hermes** — use the Hermes venv python (`/Users/mattwo01/.hermes/hermes-agent/venv/bin/python`), `cd` to the plugin repo first, then `sys.path.insert(0, '.')`. Tool handlers take `(args: dict, **kwargs)` — call as `dremio_run_sql({'sql': '...', 'max_rows': 200})`, NOT `dremio_run_sql(sql='...', max_rows=200)`. Do NOT manually add `hermes-plugin-core` to sys.path — it's already in the Hermes venv. See `references/catalog-search-patterns.md` for the full working script.

## Known dlcldsi.cldsi-dev Catalog (dev/staging)

`INFORMATION_SCHEMA` queries surface this source. Key marts tables containing "feature store":

```
dlcldsi.cldsi-dev/
  pipeline/marts/                              <- fomod_feature_store (canonical dev)
  personal_spaces/
    dbtsvc/pipeline/marts/                     <- fomod_feature_store
    dbtsvc/pipeline_training_dm3/marts/        <- fomod_feature_store
    fomod_testing/pipeline_training_dm3/marts/ <- fomod_feature_store,
                                                  arc__feature_store,
                                                  ci__feature_store,
                                                  ci__feature_store_monitoring
    mattwo01/pipeline/marts/                   <- fomod_feature_store
    unknown_user/pipeline/marts/               <- fomod_feature_store
```

See `references/feature-store-tables.md` for the full query result.

## References

- `references/catalog-search-patterns.md` — LIKE search patterns, known feature-store tables, extended catalog structure, ad-hoc script setup.
