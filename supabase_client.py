import os
from supabase import create_client

from dotenv import load_dotenv #Hides api key so it doesnt get abused on GitHub
load_dotenv()

SupabaseURL= os.environ.get("SUPABASE_PROJECT_URL")

SupabaseKEY = os.environ.get("SUPABASE_KEY")

supabase= create_client(SupabaseURL, SupabaseKEY)