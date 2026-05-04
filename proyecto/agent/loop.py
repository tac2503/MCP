import json
#import sys
from .ollama_client import generate_response
from .prompt import SYSTEM_PROMPT
from proyecto.agent.mpc_client import call_tool_sync

def run_agent(user_input:str):
    
    prompt=SYSTEM_PROMPT + "\nUsuario: " + user_input 
    
    response=generate_response(prompt)
    
    try:
        data = json.loads(response)
        #print(response,file=sys.stderr)
        
        if "tool" in data:
            tool_name = data["tool"]
            arguments = data.get("arguments", {})
            
            tool_result = call_tool_sync(tool_name, arguments)
            
            final_prompt= f"""
                Resultado de la herramienta: 
                {tool_result}
                
                Responde al usuario de forma clara y natural.
                
            """
            
            return generate_response(final_prompt)
    except json.JSONDecodeError:
        return response
    return response

