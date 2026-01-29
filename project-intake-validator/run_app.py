#!/usr/bin/env python3
"""
Startup helper for Project Intake Validator
Ensures all configuration is correct before starting the app
"""
import sys
import os
from pathlib import Path

# Add current directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

def check_environment():
    """Check if required environment variables are set"""
    print("Checking environment configuration...")
    
    required_vars = [
        "AZURE_OPENAI_API_KEY",
        "AZURE_OPENAI_ENDPOINT",
        "AZURE_OPENAI_DEPLOYMENT_NAME",
        "AZURE_OPENAI_API_VERSION"
    ]
    
    missing = []
    for var in required_vars:
        if var not in os.environ or os.environ[var] in ["", "YOUR_NEW_KEY_HERE", "https://<your-resource-name>.cognitiveservices.azure.com/"]:
            missing.append(var)
            print(f"  ✗ {var}: Not configured")
        else:
            value = os.environ[var]
            if "key" in var.lower() or "api" in var.lower():
                display_value = value[:10] + "..." if len(value) > 10 else value
            else:
                display_value = value
            print(f"  ✓ {var}: {display_value}")
    
    if missing:
        print(f"\n⚠ Missing or invalid configuration for: {', '.join(missing)}")
        print("Please set these environment variables in .env file or system environment")
        return False
    
    print("\n✓ All environment variables are configured")
    return True

def main():
    """Main entry point"""
    from dotenv import load_dotenv
    
    # Load .env file
    env_file = Path(__file__).parent / ".env"
    if env_file.exists():
        print(f"Loading environment from: {env_file}")
        load_dotenv(env_file)
    else:
        print("Warning: .env file not found")
    
    # Check environment
    if not check_environment():
        print("\n" + "=" * 60)
        print("ERROR: Environment configuration incomplete")
        print("=" * 60)
        print("\nTo fix, edit the .env file with your Azure OpenAI credentials:")
        print("  1. AZURE_OPENAI_API_KEY - Your API key from Azure Portal")
        print("  2. AZURE_OPENAI_ENDPOINT - Your resource endpoint URL")
        print("  3. AZURE_OPENAI_DEPLOYMENT_NAME - Your model deployment name (e.g., gpt-4o)")
        print("  4. AZURE_OPENAI_API_VERSION - API version (e.g., 2025-01-01-preview)")
        return 1
    
    print("\n" + "=" * 60)
    print("Starting Streamlit app...")
    print("=" * 60)
    
    # Import and run streamlit
    import subprocess
    result = subprocess.run(
        [sys.executable, "-m", "streamlit", "run", "streamlit_app.py"],
        cwd=Path(__file__).parent
    )
    return result.returncode

if __name__ == "__main__":
    sys.exit(main())
