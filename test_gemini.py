#!/usr/bin/env python
"""Test Gemini LLM integration"""

import os
import sys

# Set API key from .env file
from dotenv import load_dotenv
load_dotenv()

print("Testing Gemini LLM Integration...")
print("=" * 70)

# Check API key
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    print("❌ GOOGLE_API_KEY not found in environment")
    sys.exit(1)

print(f"✅ API key found: {api_key[:20]}...")

# Test Gemini import
try:
    from langchain_google_genai import ChatGoogleGenerativeAI
    from langchain_core.messages import HumanMessage, SystemMessage
    print("✅ LangChain Gemini imported")
    
    # Initialize Gemini
    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-flash",
        google_api_key=api_key,
        temperature=0.7
    )
    print("✅ Gemini LLM initialized")
    
    # Test simple prompt
    system_prompt = "You are a knowledgeable museum tour guide."
    user_query = "Describe The Starry Night by Vincent van Gogh in 3 sentences."
    
    print("\n📤 Sending test request to Gemini API...")
    response = llm.invoke([
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_query)
    ])
    
    print("✅ Gemini API response received!")
    print("\n" + "=" * 70)
    print("RESPONSE:")
    print(response.content)
    print("=" * 70)
    print(f"\n✅ SUCCESS: Gemini LLM integration works!")
    print(f"Response length: {len(response.content)} characters")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
