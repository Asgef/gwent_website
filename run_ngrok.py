from dotenv import load_dotenv, set_key
import os
from pyngrok import ngrok


load_dotenv()

ngrok_token = os.getenv("NGROK_AUTHTOKEN")
if not ngrok_token:
    raise ValueError("NGROK_AUTHTOKEN not found in environment variables")

ngrok.set_auth_token(ngrok_token)

http_tunnel = ngrok.connect(8000)

public_url = http_tunnel.public_url
print(f" * ngrok tunnel \"{public_url}\" -> \"http://localhost:8000\"")

set_key('.env', 'NGROK_URL', public_url)

input("Press Enter to exit...\n\n")
