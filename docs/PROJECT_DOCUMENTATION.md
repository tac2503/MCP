# Documentación del proyecto MCP

## Resumen
MCP es un proyecto que integra un agente conversacional con herramientas externas y un servidor de soporte. Esta documentación cubre qué es MCP, la estructura del repositorio, requisitos, cómo ejecutar el proyecto y el flujo operativo.

## ¿Qué es MCP?
MCP (Modelo de Comunicación Programable) es un sistema que permite interactuar con un agente basado en modelos LLM y complementar su comportamiento mediante llamadas a herramientas auxiliares y un servidor local para persistencia y servicios.

## Sobre este repositorio
Este repositorio contiene:

- Un agente y clientes para interactuar con modelos (`proyecto/agent`).
- Un servidor y capa de base de datos para persistencia y servicios (`proyecto/mcp_server`).
- Scripts de arranque y utilidades en la raíz (`main.py`, `requirements.txt`).

## Estructura principal (resumen)

- `main.py` : entrada simple para probar el agente en consola.
- `proyecto/agent/` : lógica del agente
  - `loop.py` : orquestador `run_agent()` que construye prompts y procesa respuestas.
  - `ollama_client.py` : cliente que genera respuestas (conexión al LLM local/externo).
  - `mpc_client.py` : llamadas a herramientas externas/síncronas.
  - `prompt.py` : prompt del sistema y plantillas.
- `proyecto/mcp_server/` : servidor y DB
  - `run_server.py` : ejecuta el servidor (usando `anyio` y stdio-server).
  - `db/` : sesiones, creación de tablas, `seed.py` para datos iniciales.
  - `models/` : modelos ORM (ej. `usuario.py`).
  - `tools/` : utilidades compartidas.

## Archivos más importantes y comportamiento

### `main.py`
Es la entrada principal para probar el agente desde consola. Cuando se ejecuta:

- crea las tablas con `create_tables()`;
- pide un mensaje por teclado;
- envía ese mensaje a `run_agent()`;
- muestra la respuesta final al usuario;
- aplica `fix_response()` si detecta problemas de codificación.

### `proyecto/agent/loop.py`
Es el orquestador del agente. Su comportamiento es:

- construye el prompt uniendo `SYSTEM_PROMPT` con el mensaje del usuario;
- llama a `generate_response()` para consultar el modelo;
- intenta interpretar la respuesta como JSON;
- si la respuesta incluye una tool, la ejecuta con `call_tool_sync()`;
- vuelve a preguntar al modelo con el resultado de la herramienta para producir una respuesta final.

Este archivo define el flujo central de decisión entre responder directamente o usar herramientas.

### `proyecto/agent/ollama_client.py`
Actúa como cliente HTTP hacia Ollama. Su función principal:

- lee variables de entorno como `OLLAMA_URL` y `OLLAMA_MODEL`;
- envía el prompt al endpoint `/api/generate`;
- espera una respuesta no segmentada (`stream = False`);
- valida errores de red o respuestas vacías.

Si Ollama no responde correctamente, aquí se genera el error que bloquea la conversación.

### `proyecto/agent/mpc_client.py`
Es el puente entre el agente y el servidor MCP. Hace lo siguiente:

- levanta el servidor local con `python -m proyecto.mcp_server.run_server`;
- abre una conexión por stdio;
- inicializa la sesión MCP;
- llama a la tool solicitada con sus argumentos;
- devuelve el texto generado por la herramienta al flujo del agente.

### `proyecto/agent/prompt.py`
Contiene el `SYSTEM_PROMPT`, que define cómo debe comportarse el asistente. Este prompt:

- indica cuándo usar tools;
- obliga a responder en JSON cuando se solicita una herramienta;
- enumera las tools disponibles;
- incluye ejemplos para guiar al modelo.

Su contenido controla directamente la calidad del enrutamiento entre lenguaje natural y acciones sobre la base de datos.

### `proyecto/mcp_server/server.py`
Define el servidor MCP y registra las tools disponibles. Su rol es:

- exponer la lista de herramientas mediante `list_tools()`;
- recibir llamadas con `call_tool()`;
- enrutar cada tool a la función correcta de `user_tools.py`;
- devolver resultados como `TextContent` en formato JSON.

Aquí está la capa que traduce la petición MCP a lógica de negocio real.

### `proyecto/mcp_server/tools/user_tools.py`
Implementa la lógica de negocio para usuarios. Sus funciones:

- `get_user_by_email()` busca un usuario por email;
- `create_new_user()` valida datos y evita duplicados;
- `get_all_users()` devuelve el listado completo de usuarios.

Estas funciones usan la sesión de base de datos y las funciones CRUD para operar sobre los datos.

### `proyecto/mcp_server/db/session.py`
Centraliza la conexión con la base de datos. Hace tres cosas clave:

- carga `DATABASE_URL` desde el entorno;
- crea el `engine` de SQLAlchemy;
- expone `SessionLocal` y `create_tables()`.

