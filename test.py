from supabase import create_client
import os
from dotenv import load_dotenv

load_dotenv()

# Enforce UTF-8 environment globally
os.environ["PYTHONUTF8"] = "1"
os.environ["PYTHONIOENCODING"] = "utf-8"

SUPABASE_URL = os.getenv("SUPABASE_URL").encode("utf-8", "ignore").decode("utf-8")
SUPABASE_KEY = os.getenv("SUPABASE_KEY").encode("utf-8", "ignore").decode("utf-8")

supabase = create_client(SUPABASE_URL.strip(), SUPABASE_KEY.strip())
