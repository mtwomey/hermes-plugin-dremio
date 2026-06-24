"""Tool implementations for hermes-plugin-dremio."""
import json
import logging

from hermes_plugin_core.keychain import cred_get

logger = logging.getLogger("dremio")

SERVICE = "hermes-dremio"


def dremio_ping(args: dict) -> str:
    """Test connectivity and authentication."""
    try:
        # TODO: implement real ping
        api_key = cred_get(SERVICE, "api_key")
        if not api_key:
            return json.dumps({"error": "not configured — run: python setup.py credentials configure"})
        return json.dumps({"status": "ok"})
    except Exception as e:
        logger.exception("ping failed")
        return json.dumps({"error": str(e)})
