# Dremio Catalog Search Patterns & Pitfalls

## Searching by Table Name in INFORMATION_SCHEMA

### ⚠️ LIKE with spaces returns 0 rows
`LIKE '%feature store%'` (literal space) misses all matches — Dremio table names
use underscores, so the space never appears. Use wildcards around both words:

```sql
-- WRONG: returns 0 rows
SELECT TABLE_CATALOG, TABLE_SCHEMA, TABLE_NAME
FROM INFORMATION_SCHEMA."TABLES"
WHERE LOWER(TABLE_NAME) LIKE '%feature store%';

-- CORRECT: returns all matches
SELECT TABLE_CATALOG, TABLE_SCHEMA, TABLE_NAME
FROM INFORMATION_SCHEMA."TABLES"
WHERE LOWER(TABLE_NAME) LIKE '%feature%store%';
```

### INFORMATION_SCHEMA coverage gap
INFORMATION_SCHEMA only covers `dlcldsi`/`cldsi-dev` paths. It does **not** surface
production datasets under `Prod/cldsi-prod/`. For prod tables, browse directly:

```python
dremio_browse({"path": "Prod/cldsi-prod/pipeline/marts"})
```

---

## Known Feature-Store Tables (as of 2026-06)

All in catalog `DREMIO`:

| TABLE_NAME | SCHEMA |
|-----------|--------|
| `fomod_feature_store` | `dlcldsi.cldsi-dev.pipeline.marts` |
| `fomod_feature_store` | `dlcldsi.cldsi-dev.personal_spaces.dbtsvc.pipeline.marts` |
| `fomod_feature_store` | `dlcldsi.cldsi-dev.personal_spaces.dbtsvc.pipeline_training_dm3.marts` |
| `fomod_feature_store` | `dlcldsi.cldsi-dev.personal_spaces.fomod_testing.pipeline_training_dm3.marts` |
| `arc__feature_store` | `dlcldsi.cldsi-dev.personal_spaces.fomod_testing.pipeline_training_dm3.marts` |
| `ci__feature_store` | `dlcldsi.cldsi-dev.personal_spaces.fomod_testing.pipeline_training_dm3.marts` |
| `ci__feature_store_monitoring` | `dlcldsi.cldsi-dev.personal_spaces.fomod_testing.pipeline_training_dm3.marts` |
| `fomod_feature_store` | `dlcldsi.cldsi-dev.personal_spaces.mattwo01.pipeline.marts` |
| `fomod_feature_store` | `dlcldsi.cldsi-dev.personal_spaces.unknown_user.pipeline.marts` |

Production path (via `dremio_browse`):
- `["Prod", "cldsi-prod", "pipeline", "marts", "fomod_feature_store"]` — VIRTUAL_DATASET

---

## Running Plugin Tools Outside Hermes (Ad-hoc Scripts)

Use the **Hermes venv python** — it already has `hermes_plugin_core` and all deps installed:

```bash
cd /Users/mattwo01/Git_Repos/hermes-plugin-dremio
/Users/mattwo01/.hermes/hermes-agent/venv/bin/python -c "
import sys
sys.path.insert(0, '.')
import json
from tools import dremio_run_sql, dremio_browse, dremio_catalog_list, dremio_get_schema

# All tool functions take a SINGLE POSITIONAL DICT — NOT keyword args
result = dremio_run_sql({'sql': 'SELECT ...', 'max_rows': 200})
print(result)
"
```

**Critical pitfalls:**
- Call as `dremio_run_sql({'sql': '...', 'max_rows': 200})` — **not** `dremio_run_sql(sql='...', max_rows=200)`. The handler signature is `(args: dict, **kwargs)`.
- Only add the plugin repo to `sys.path` (`/Users/mattwo01/Git_Repos/hermes-plugin-dremio`). Do NOT manually add `hermes-plugin-core` — the Hermes venv already has it installed.
- Using the system or conda python will fail with `ModuleNotFoundError: No module named 'hermes_plugin_core'`.

---

## Extended Catalog Structure

```
Prod/
  cldsi-prod/
    pipeline/
      marts/         <- fomod_feature_store (VIRTUAL), arc__* views, util__last_run

dlcldsi/ (cldsi-dev via INFORMATION_SCHEMA)
  pipeline/
    marts/           <- fomod_feature_store
  personal_spaces/
    dbtsvc/
      pipeline/marts/                    <- fomod_feature_store
      pipeline_training_dm3/marts/       <- fomod_feature_store
    fomod_testing/
      pipeline_training_dm3/marts/       <- fomod_feature_store, arc__feature_store,
                                            ci__feature_store, ci__feature_store_monitoring
    mattwo01/
      pipeline/marts/                    <- fomod_feature_store
    unknown_user/
      pipeline/marts/                    <- fomod_feature_store
```
