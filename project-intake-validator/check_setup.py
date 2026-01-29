#!/usr/bin/env python3
"""
Validation script to quickly test if the application can start
Run this before running streamlit run streamlit_app.py
"""
import sys
import os
from pathlib import Path

# Add current directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

def main():
    from dotenv import load_dotenv
    
    print("=" * 70)
    print("PROJECT INTAKE VALIDATOR - PRE-FLIGHT CHECKS")
    print("=" * 70)
    
    # Load .env
    env_file = Path(__file__).parent / ".env"
    if env_file.exists():
        load_dotenv(env_file)
    
    print("\n1. Checking Python environment...")
    print(f"   Python version: {sys.version.split()[0]}")
    print(f"   Path: {sys.executable}")
    
    print("\n2. Testing imports...")
    errors = []
    try:
        from src.piv.graph.graph import build_graph
        print("   ✓ Core graph builder imports OK")
    except Exception as e:
        errors.append(f"Graph builder import failed: {e}")
        print(f"   ✗ {errors[-1]}")
    
    try:
        from src.piv.llm.azure_openai_client import AzureOpenAILLM
        print("   ✓ Azure OpenAI client imports OK")
    except Exception as e:
        errors.append(f"Azure OpenAI import failed: {e}")
        print(f"   ✗ {errors[-1]}")
    
    print("\n3. Checking environment variables...")
    required = {
        "AZURE_OPENAI_API_KEY": "API Key",
        "AZURE_OPENAI_ENDPOINT": "Endpoint URL",
        "AZURE_OPENAI_DEPLOYMENT_NAME": "Deployment name",
        "AZURE_OPENAI_API_VERSION": "API version"
    }
    
    config_ok = True
    for var, desc in required.items():
        val = os.environ.get(var, "").strip()
        if not val or val in ["YOUR_NEW_KEY_HERE", "https://<your-resource-name>.cognitiveservices.azure.com/"]:
            print(f"   ✗ {desc} ({var}): NOT SET")
            config_ok = False
        else:
            if "key" in var.lower():
                display = val[:8] + "..." if len(val) > 8 else val
            else:
                display = val
            print(f"   ✓ {desc}: {display}")
    
    print("\n4. Checking files...")
    required_files = [
        "streamlit_app.py",
        "main.py",
        "prompts/section_extractor.md",
        ".env",
    ]
    
    for file in required_files:
        fpath = Path(__file__).parent / file
        if fpath.exists():
            print(f"   ✓ {file}")
        else:
            errors.append(f"Missing file: {file}")
            print(f"   ✗ {file}")
    
    print("\n" + "=" * 70)
    
    if errors:
        print("ERRORS FOUND:")
        for i, err in enumerate(errors, 1):
            print(f"  {i}. {err}")
        print("\nFIX: Check .env file configuration and ensure all dependencies are installed")
        return 1
    elif not config_ok:
        print("WARNING: Azure OpenAI configuration is incomplete")
        print("\nFIX: Edit .env file with your Azure OpenAI credentials")
        return 1
    else:
        print("✓ All checks passed!")
        print("\nYou can now run the app with:")
        print("  streamlit run streamlit_app.py")
        return 0

if __name__ == "__main__":
    sys.exit(main())
