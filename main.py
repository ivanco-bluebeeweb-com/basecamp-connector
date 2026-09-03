"""Basecamp Connector execution entrypoint."""
from app import app
import handlers_connection as hc
import handlers_resources as hr

# Register connection tools
app.register_tool("connect_basecamp", hc.connect_basecamp)
app.register_tool("list_connections", hc.list_connections)
app.register_tool("disconnect_basecamp", hc.disconnect_basecamp)

# Register project tools
app.register_tool("list_projects", hr.list_projects)
app.register_tool("get_project", hr.get_project)
app.register_tool("create_project", hr.create_project)

# Register to-do tools
app.register_tool("list_todos", hr.list_todos)
app.register_tool("create_todo", hr.create_todo)
app.register_tool("complete_todo", hr.complete_todo)
app.register_tool("uncomplete_todo", hr.uncomplete_todo)

# Register message tools
app.register_tool("list_messages", hr.list_messages)
app.register_tool("post_message", hr.post_message)

# Register webhook tools
app.register_tool("list_webhooks", hr.list_webhooks)
app.register_tool("create_webhook", hr.create_webhook)

# Value-add audit
app.register_tool("audit_basecamp_health", hr.audit_basecamp_health)

if __name__ == "__main__":
    app.run()
