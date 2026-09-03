"""Panel UI for Basecamp Connector."""
from __future__ import annotations
from imperal_sdk import ui
from app import ext

def _settings_button() -> ui.UINode:
    return ui.Button(
        "App settings",
        variant="secondary",
        size="sm",
        icon="settings",
        on_click=ui.Call("__panel__basecamp_settings")
    )

def _help_modal() -> ui.UINode:
    return ui.Modal(
        trigger=ui.Button("How do I set this up?", variant="ghost", size="sm"),
        title="Connecting Basecamp",
        children=[
            ui.Text(
                "1. Sign in to your Basecamp dashboard and navigate to API & Integrations Settings.\n"
                "2. Generate an API Key or Bearer Token with suitable permissions.\n"
                "3. Paste the API Key and optional Base URL into the form on the left.\n"
                "4. Click Connect Basecamp to verify and save your credentials.",
                variant="body"
            )
        ]
    )

@ext.panel(slot="sidebar")
async def main_panel(ctx) -> ui.UINode:
    form = ui.Form(
        id="connect_basecamp_form",
        submit_label="Connect Basecamp",
        action=ui.Call("connect_basecamp"),
        children=[
            ui.Input(
                name="label",
                label="Connection Label",
                placeholder="e.g. Production Account"
            ),
            ui.Input(
                name="api_key",
                label="API Key / Token",
                placeholder="Enter Basecamp API Key or Bearer Token"
            ),
            ui.Input(
                name="base_url",
                label="Base URL (optional)",
                placeholder="https://basecamp.com"
            )
        ]
    )

    return ui.Stack(
        children=[
            ui.Heading("Basecamp Connector", level=3),
            ui.Text("Connect and manage your Basecamp workspace.", variant="caption"),
            ui.Divider(),
            form,
            ui.Divider(),
            _help_modal(),
            ui.Divider(),
            _settings_button()
        ]
    )
