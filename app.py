"""Imperal extension app definition for Basecamp."""
from __future__ import annotations
from imperal_sdk import App

ext = App(
    name="Basecamp",
    app_id="basecamp-connector",
    version="0.1.0",
    description="Connect and operate Basecamp from Imperal Cloud."
)
chat = ext.chat
