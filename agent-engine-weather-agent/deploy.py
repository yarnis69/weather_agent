import vertexai

client = vertexai.Client(  
    project="weather-agent-504614",
    location="europe-west2",
)


remote_app = client.agent_engines.create( 
    config={
        "source_packages": ["weather_agent"],            
        "entrypoint_module": "weather_agent.agent",      
        "entrypoint_object": "app",     
        "display_name": "Weather_Agent",    
        "identity_type": "AGENT_IDENTITY",
        "requirements_file": "weather_agent/requirements.txt",
        "agent_framework": "google-adk",
        "class_methods": [

    # --- session management (sync) ---
    {
        "name": "create_session",
        "api_mode": "",
        "parameters": {
            "type": "object",
            "properties": {
                "user_id": {"type": "string", "description": "Caller identifier"},
                "session_id": {"type": "string", "description": "Optional; generated if omitted"},
                "state": {"type": "object", "description": "Optional initial session state"},
            },
            "required": ["user_id"],
        },
    },
    {
        "name": "get_session",
        "api_mode": "",
        "parameters": {
            "type": "object",
            "properties": {
                "user_id": {"type": "string"},
                "session_id": {"type": "string"},
            },
            "required": ["user_id", "session_id"],
        },
    },
    {
        "name": "list_sessions",
        "api_mode": "",
        "parameters": {
            "type": "object",
            "properties": {"user_id": {"type": "string"}},
            "required": ["user_id"],
        },
    },
    {
        "name": "delete_session",
        "api_mode": "",
        "parameters": {
            "type": "object",
            "properties": {
                "user_id": {"type": "string"},
                "session_id": {"type": "string"},
            },
            "required": ["user_id", "session_id"],
        },
    },

    # --- session management (async) ---
    {
        "name": "async_create_session",
        "api_mode": "async",
        "parameters": {
            "type": "object",
            "properties": {
                "user_id": {"type": "string"},
                "session_id": {"type": "string"},
                "state": {"type": "object"},
            },
            "required": ["user_id"],
        },
    },
    {
        "name": "async_get_session",
        "api_mode": "async",
        "parameters": {
            "type": "object",
            "properties": {
                "user_id": {"type": "string"},
                "session_id": {"type": "string"},
            },
            "required": ["user_id", "session_id"],
        },
    },
    {
        "name": "async_list_sessions",
        "api_mode": "async",
        "parameters": {
            "type": "object",
            "properties": {"user_id": {"type": "string"}},
            "required": ["user_id"],
        },
    },
    {
        "name": "async_delete_session",
        "api_mode": "async",
        "parameters": {
            "type": "object",
            "properties": {
                "user_id": {"type": "string"},
                "session_id": {"type": "string"},
            },
            "required": ["user_id", "session_id"],
        },
    },

    # --- querying ---
    {
        "name": "stream_query",
        "api_mode": "stream",
        "parameters": {
            "type": "object",
            "properties": {
                "message": {
                    "anyOf": [{"type": "string"}, {"type": "object"}],
                    "description": "The user's weather question",
                },
                "user_id": {"type": "string"},
                "session_id": {"type": "string", "description": "Optional; new session if omitted"},
                "run_config": {"type": "object"},
            },
            "required": ["message", "user_id"],
        },
    },
    {
        "name": "async_stream_query",
        "api_mode": "async_stream",
        "parameters": {
            "type": "object",
            "properties": {
                "message": {
                    "anyOf": [{"type": "string"}, {"type": "object"}],
                    "description": "The user's weather question",
                },
                "user_id": {"type": "string"},
                "session_id": {"type": "string"},
                "session_events": {"type": "array", "items": {"type": "object"}},
                "run_config": {"type": "object"},
            },
            "required": ["message", "user_id"],
        },
    },
]
      },
)