import sys
import json
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from hermes_plugin_core.testing import TestSuite, expect_ok


def register_tests(suite):
    suite.add("ping", test_ping)
    suite.add("catalog_list", test_catalog_list)
    suite.add("browse_root_path", test_browse)
    suite.add("get_schema", test_get_schema)
    suite.add("run_sql", test_run_sql)


def test_ping():
    from tools import dremio_ping
    expect_ok(dremio_ping({}))


def test_catalog_list():
    from tools import dremio_catalog_list
    raw = dremio_catalog_list({})
    data = json.loads(raw)
    assert isinstance(data, list), f"Expected list, got: {raw}"
    assert len(data) > 0, "Expected at least one catalog entry"


def test_browse():
    from tools import dremio_browse
    raw = dremio_browse({"path": "Prod/src-staffing-crm/salesforce2/sfdc"})
    data = json.loads(raw)
    assert "error" not in data, f"Browse failed: {raw}"
    assert "children" in data or "fields" in data, f"Unexpected shape: {raw}"


def test_get_schema():
    from tools import dremio_get_schema
    raw = dremio_get_schema({"path": "Prod/src-staffing-crm/salesforce2/sfdc/account"})
    data = json.loads(raw)
    assert isinstance(data, list), f"Expected list of fields, got: {raw}"
    assert len(data) > 0, "Expected at least one field"
    assert "name" in data[0] and "type" in data[0], f"Unexpected field shape: {data[0]}"


def test_run_sql():
    from tools import dremio_run_sql
    raw = dremio_run_sql({
        "sql": 'SELECT COUNT(*) AS cnt FROM "Prod"."src-staffing-crm"."salesforce2"."sfdc"."account"',
        "max_rows": 1
    })
    data = json.loads(raw)
    assert "error" not in data, f"SQL failed: {raw}"
    assert "rows" in data, f"No rows key: {raw}"
