DREMIO_PING = {
    "name": "dremio_ping",
    "description": "Test Dremio Cloud connectivity and authentication. Returns project info.",
    "parameters": {
        "type": "object",
        "properties": {},
        "required": [],
    },
}

DREMIO_CATALOG_LIST = {
    "name": "dremio_catalog_list",
    "description": "List top-level Dremio catalog entries (sources, spaces, folders).",
    "parameters": {
        "type": "object",
        "properties": {},
        "required": [],
    },
}

DREMIO_BROWSE = {
    "name": "dremio_browse",
    "description": (
        "Browse a Dremio catalog path.\n\n"
        "For containers, lists children. For datasets, returns fields and type."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "path": {
                "type": "string",
                "description": (
                    'Slash-separated catalog path, e.g. "Prod/src-staffing-crm/salesforce2/sfdc"'
                ),
            },
        },
        "required": ["path"],
    },
}

DREMIO_GET_SCHEMA = {
    "name": "dremio_get_schema",
    "description": "Get the column schema for a Dremio table or view.",
    "parameters": {
        "type": "object",
        "properties": {
            "path": {
                "type": "string",
                "description": (
                    'Slash-separated catalog path, e.g. "Prod/src-staffing-crm/salesforce2/sfdc/account"'
                ),
            },
        },
        "required": ["path"],
    },
}

DREMIO_RUN_SQL = {
    "name": "dremio_run_sql",
    "description": (
        "Execute a SQL query on Dremio Cloud. Returns results as JSON.\n\n"
        "Uses async job polling: submits the query, waits for completion, then fetches results."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "sql": {
                "type": "string",
                "description": "SQL query to execute.",
            },
            "max_rows": {
                "type": "integer",
                "description": "Maximum number of rows to return (default 100).",
            },
        },
        "required": ["sql"],
    },
}
