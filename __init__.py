"""Hermes plugin: dremio"""
from hermes_plugin_core import setup_logging
from hermes_plugin_core.config import get_log_level
from hermes_plugin_core.keychain import cred_get


def register(ctx):
    log_level = get_log_level("dremio")
    setup_logging("dremio", log_level)
    ctx.register_tools([
        "dremio_ping",
    ])
