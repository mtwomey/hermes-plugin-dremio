from pathlib import Path
from hermes_plugin_core.setup_cli import SetupCLI, PluginConfig

config = PluginConfig(
    plugin_key="dremio",
    service="hermes-dremio-cloud",
    repo_dir=Path(__file__).parent.resolve(),
    keys=["pat", "project_id"],
    cred_prompts={
        "pat":        ("Dremio Cloud Personal Access Token", "", True),
        "project_id": ("Dremio Cloud Project ID (UUID)", "", False),
    },
    requirements=["requests"],
    has_skill_stub=True,
    skill_stub_category="data-science",
)

if __name__ == "__main__":
    SetupCLI(config).run()
