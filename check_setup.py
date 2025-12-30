#!/usr/bin/env python3
"""
Check if the environment is properly configured for running the benchmark pipeline.
"""

import os
import sys
from pathlib import Path

def check_file_exists(filepath, description):
    """Check if a file exists."""
    if Path(filepath).exists():
        print(f"✓ {description}: Found")
        return True
    else:
        print(f"✗ {description}: Not found")
        return False

def check_env_variable(var_name):
    """Check if an environment variable is set."""
    value = os.getenv(var_name)
    if value and value != f"your_{var_name.lower()}_here":
        print(f"✓ {var_name}: Set")
        return True
    else:
        print(f"✗ {var_name}: Not set or using default value")
        return False

def check_python_version():
    """Check Python version."""
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"✓ Python version: {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print(f"✗ Python version: {version.major}.{version.minor}.{version.micro} (requires 3.8+)")
        return False

def check_package(package_name):
    """Check if a Python package is installed."""
    try:
        __import__(package_name.replace("-", "_"))
        print(f"✓ {package_name}: Installed")
        return True
    except ImportError:
        print(f"✗ {package_name}: Not installed")
        return False

def main():
    print("🔍 LyTOC Benchmark Environment Check")
    print("="*60)

    all_checks_passed = True

    # Check Python version
    print("\n📌 Python Version:")
    if not check_python_version():
        all_checks_passed = False

    # Check required files
    print("\n📌 Required Files:")
    checks = [
        ("requirements.txt", "Requirements file"),
        (".env", "Environment file"),
        ("raw", "Raw PDF directory"),
    ]

    for filepath, description in checks:
        if not check_file_exists(filepath, description):
            all_checks_passed = False

    # Check PDF files
    print("\n📌 PDF Files:")
    raw_dir = Path("raw")
    if raw_dir.exists():
        pdf_files = list(raw_dir.glob("*.pdf"))
        if pdf_files:
            print(f"✓ Found {len(pdf_files)} PDF files")
        else:
            print(f"✗ No PDF files found in raw/ directory")
            all_checks_passed = False
    else:
        print("✗ raw/ directory not found")
        all_checks_passed = False

    # Check environment variables
    print("\n📌 Environment Variables:")
    from dotenv import load_dotenv
    load_dotenv()

    env_vars = [
        "LLAMA_CLOUD_API_KEY",
        "HF_TOKEN",
    ]

    for var in env_vars:
        if not check_env_variable(var):
            all_checks_passed = False

    # Check Python packages
    print("\n📌 Python Packages:")
    packages = [
        "llama_parse",
        "datasets",
        "huggingface_hub",
        "dotenv",
        "pandas",
    ]

    for package in packages:
        if not check_package(package):
            all_checks_passed = False

    # Summary
    print("\n" + "="*60)
    if all_checks_passed:
        print("✅ All checks passed! You're ready to run the pipeline.")
        print("\nNext steps:")
        print("  python run_pipeline.py")
        print("  or")
        print("  python extract_pdfs.py")
    else:
        print("❌ Some checks failed. Please fix the issues above.")
        print("\nCommon fixes:")
        print("  1. Install dependencies: pip install -r requirements.txt")
        print("  2. Set up environment: cp .env.example .env && edit .env")
        print("  3. Add PDF files to raw/ directory")
    print("="*60)

    return 0 if all_checks_passed else 1

if __name__ == "__main__":
    sys.exit(main())