Este archivo es crítico porque si la URL de la base de datos no existe o es inválida, todo el sistema falla.

### `proyecto/mcp_server/db/crud.py`
Contiene las operaciones básicas sobre la tabla `usuarios`:

- `create_user()` crea y confirma un usuario;
- `get_user_email()` busca un usuario por email;
- `get_users()` recupera la lista completa.

Es la capa más cercana a la base de datos y se usa desde `user_tools.py`.

### `proyecto/mcp_server/models/usuario.py`
Define el modelo ORM `Usuario`. Describe la tabla `usuarios` con:

- `id` como clave primaria autoincremental;
- `nombre` obligatorio;
- `email` obligatorio y único.

Este modelo es la fuente de verdad de la estructura de la tabla.

### `proyecto/mcp_server/db/seed.py`
Se usa para poblar la base de datos con datos iniciales. Su comportamiento:

- carga variables de entorno;
- abre una sesión SQLAlchemy;
- inserta un usuario de ejemplo si no existe;
- maneja errores operacionales de la base de datos.

Es útil para arrancar con datos mínimos y verificar que la persistencia funciona.

### `proyecto/mcp_server/run_server.py`
Es el punto de entrada del servidor MCP. Ejecuta:

- `stdio_server()`;
- `server.run(...)`;
- `anyio.run(main)` para arrancar el evento asíncrono.

Este archivo permite que el servidor se conecte por stdio con el cliente MCP.

### `README.md`
Funciona como puerta de entrada corta del proyecto. Ahora enlaza hacia `docs/PROJECT_DOCUMENTATION.md` para dejar la documentación completa separada del resumen inicial.

## Requisitos

- Python 3.11+ (recomendado). Asegúrate de usar un entorno virtual.
- Instalar dependencias del archivo `requirements.txt`.
- Definir la variable de entorno `DATABASE_URL` (o un `.env` con `DATABASE_URL`) antes de iniciar la app. Ejemplo para SQLite:

```
DATABASE_URL=sqlite:///./mcp.db
```

## Instalación (rápida)

1. Crear y activar un entorno virtual:

```powershell
python -m venv venv
& .\venv\Scripts\Activate.ps1
```

2. Instalar dependencias:

```powershell
pip install -r requirements.txt
```

3. Crear un `.env` con `DATABASE_URL` (ej. SQLite) o configurar la BD.

4. (Opcional) Inicializar datos:

```powershell
python -m proyecto.mcp_server.db.seed
```

## Ejecución

- Ejecutar la interfaz de consola (prompt hacia el agente):

```powershell
python main.py
```

El script `main.py` crea las tablas en la base de datos y abre un prompt para enviar mensajes al agente.

- Ejecutar el servidor MCP (LSP/stdio server):

```powershell
python -m proyecto.mcp_server.run_server
```

Este comando ejecuta el servidor que utiliza `anyio` y el adaptador `mcp.server.stdio`.

## Flujo interno (resumen)

1. El usuario escribe un mensaje en el prompt (`main.py`).
2. `main.py` llama a `run_agent()` en `proyecto/agent/loop.py`.
3. `loop.py` construye el prompt base (`SYSTEM_PROMPT`) y solicita una respuesta al LLM vía `ollama_client.generate_response()`.
4. Si la respuesta es JSON y solicita una `tool`, `loop.py` llama a `mpc_client.call_tool_sync()` para ejecutar la herramienta solicitada.
5. El resultado de la herramienta se integra en un prompt final y se pide al LLM que genere la respuesta al usuario.
6. Para persistencia y datos, el servidor y la DB están en `proyecto/mcp_server/`.

## Configuración y variables importantes

- `DATABASE_URL` : URL de la base de datos usada por SQLAlchemy.
- `.env` : se usa `python-dotenv` para cargar variables locales.

## Consideraciones y solución de problemas

- Encoding de salida: `main.py` incluye `fix_response()` para arreglar problemas de codificación (UTF-8 vs latin1).
- Si hay errores al crear las tablas, revisa `DATABASE_URL` y permisos de acceso a la ruta/servidor.
- Si las instalaciones con `pip` fallan por versiones, comprueba la versión de Python del entorno virtual.

## Desarrollo y pruebas rápidas

- Para probar cambios en el agente, editar `proyecto/agent/loop.py` y usar `python main.py`.
- Para depurar la parte del servidor, lanzar `python -m proyecto.mcp_server.run_server` y conectar un cliente compatible con stdio si corresponde.

## Próximos pasos sugeridos

- Añadir ejemplos de prompts y casos de prueba automatizados.
- Documentar las APIs internas de `mpc_client` y `ollama_client` con ejemplos.

---
Si quieres, puedo adaptar esta documentación en un formato más largo (README en español/inglés), añadir un `docs/TOC.md` o crear un `Makefile`/scripts para automatizar la instalación y arranque. ¿Qué prefieres que haga a continuación?
