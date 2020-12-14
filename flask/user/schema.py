USER_CREATE = {
    "type": "object",
    "properties": {
        "email": {
            "type": "string",
            "pattern": r"^[\w-]+@[a-z]+.[a-z]+$"
        },
        "password": {
            "type": "string",
            "pattern": r"[\w!@#$%^&*()=+\[\]\{\}]+"
        },
        "username": {
            "type": "string"
        },
    },
    "required": ["email", "password"]
}
