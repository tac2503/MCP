import asyncio
import sys
from mcp import ClientSession
from mcp.client.stdio import stdio_client, StdioServerParameters


async def call_tool(tool_name: str, arguments: dict) -> str:
    """
    Llama una tool del MCP server usando stdio.
    """

    server_params = StdioServerParameters(
        command=sys.executable,
        args=["-m", "proyecto.mcp_server.run_server"],
    )
    
    async with stdio_client(server_params) as (read,write):
        
        async with ClientSession(read,write) as session:
            await session.initialize()
            
            result= await session.call_tool(tool_name, arguments)
            
            if result.content and len(result.content) > 0:
                return result.content[0].text 
            
            return "Error: No se recibió respuesta de la herramienta."  


def call_tool_sync(tool_name: str, arguments: dict) -> str:
    """
    Wrapper síncrono para usar en código normal (sin async).
    """
    return asyncio.run(call_tool(tool_name, arguments))