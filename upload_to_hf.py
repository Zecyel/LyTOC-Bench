import os
from pathlib import Path
from huggingface_hub import HfApi, create_repo
from datasets import load_from_disk
from dotenv import load_dotenv

load_dotenv()

def upload_to_huggingface(repo_name, private=False):
    """Upload benchmark dataset to HuggingFace."""

    # Check if dataset exists
    dataset_path = Path("benchmark_dataset/huggingface_dataset")
    if not dataset_path.exists():
        print("Error: Dataset not found. Run create_benchmark.py first.")
        return

    # Get HuggingFace token
    token = os.getenv("HF_TOKEN")
    if not token:
        print("Error: HF_TOKEN not found in .env file")
        return

    # Initialize HF API
    api = HfApi(token=token)

    # Create repository
    print(f"Creating repository: {repo_name}")
    try:
        repo_url = create_repo(
            repo_id=repo_name,
            repo_type="dataset",
            private=private,
            exist_ok=True,
            token=token
        )
        print(f"Repository created/found: {repo_url}")
    except Exception as e:
        print(f"Error creating repository: {e}")
        return

    # Load dataset
    print("Loading dataset...")
    dataset = load_from_disk(str(dataset_path))

    # Upload dataset
    print("Uploading dataset to HuggingFace...")
    try:
        dataset.push_to_hub(
            repo_id=repo_name,
            token=token,
            private=private
        )
        print(f"✓ Dataset uploaded successfully!")
        print(f"View at: https://huggingface.co/datasets/{repo_name}")
    except Exception as e:
        print(f"Error uploading dataset: {e}")
        return

    # Upload additional files (README, JSON, JSONL)
    print("\nUploading additional files...")
    files_to_upload = [
        ("HF_README.md", "README.md"),  # Upload HF_README.md as README.md
        ("benchmark_dataset/dataset.json", "dataset.json"),
        ("benchmark_dataset/dataset.jsonl", "dataset.jsonl"),
    ]

    for local_path, repo_path in files_to_upload:
        if Path(local_path).exists():
            try:
                api.upload_file(
                    path_or_fileobj=local_path,
                    path_in_repo=repo_path,
                    repo_id=repo_name,
                    repo_type="dataset",
                    token=token
                )
                print(f"✓ Uploaded {local_path}")
            except Exception as e:
                print(f"✗ Error uploading {local_path}: {e}")

    print(f"\n{'='*50}")
    print(f"Upload complete!")
    print(f"Dataset URL: https://huggingface.co/datasets/{repo_name}")

if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python upload_to_hf.py <username/repo-name> [--private]")
        print("Example: python upload_to_hf.py myusername/lytoc-benchmark")
        sys.exit(1)

    repo_name = sys.argv[1]
    private = "--private" in sys.argv

    upload_to_huggingface(repo_name, private)
