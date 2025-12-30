#!/usr/bin/env python3
"""
Helper script to run the full benchmark pipeline.
"""

import sys
import subprocess
from pathlib import Path

def check_env_file():
    """Check if .env file exists."""
    if not Path(".env").exists():
        print("⚠ Warning: .env file not found!")
        print("Please create a .env file with your API keys:")
        print("  cp .env.example .env")
        print("  # Edit .env and add your keys")
        return False
    return True

def run_command(cmd, description):
    """Run a command and handle errors."""
    print(f"\n{'='*60}")
    print(f"📍 {description}")
    print(f"{'='*60}\n")

    try:
        result = subprocess.run(cmd, check=True, shell=True)
        print(f"\n✓ {description} completed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n✗ Error: {description} failed!")
        print(f"Error code: {e.returncode}")
        return False

def main():
    """Run the benchmark creation pipeline."""

    print("🚀 LyTOC Benchmark Creation Pipeline")
    print("="*60)

    # Check environment
    if not check_env_file():
        response = input("\nContinue anyway? (y/n): ")
        if response.lower() != 'y':
            print("Exiting...")
            sys.exit(1)

    # Step 1: Extract PDFs
    print("\n📄 Step 1: Extracting content from PDFs...")
    if not run_command("python extract_pdfs.py", "PDF Extraction"):
        print("\nPipeline stopped due to error.")
        sys.exit(1)

    # Step 2: Create benchmark
    print("\n📊 Step 2: Creating benchmark dataset...")
    if not run_command("python create_benchmark.py", "Benchmark Creation"):
        print("\nPipeline stopped due to error.")
        sys.exit(1)

    # Step 3: Ask about upload
    print("\n" + "="*60)
    print("✅ Benchmark dataset created successfully!")
    print("="*60)

    response = input("\n📤 Would you like to upload to HuggingFace? (y/n): ")
    if response.lower() == 'y':
        repo_name = input("Enter repository name (e.g., username/repo-name): ")
        private = input("Make repository private? (y/n): ")

        cmd = f"python upload_to_hf.py {repo_name}"
        if private.lower() == 'y':
            cmd += " --private"

        run_command(cmd, "HuggingFace Upload")

    print("\n" + "="*60)
    print("🎉 Pipeline complete!")
    print("="*60)

if __name__ == "__main__":
    main()
