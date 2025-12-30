import json
import re
from pathlib import Path
from datasets import Dataset, DatasetDict
import pandas as pd

def parse_homework_content(content, hw_number):
    """Parse homework markdown content to extract problems and solutions."""

    # This is a basic parser - you may need to adjust based on actual PDF structure
    problems = []

    # Try to split by problem numbers
    # Look for patterns like "Problem 1", "Question 1", "1.", etc.
    problem_pattern = r'(?:Problem|Question|Exercise|\n)[\s]*(\d+)[\.:\s]'

    parts = re.split(problem_pattern, content)

    if len(parts) > 1:
        # First part is usually header/introduction
        for i in range(1, len(parts), 2):
            if i + 1 < len(parts):
                problem_num = parts[i]
                problem_content = parts[i + 1].strip()

                problems.append({
                    "homework": f"hw{hw_number}",
                    "problem_number": problem_num,
                    "content": problem_content,
                    "full_id": f"hw{hw_number}_problem{problem_num}"
                })
    else:
        # If no clear problem structure, treat as single content
        problems.append({
            "homework": f"hw{hw_number}",
            "problem_number": "1",
            "content": content.strip(),
            "full_id": f"hw{hw_number}_problem1"
        })

    return problems

def create_benchmark():
    """Create benchmark dataset from parsed PDFs."""

    parsed_dir = Path("parsed_data")

    if not parsed_dir.exists():
        print("Error: parsed_data directory not found. Run extract_pdfs.py first.")
        return

    # Load extraction metadata
    metadata_file = parsed_dir / "extraction_metadata.json"
    if not metadata_file.exists():
        print("Error: extraction_metadata.json not found. Run extract_pdfs.py first.")
        return

    with open(metadata_file, "r", encoding="utf-8") as f:
        metadata = json.load(f)

    # Process all successfully parsed files
    all_problems = []

    for hw_name, info in sorted(metadata.items()):
        if info["status"] != "success":
            print(f"Skipping {hw_name} (parsing failed)")
            continue

        # Extract homework number
        hw_number = re.search(r'hw(\d+)', hw_name)
        if not hw_number:
            print(f"Warning: Could not extract homework number from {hw_name}")
            continue
        hw_num = hw_number.group(1)

        # Read parsed content
        md_file = Path(info["parsed_file"])
        with open(md_file, "r", encoding="utf-8") as f:
            content = f.read()

        # Parse into problems
        problems = parse_homework_content(content, hw_num)
        all_problems.extend(problems)

        print(f"Processed {hw_name}: {len(problems)} problems")

    print(f"\nTotal problems extracted: {len(all_problems)}")

    # Create dataset
    df = pd.DataFrame(all_problems)
    dataset = Dataset.from_pandas(df)

    # Save as different formats
    output_dir = Path("benchmark_dataset")
    output_dir.mkdir(exist_ok=True)

    # Save as JSON
    with open(output_dir / "dataset.json", "w", encoding="utf-8") as f:
        json.dump(all_problems, f, indent=2, ensure_ascii=False)

    # Save as JSONL
    with open(output_dir / "dataset.jsonl", "w", encoding="utf-8") as f:
        for problem in all_problems:
            f.write(json.dumps(problem, ensure_ascii=False) + "\n")

    # Save dataset info
    dataset.save_to_disk(str(output_dir / "huggingface_dataset"))

    print(f"\nBenchmark dataset created successfully!")
    print(f"Output directory: {output_dir}")
    print(f"Formats: JSON, JSONL, HuggingFace Dataset")

    # Print sample
    if all_problems:
        print(f"\nSample problem:")
        print(f"ID: {all_problems[0]['full_id']}")
        print(f"Homework: {all_problems[0]['homework']}")
        print(f"Problem: {all_problems[0]['problem_number']}")
        print(f"Content preview: {all_problems[0]['content'][:200]}...")

    return dataset

if __name__ == "__main__":
    create_benchmark()
