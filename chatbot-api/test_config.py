#!/usr/bin/env python3
"""Test script to verify configuration loading."""

import os
import sys
from pathlib import Path

# Add the app directory to the path
sys.path.insert(0, str(Path(__file__).parent))

def test_env_loading():
    """Test environment variable loading."""
    print("=== Environment Variable Test ===")
    print(f"OLLAMA_MODEL from os.getenv: {os.getenv('OLLAMA_MODEL', 'Not set')}")
    print(f"Current working directory: {os.getcwd()}")
    print(f".env file exists: {os.path.exists('.env')}")
    
    if os.path.exists('.env'):
        print("\n=== .env file contents ===")
        with open('.env', 'r') as f:
            for line_num, line in enumerate(f, 1):
                if line.strip() and not line.strip().startswith('#'):
                    print(f"{line_num}: {line.strip()}")
    
    print("\n=== Testing pydantic-settings loading ===")
    try:
        from app.config import settings
        print(f"Settings ollama_model: {settings.ollama_model}")
        print(f"Settings ollama_base_url: {settings.ollama_base_url}")
        print(f"Settings api_host: {settings.api_host}")
        print(f"Settings api_port: {settings.api_port}")
    except Exception as e:
        print(f"Error loading settings: {e}")


if __name__ == "__main__":
    test_env_loading() 