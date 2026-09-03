"""Main entrypoint for Basecamp Connector."""
from __future__ import annotations
from app import ext
import handlers_connection as hc
import handlers_resources as hr
import panels
import panels_settings

# Register tools
ext.register_tool(
    name="connect_basecamp",
    handler=hc.connect_basecamp,
    description="Connect a Basecamp workspace by saving an API key."
)
ext.register_tool(
    name="list_connections",
    handler=hc.list_connections,
    description="List connected Basecamp workspaces."
)
ext.register_tool(
    name="disconnect_basecamp",
    handler=hc.disconnect_basecamp,
    description="Disconnect a Basecamp workspace."
)
ext.register_tool(
    name="get_overview",
    handler=hr.get_overview,
    description="Read Basecamp account overview and status."
)
ext.register_tool(
    name="audit_health",
    handler=hr.audit_health,
    description="Build health audit report for Basecamp connection."
)
ext.register_tool(
    name="list_resources",
    handler=hr.list_resources,
    description="List resources in Basecamp."
)
ext.register_tool(
    name="get_resource",
    handler=hr.get_resource,
    description="Get details of a Basecamp resource."
)

if __name__ == "__main__":
    ext.run()
