from proyecto.agent.loop import run_agent
from proyecto.mcp_server.db.session import create_tables

def prompt(message:str):
    print("Enviando mensaje al agente...")
    response = run_agent(message)
    print("Respuesta del agente:", response)

if __name__ == "__main__":
    create_tables()
    prompt(input("Escribe tu mensaje para el agente: "))
    
