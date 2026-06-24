#!/usr/bin/env python3
"""Setup script for hermes-plugin-dremio.

Usage:
    python setup.py install       # install plugin into Hermes
    python setup.py uninstall     # remove plugin from Hermes
    python setup.py status        # show installation status
    python setup.py credentials   # manage credentials
    python setup.py log           # manage log level
    python setup.py audit         # check compliance
    python setup.py test          # run smoke tests
"""
from pathlib import Path
from hermes_plugin_core.setup_cli import SetupCLI, PluginConfig

config = PluginConfig(
    plugin_key="dremio",
    service="hermes-dremio",
    repo_dir=Path(__file__).parent.resolve(),
    keys=["api_key"],
    cred_prompts={
        "api_key": ("API Key", "", True),
    },
    requirements=[],
    has_skill_stub=True,
    skill_stub_category="data-science",
)

if __name__ == "__main__":
    SetupCLI(config).run()
