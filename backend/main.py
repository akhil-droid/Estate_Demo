"""
UK Estate Agency AI - Main Entry Point
=======================================
Run this file to start the multi-agent system.
"""

import os
import uvicorn
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


def print_banner():
    """Print startup banner."""
    print("\n" + "=" * 70)
    print("🏠 UK ESTATE AGENCY AI - MULTI-AGENT SYSTEM")
    print("=" * 70)
    print("\n🤖 Agents:")
    print("   🎯 Orchestrator - Central Coordinator")
    print("   🔍 Scout - Data Retrieval")
    print("   🧠 Intelligence - Analysis & Scoring")
    print("   ✍️  Content - Content Generation")
    print("   ✅ Compliance - Validation")
    print("\n📊 Data Source: CSV files from demo_mock_data/")
    print("👤 Human Approval: Terminal Input")
    print("\n" + "-" * 70)
    print("🌐 API Server: http://localhost:8000")
    print("📚 API Docs: http://localhost:8000/docs")
    print("🔄 ReDoc: http://localhost:8000/redoc")
    print("-" * 70 + "\n")


def check_openai_key():
    """Check if OpenAI API key is set."""
    key = os.getenv("OPENAI_API_KEY", "")
    if not key or key == "your-api-key-here":
        print("⚠️  WARNING: OPENAI_API_KEY not set!")
        print("   Set it using: export OPENAI_API_KEY='your-key-here'")
        print("   Or add it to a .env file")
        print("")
        return False
    else:
        print(f"✅ OpenAI API Key: {'*' * 20}{key[-4:]}")
        return True


def check_data_files():
    """Check if data files exist."""
    data_path = os.path.join(os.path.dirname(__file__), "..", "demo_mock_data")
    
    required_files = [
        "entities/properties.csv",
        "entities/vendors.csv",
        "entities/buyers.csv",
        "entities/employees.csv",
    ]
    
    all_found = True
    for file in required_files:
        full_path = os.path.join(data_path, file)
        if os.path.exists(full_path):
            print(f"✅ Found: {file}")
        else:
            print(f"❌ Missing: {file}")
            all_found = False
    
    return all_found


def main():
    """Main entry point."""
    print_banner()
    
    print("🔍 Checking configuration...\n")
    
    key_ok = check_openai_key()
    print("")
    data_ok = check_data_files()
    print("")
    
    if not key_ok:
        print("⚠️  OpenAI API key not configured. LLM calls will fail.")
        print("   The system will start, but agent responses will error.")
        print("")
    
    if not data_ok:
        print("⚠️  Some data files missing. Data lookups may fail.")
        print("   Place demo_mock_data folder in the project root.")
        print("")
    
    print("🚀 Starting server...\n")
    
    # Import and run the FastAPI app
    from api import app
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )


if __name__ == "__main__":
    main()