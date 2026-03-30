from config.settings import GROQ_API_KEY
import os

print(f"Key from config.settings: {GROQ_API_KEY[:8]}...")
if GROQ_API_KEY == os.getenv("GROQ_API_KEY"):
    print("✅ Key matches os.getenv")
else:
    print("❌ Key MISMATCH!")
