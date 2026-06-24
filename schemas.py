"""Tool schemas for hermes-plugin-dremio."""

TOOLS = [
    {
        "name": "dremio_ping",
        "description": "Test connectivity and authentication for dremio.",
        "input_schema": {
            "type": "object",
            "properties": {},
            "required": [],
        },
    },
]
