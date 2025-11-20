import os
from dotenv import load_dotenv

# Load API key
load_dotenv()
api_key = os.getenv('GOOGLE_API_KEY')
print(f"API Key loaded: {api_key[:20]}..." if api_key else "No API key found")

# Test basic Gemini API
try:
    from google import genai
    
    client = genai.Client(api_key=api_key)
    
    response = client.models.generate_content(
        model="gemini-2.0-flash-exp",  # Latest free model
        contents="Explain how AI works in a few words",
    )
    
    print("\n✅ SUCCESS! Gemini API works:")
    print(response.text)
    
except Exception as e:
    print(f"\n❌ ERROR: {type(e).__name__}: {e}")
    print("\nTrying alternative model names...")
    
    # Try different model names
    models_to_try = [
        "gemini-pro",
        "gemini-1.5-flash", 
        "gemini-1.5-pro",
        "models/gemini-pro"
    ]
    
    for model in models_to_try:
        try:
            print(f"\nTrying {model}...")
            client = genai.Client(api_key=api_key)
            response = client.models.generate_content(
                model=model,
                contents="Explain AI briefly",
            )
            print(f"✅ {model} WORKS!")
            print(response.text)
            break
        except Exception as e2:
            print(f"❌ {model} failed: {e2}")