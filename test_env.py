from dotenv import load_dotenv
import os

loaded = load_dotenv()

print("Loaded:", loaded)
print("Current directory:", os.getcwd())
print("ENV file exists:", os.path.exists(".env"))
print("Key:", os.getenv("GROQ_API_KEY"))