from proyecto.agent.loop import run_agent
from proyecto.mcp_server.db.session import create_tables


def prompt(message:str):
    print("Enviando mensaje al agente...")
    response = run_agent(message)
    print("Respuesta del agente:", fix_response(response))
    
def fix_response(response:str):
    if "Ã" in response:
        try:
            return response.encode('latin1').decode('utf-8')
        except UnicodeDecodeError:
            pass
    return response

if __name__ == "__main__":
    create_tables()
    prompt(input("Escribe tu mensaje para el agente: "))
    
