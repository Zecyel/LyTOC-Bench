"""
Create benchmark dataset from parsed PDF content.

This script reads all markdown files from parsed_data/ directory,
splits them into individual exercises, and creates a structured dataset.
"""

import json
import re
from pathlib import Path
from datasets import Dataset
import pandas as pd


def extract_homework_number(filename):
    """Extract homework number from filename like 'hw1.md' -> '1'."""
    match = re.search(r'hw(\d+)', filename)
    return match.group(1) if match else None


def split_exercises(content, hw_number):
    """
    Split homework content into individual exercises.

    Pattern matches:
    - "1 (30'). Exercise content..."
    - "2 (40'). Exercise content..."
    - "3. Exercise content..." (without time)

    Args:
        content: Full markdown content
        hw_number: Homework number (e.g., "1", "2", "13")

    Returns:
        List of exercise dictionaries
    """
    exercises = []

    # Remove the header (first few lines with title and date)
    lines = content.split('\n')
    content_start = 0
    for i, line in enumerate(lines):
        if re.match(r'^\d+\s*\(', line):  # First exercise starts
            content_start = i
            break

    if content_start > 0:
        content = '\n'.join(lines[content_start:])

    # Pattern to match exercise numbers: "1 (30'). " or "1. " or "2 (40'). "
    # Matches: digit(s), optional space, optional (time'), optional space, period or dot
    exercise_pattern = r'^(\d+)\s*(?:\([^)]+\))?\s*\.?\s+'

    # Split by exercise numbers
    parts = re.split(exercise_pattern, content, flags=re.MULTILINE)

    # parts will be like: ['', '1', 'content1', '2', 'content2', '3', 'content3', ...]
    # Skip the first empty element and process pairs
    for i in range(1, len(parts), 2):
        if i + 1 < len(parts):
            exercise_num = parts[i].strip()
            exercise_content = parts[i + 1].strip()

            # Remove trailing page numbers (single digit at the end)
            exercise_content = re.sub(r'\n\d+\s*$', '', exercise_content)

            # Skip if content is too short (likely parsing error)
            if len(exercise_content) < 10:
                continue

            # No sub-problem splitting, treat each exercise as a single unit
            exercises.append({
                "homework": f"hw{hw_number}",
                "exercise_number": exercise_num,
                "content": exercise_content.strip(),
                "full_id": f"hw{hw_number}_ex{exercise_num}"
            })

    return exercises


def create_benchmark():
    """Create benchmark dataset from parsed PDFs."""

    parsed_dir = Path("parsed_data")

    if not parsed_dir.exists():
        print("Error: parsed_data directory not found. Run extract_pdfs.py first.")
        return

    # Get all markdown files
    md_files = sorted(parsed_dir.glob("hw*.md"))

    if not md_files:
        print("No homework markdown files found in parsed_data/")
        return

    print(f"Found {len(md_files)} homework files")
    print("="*60)

    # Process all files
    all_exercises = []

    for md_file in md_files:
        hw_number = extract_homework_number(md_file.name)
        if not hw_number:
            print(f"Warning: Could not extract homework number from {md_file.name}")
            continue

        # Read content
        with open(md_file, "r", encoding="utf-8") as f:
            content = f.read()

        # Split into exercises
        exercises = split_exercises(content, hw_number)
        all_exercises.extend(exercises)

        print(f"hw{hw_number}: {len(exercises)} exercises")

    print(f"\n{'='*60}")
    print(f"Total exercises extracted: {len(all_exercises)}")

    if not all_exercises:
        print("No exercises found. Check the parsing logic.")
        return

    # Create output directory
    output_dir = Path("benchmark_dataset")
    output_dir.mkdir(exist_ok=True)

    # Save as JSON
    json_file = output_dir / "dataset.json"
    with open(json_file, "w", encoding="utf-8") as f:
        json.dump(all_exercises, f, indent=2, ensure_ascii=False)
    print(f"\n✓ Saved to {json_file}")

    # Save as JSONL
    jsonl_file = output_dir / "dataset.jsonl"
    with open(jsonl_file, "w", encoding="utf-8") as f:
        for exercise in all_exercises:
            f.write(json.dumps(exercise, ensure_ascii=False) + '\n')
    print(f"✓ Saved to {jsonl_file}")

    # Create HuggingFace dataset
    df = pd.DataFrame(all_exercises)
    dataset = Dataset.from_pandas(df)
    dataset.save_to_disk(str(output_dir / "huggingface_dataset"))
    print(f"✓ Saved to {output_dir / 'huggingface_dataset'}")

    # Print statistics
    print(f"\n{'='*60}")
    print("Dataset Statistics:")
    print(f"  Total exercises: {len(all_exercises)}")
    print(f"  Homeworks: {len(set(ex['homework'] for ex in all_exercises))}")

    # Print sample
    if all_exercises:
        print(f"\n{'='*60}")
        print("Sample Exercise:")
        sample = all_exercises[0]
        print(f"  ID: {sample['full_id']}")
        print(f"  Homework: {sample['homework']}")
        print(f"  Exercise: {sample['exercise_number']}")
        print(f"  Content preview: {sample['content'][:200]}...")

    # Print breakdown by homework
    print(f"\n{'='*60}")
    print("Breakdown by Homework:")
    hw_counts = {}
    for ex in all_exercises:
        hw = ex['homework']
        hw_counts[hw] = hw_counts.get(hw, 0) + 1

    for hw in sorted(hw_counts.keys(), key=lambda x: int(x[2:])):
        print(f"  {hw}: {hw_counts[hw]} exercises")

    return dataset


if __name__ == "__main__":
    create_benchmark()
