import os
from pathlib import Path
from dotenv import load_dotenv
from supabase import create_client, Client

# Carrega o .env que está nesta mesma pasta (backend/), não importa
# de onde você rode o programa.
env_path = Path(__file__).parent / ".env"
load_dotenv(env_path)

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

# Se as credenciais não vieram, avisa logo, com uma mensagem clara.
if not SUPABASE_URL or not SUPABASE_KEY:
    raise RuntimeError("Faltam SUPABASE_URL ou SUPABASE_KEY no arquivo .env")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)