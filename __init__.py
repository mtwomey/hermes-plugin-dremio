from pathlib import Path

from hermes_plugin_core import setup_logging
from hermes_plugin_core.config import get_log_level
from . import schemas, tools

_SKILL_MD = Path(__file__).parent / "SKILL.md"


def register(ctx) -> None:
    setup_logging("dremio", get_log_level("dremio"))

    _REGISTRY = [
        (schemas.DREMIO_PING,         tools.dremio_ping),
        (schemas.DREMIO_CATALOG_LIST, tools.dremio_catalog_list),
        (schemas.DREMIO_BROWSE,       tools.dremio_browse),
        (schemas.DREMIO_GET_SCHEMA,   tools.dremio_get_schema),
        (schemas.DREMIO_RUN_SQL,      tools.dremio_run_sql),
    ]

    for schema, handler in _REGISTRY:
        ctx.register_tool(
            name=schema["name"],
            toolset="dremio",
            schema=schema,
            handler=handler,
        )

    if _SKILL_MD.exists():
        ctx.register_skill("dremio", _SKILL_MD)
