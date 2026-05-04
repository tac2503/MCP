from mcp.server import Server
from mcp.types import TextContent, Tool
from .tools import user_tools
import json

server = Server("mi-primer-mcp")


@server.list_tools()
async def handle_list_tools():
    return [
        Tool(
            name="get_user_by_email",
            description="Obtiene un usuario por su email.",
            inputSchema={
                "type": "object",
                "properties": {
                    "email": {"type": "string"},
                },
                "required": ["email"],
                "additionalProperties": False,
            },
        ),
        Tool(
            name="create_new_user",
            description="Crea un usuario nuevo.",
            inputSchema={
                "type": "object",
                "properties": {
                    "nombre": {"type": "string"},
                    "name": {"type": "string"},
                    "email": {"type": "string"},
                },
                "required": ["email"],
                "additionalProperties": False,
            },
        ),
        Tool(
            name="get_all_users",
            description="Lista todos los usuarios.",
            inputSchema={
                "type": "object",
                "properties": {},
                "additionalProperties": False,
            },
        ),
    ]


@server.call_tool()
async def handle_tool_call(name: str, arguments: dict):
    if name == "get_user_by_email":
        result = user_tools.get_user_by_email(arguments.get("email"))
        return [TextContent(type="text", text=json.dumps(result))]
    elif name == "create_new_user":
        nombre = arguments.get("nombre") or arguments.get("name")
        result = user_tools.create_new_user(nombre, arguments.get("email"))
        return [TextContent(type="text", text=json.dumps(result))]
    elif name == "get_all_users":
        result = user_tools.get_all_users()
        return [TextContent(type="text", text=json.dumps(result))]
    else:
        return [TextContent(type="text", text=json.dumps({"error": "Tool not found"}))]

