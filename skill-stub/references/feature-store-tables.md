# Feature Store Tables in Dremio

Query used (2026-06-25):
```sql
SELECT TABLE_CATALOG, TABLE_SCHEMA, TABLE_NAME, TABLE_TYPE
FROM INFORMATION_SCHEMA."TABLES"
WHERE LOWER(TABLE_NAME) LIKE '%feature%store%'
ORDER BY TABLE_SCHEMA, TABLE_NAME
```

## Results (9 rows)

| TABLE_SCHEMA | TABLE_NAME | TABLE_TYPE |
|---|---|---|
| `dlcldsi.cldsi-dev.personal_spaces.dbtsvc.pipeline.marts` | `fomod_feature_store` | TABLE |
| `dlcldsi.cldsi-dev.personal_spaces.dbtsvc.pipeline_training_dm3.marts` | `fomod_feature_store` | TABLE |
| `dlcldsi.cldsi-dev.personal_spaces.fomod_testing.pipeline_training_dm3.marts` | `arc__feature_store` | TABLE |
| `dlcldsi.cldsi-dev.personal_spaces.fomod_testing.pipeline_training_dm3.marts` | `ci__feature_store` | TABLE |
| `dlcldsi.cldsi-dev.personal_spaces.fomod_testing.pipeline_training_dm3.marts` | `ci__feature_store_monitoring` | TABLE |
| `dlcldsi.cldsi-dev.personal_spaces.fomod_testing.pipeline_training_dm3.marts` | `fomod_feature_store` | TABLE |
| `dlcldsi.cldsi-dev.personal_spaces.mattwo01.pipeline.marts` | `fomod_feature_store` | TABLE |
| `dlcldsi.cldsi-dev.personal_spaces.unknown_user.pipeline.marts` | `fomod_feature_store` | TABLE |
| `dlcldsi.cldsi-dev.pipeline.marts` | `fomod_feature_store` | TABLE |

## Notes
- All are TABLE_CATALOG = `DREMIO`.
- `dlcldsi.cldsi-dev.pipeline.marts.fomod_feature_store` is the canonical dev table.
- The `fomod_testing` personal space contains variant tables (`arc__`, `ci__`) not found elsewhere.
- INFORMATION_SCHEMA does NOT surface the Prod (`cldsi-prod`) source — use `dremio_browse` for that.
