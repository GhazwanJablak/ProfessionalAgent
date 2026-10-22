user_details_schema = {
    "name": "record_user_details",
    "description": "Use this tool to register user interest in getting in touch",
    "parameters": {
        "type": "object",
        "properties": {
            "email": {
                "type": "string",
                "description": "User email address"
            },
            "name": {
                "type": "string",
                "description": "User's name"
            },
            "notes": {
                "type": "string",
                "description": "Any additional information about the user and the conversation"
            }
        },
        "required": ["name"],
        "additionalProperties": False
    }
}

unknown_question_schema= {
    "name": "record_unknown_question",
    "description": "recording user's question that LLM couldn't answer",
    "parameters": {
        "type": "object",
        "properties": {
            "question": {
                "type": "string",
                "description": "user's question"
            }
        },
        "required": ["question"],
        "additionalProperties": False
    }
}