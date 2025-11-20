#!/usr/bin/env python
"""Quick test of generate_description with Gemini API - minimal imports"""

import os
import sys

# Load .env
print("Loading environment...")
from dotenv import load_dotenv
load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    print("❌ No API key found")
    sys.exit(1)

print(f"✅ API key loaded: {api_key[:15]}...")

# Test direct Gemini call without heavy imports
print("\n1️⃣ Testing Gemini API directly...")
try:
    import google.generativeai as genai
    
    genai.configure(api_key=api_key)
    
    # Use gemini-pro (stable, widely available model)
    print("Using model: gemini-pro")
    model = genai.GenerativeModel('gemini-pro')
    
    prompt = """You are a knowledgeable museum tour guide.

Artwork: The Starry Night
Artist: Vincent van Gogh  
Period: 1889, Post-Impressionism

Generate an engaging, accessible description (150-250 words) for museum visitors."""
    
    print("📤 Calling Gemini API...")
    response = model.generate_content(prompt)
    
    print("\n" + "="*70)
    print("✅ GEMINI API WORKS!")
    print("="*70)
    print(response.text)
    print("="*70)
    print(f"\n✅ Generated {len(response.text)} characters")
    print("\n2️⃣ Next: Test with LangChain integration from app.py...")
    
except ImportError:
    print("❌ google-generativeai not installed")
    print("Installing...")
    os.system("pip install -q google-generativeai")
    print("Please run this script again")
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
