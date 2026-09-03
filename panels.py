"""Panel UI for Basecamp Connector."""
from __future__ import annotations
from imperal_sdk import ui
from app import ext
import handlers_connection as h

def _settings_button() -> ui.UINode:
    return ui.Button(
        "App settings",
        variant="secondary",
        size="sm",
        icon="settings",
        on_click=ui.Call("__basecamp_settings")
    )

def _help_modal() -> ui.UINode:
    return ui.Modal(
        trigger=ui.Button("How do I set this up?", variant="ghost", size="sm"),
        title="Connecting Basecamp",
        children=[
            ui.Text(
                "1. Sign in to your Basecamp account and get your OAuth token and account ID.\n"
                "2. Enter your account details below.\n"
                "3. Click Connect Basecamp to verify and save your connection securely.",
                variant="body"
            )
        ]
    )

@ext.panel("basecamp_sidebar", slot="left")
async def basecamp_sidebar(ctx, **kwargs) -> ui.UINode:
    connections = await h._load_connections(ctx)
    conn_items = [
        ui.Text(c.get("label") or "Basecamp Account", variant="body")
        for c in connections
    ] if connections else [ui.Text("No Basecamp accounts connected yet.", variant="caption")]

    return ui.Stack(
        direction="v",
        gap=3,
        children=[
            ui.Text("Basecamp", variant="heading"),
            ui.Stack(direction="v", gap=1, children=conn_items),
            ui.Divider(),
            ui.Form(
                submit_label="Connect Basecamp",
                action=ui.Call("connect_basecamp"),
                children=[
                    ui.Stack(
                        direction="v",
                        gap=2,
                        children=[
                            ui.Stack(
                                direction="v",
                                gap=1,
                                children=[
                                    ui.Text("Connection Label", variant="label"),
                                    ui.Input(
                                        param_name="label",
                                        placeholder="e.g. Production Basecamp"
                                    ),
                                ]
                            ),
                            ui.Stack(
                                direction="v",
                                gap=1,
                                children=[
                                    ui.Text("Account ID", variant="label"),
                                    ui.Input(
                                        param_name="account_id",
                                        placeholder="e.g. 1234567"
                                    ),
                                ]
                            ),
                            ui.Stack(
                                direction="v",
                                gap=1,
                                children=[
                                    ui.Text("OAuth Access Token", variant="label"),
                                    ui.Input(
                                        param_name="access_token",
                                        placeholder="Enter OAuth access token"
                                    ),
                                ]
                            ),
                        ]
                    )
                ]
            ),
            _help_modal(),
            ui.Spacer(),
            _settings_button(),
        ]
    )
