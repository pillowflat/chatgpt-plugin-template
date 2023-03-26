TITLE = "ChatGPT Plugin Template"
VERSION = "1.0.0"
DESCRIPTION = "Plugin template with a simple query example"


def get_plugin_config():
    return {
        "schema_version": "v1",
        "name_for_human": TITLE,
        "name_for_model": TITLE,
        "description_for_human": DESCRIPTION,
        "description_for_model": DESCRIPTION,
        "auth": {
            "type": "none"
        },
        "api": {
            "type": "openapi",
            "url": "http://localhost:8000/openapi.json",
            "is_user_authenticated": False
        },
        "logo_url": "example.com/logo.png",
        "contact_email": "myemail@example.com",
        "legal_info_url": "http://www.example.com/legal"
    }
