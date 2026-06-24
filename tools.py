"""
tools.py - Dremio Cloud tool handlers for hermes-plugin-dremio.

Credentials are loaded lazily on first tool call via hermes_plugin_core.keychain.
"""

import json
import time
import urllib.parse

import requests
from hermes_plugin_core.keychain import cred_get

# ---------------------------------------------------------------------------
# Lazy credential state
# ---------------------------------------------------------------------------
_state: dict = {}


def _get_http_state() -> dict:
    """Return (and lazily initialise) BASE + HEADERS from Keychain."""
    if "base" not in _state:
        pat = cred_get("hermes-dremio-cloud", "pat")
        project_id = cred_get("hermes-dremio-cloud", "project_id")
        if not pat:
            raise RuntimeError("Dremio PAT not set. Run: python setup.py credentials configure")
        if not project_id:
            raise RuntimeError("Dremio project_id not set. Run: python setup.py credentials configure")
        _state["base"] = f"https://api.dremio.cloud/v0/projects/{project_id}"
        _state["headers"] = {
            "Authorization": f"Bearer {pat}",
            "Content-Type": "application/json",
        }
    return _state


def _encode_path(slash_path: str) -> str:
    """URL-encode each segment of a slash-separated path and join with '/'."""
    segments = slash_path.strip("/").split("/")
    return "/".join(urllib.parse.quote(seg, safe="") for seg in segments)


# ---------------------------------------------------------------------------
# Tool handlers
# ---------------------------------------------------------------------------

def dremio_ping(args: dict, **kwargs) -> str:
    try:
        s = _get_http_state()
        resp = requests.get(f"{s['base']}/catalog", headers=s["headers"], timeout=15)
        if resp.status_code == 200:
            data = resp.json().get("data", [])
            return json.dumps({
                "ok": True,
                "project_id": s["base"].rsplit("/", 1)[-1],
                "catalog_count": len(data),
            })
        return json.dumps({
            "ok": False,
            "status_code": resp.status_code,
            "error": resp.text,
        })
    except Exception as e:
        return json.dumps({"ok": False, "error": str(e)})


def dremio_catalog_list(args: dict, **kwargs) -> str:
    try:
        s = _get_http_state()
        resp = requests.get(f"{s['base']}/catalog", headers=s["headers"], timeout=15)
        resp.raise_for_status()
        entries = resp.json().get("data", [])
        result = [
            {
                "path": entry.get("path", []),
                "type": entry.get("type", ""),
                "containerType": entry.get("containerType", ""),
            }
            for entry in entries
        ]
        return json.dumps(result)
    except Exception as e:
        return json.dumps({"error": str(e)})


def dremio_browse(args: dict, **kwargs) -> str:
    try:
        path = args.get("path", "")
        s = _get_http_state()
        encoded = _encode_path(path)
        resp = requests.get(f"{s['base']}/catalog/by-path/{encoded}", headers=s["headers"], timeout=15)
        resp.raise_for_status()
        obj = resp.json()

        entity_type = obj.get("entityType", obj.get("type", ""))

        if entity_type in ("SOURCE", "SPACE", "FOLDER", "HOME", "CONTAINER"):
            children = obj.get("children", [])
            return json.dumps({
                "type": "CONTAINER",
                "containerType": entity_type,
                "children": [
                    {
                        "path": c.get("path", []),
                        "type": c.get("type", ""),
                        "containerType": c.get("containerType", ""),
                        "datasetType": c.get("datasetType", ""),
                    }
                    for c in children
                ],
            })

        if entity_type in ("PHYSICAL_DATASET", "VIRTUAL_DATASET", "DATASET"):
            fields = [
                {"name": f["name"], "type": f["type"]["name"]}
                for f in obj.get("fields", [])
            ]
            result: dict = {"type": entity_type, "fields": fields}
            if entity_type == "VIRTUAL_DATASET" and "sql" in obj:
                result["sql"] = obj["sql"]
            return json.dumps(result)

        return json.dumps({"type": entity_type, "raw": obj})

    except requests.HTTPError as e:
        return json.dumps({"error": f"HTTP {e.response.status_code}: {e.response.text}"})
    except Exception as e:
        return json.dumps({"error": str(e)})


def dremio_get_schema(args: dict, **kwargs) -> str:
    try:
        path = args.get("path", "")
        s = _get_http_state()
        encoded = _encode_path(path)
        resp = requests.get(f"{s['base']}/catalog/by-path/{encoded}", headers=s["headers"], timeout=15)
        resp.raise_for_status()
        obj = resp.json()

        fields = obj.get("fields", [])
        if not fields:
            return json.dumps({"error": "No fields found - path may not be a dataset", "path": path})

        schema = [{"name": f["name"], "type": f["type"]["name"]} for f in fields]
        return json.dumps(schema)

    except requests.HTTPError as e:
        return json.dumps({"error": f"HTTP {e.response.status_code}: {e.response.text}"})
    except Exception as e:
        return json.dumps({"error": str(e)})


def dremio_run_sql(args: dict, **kwargs) -> str:
    try:
        sql = args.get("sql", "")
        max_rows = int(args.get("max_rows", 100))
        s = _get_http_state()

        submit_resp = requests.post(
            f"{s['base']}/sql",
            headers=s["headers"],
            json={"sql": sql},
            timeout=30,
        )
        submit_resp.raise_for_status()
        job_id = submit_resp.json().get("id")
        if not job_id:
            return json.dumps({"error": "No job ID returned from SQL submission"})

        MAX_POLLS = 40
        SLEEP_SEC = 3
        for _ in range(MAX_POLLS):
            time.sleep(SLEEP_SEC)
            status_resp = requests.get(
                f"{s['base']}/job/{job_id}",
                headers=s["headers"],
                timeout=15,
            )
            status_resp.raise_for_status()
            status_data = status_resp.json()
            job_state = status_data.get("jobState", "")

            if job_state == "COMPLETED":
                break
            elif job_state == "FAILED":
                return json.dumps({"error": status_data.get("errorMessage", "Job failed")})
            elif job_state in ("CANCELED", "CANCELLATION_REQUESTED"):
                return json.dumps({"error": f"Job was cancelled (state: {job_state})"})
        else:
            return json.dumps({"error": f"Timed out polling job {job_id} after {MAX_POLLS * SLEEP_SEC}s"})

        results_resp = requests.get(
            f"{s['base']}/job/{job_id}/results",
            headers=s["headers"],
            timeout=30,
        )
        results_resp.raise_for_status()
        results_data = results_resp.json()

        schema = results_data.get("schema", [])
        columns = [col.get("name", "") for col in schema]
        rows = results_data.get("rows", [])[:max_rows]

        return json.dumps({"columns": columns, "rows": rows, "row_count": len(rows)})

    except requests.HTTPError as e:
        return json.dumps({"error": f"HTTP {e.response.status_code}: {e.response.text}"})
    except Exception as e:
        return json.dumps({"error": str(e)})
