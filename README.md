# ChatGPT Plugin Template

A simple ChatGPT Plugin example using Python, FastAPI, and uvicorn.  

### Installation

- Clone this repository
- Run the following commands to create a virtual environment, install Python packages, and start the API
> Prerequisites: Python 3 is already installed on your system

```sh
python3 -m venv venv

source venv/bin/activate

pip install -r requirements.txt

uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### Verify it's working using `curl` or the `api.http` file

```sh
### curl commands ###

# OpenAI's request to get manifest.json from a well-known endpoint
curl http://localhost:8000/.well-known/ai-plugin.json

# OpenAI's request to get openapi spec (URL is configured in the ai-plugin.json file)
curl http://localhost:8000/openapi.json

# Swagger docs
curl http://localhost:8000/docs

# Sample request and response from the query API
curl commands -sX POST http://localhost:8000/query \
    -d '{"queries":[{"query": "Query 1"},{"query": "Query 2"},{"query": "Query 3"}]}' \
    -H 'Content-Type: application/json' | python3 -mjson.tool
```

- `api.http` -  Install the [RestClient extension](https://marketplace.visualstudio.com/items?itemName=humao.rest-client) and send requests

## Make changes to support your plugin's use case
Modify the `config.py` file with your plugin's information.

## Add authentication for your plugin
Follow the instructions here to enable authentication on your plugin: https://platform.openai.com/docs/plugins/authentication/no-authentication

Plugins provide various authentication schemas for different use cases
The `manifest.json` file is used to specify the authentication schema for the plugin

For schemes requiring your `OPEN_API_KEY` or `BEARER_TOKEN`, set them as environment variables by either creating a `.env` file (Option 1)
or exporting them as variables (Option 2):
```sh
# Option 1 (.env)
mv .env.example .env
# TODO: add values to .env 

# Option 2 (export)
export BEARER_TOKEN=<your BEARER_TOKEN>
export OPENAI_API_KEY=<your OPENAI_API_KEY>
```

1. No auth
    - No-auth flow allows users to send requests directly to API without any restrictions
    ```json
        "auth": {
            "type": "none"
        },
    ```
2. Service level
    - Service level authentication requires a client secret during plugin installation for authenticated traffic from OpenAI plugins
    ```json
        "auth": {
            "type": "service_http",
            "authorization_type": "bearer",
            "verification_tokens": {
                "openai": "abcdefb8a57e45bc8ad7dea5bc2f1234"
            }
        },
    ```
3. User level
    - User level authentication enables end users to copy and paste their secret API key into the ChatGPT UI during plugin install
    ```json
        "auth": {
            "type": "user_http",
            "authorization_type": "bearer",
        },
    ```
3. OAuth
    - OAuth authentication is compatible with the plugin protocol, with an example OAuth flow provided in the manifest
    - OAuth flow requires the provision of OAuth client_id and client_secret when setting up the plugin with ChatGPT. The user logs in through the plugin's website when installing the plugin and ChatGPT makes a POST request to authorization_url after redirecting to the redirect_uri.
        ```json
       "auth": {
            "type": "oauth",
            "client_url": "https://example.com/authorize",
            "scope": "",
            "authorization_url": "https://example.com/token",
            "authorization_content_type": "application/json",
            "verification_tokens": {
                "openai": "123456"
            }
        },
        ```