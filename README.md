# LyTOC Benchmark

This repository contains a benchmark dataset extracted from homework PDFs using SimpleTex OCR API.

## Features

- Automated PDF content extraction using SimpleTex OCR API
- Structured benchmark dataset creation
- Multiple export formats (JSON, JSONL, HuggingFace Dataset)
- Easy upload to HuggingFace Hub
- Interactive pipeline runner

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set Up API Keys

```bash
cp .env.example .env
# Edit .env and add your API keys:
# - OCR_UAT: Get from https://simpletex.cn
# - HF_TOKEN: Get from https://huggingface.co/settings/tokens
```

### 3. Run the Pipeline

**Option A: Interactive Pipeline** (Recommended)
```bash
python run_pipeline.py
```

**Option B: Manual Steps**
```bash
# Extract PDFs
python extract_pdfs.py

# Create benchmark dataset
python create_benchmark.py

# Upload to HuggingFace
python upload_to_hf.py <username/repo-name> [--private]
```

## Project Structure

```
lytoc/
├── raw/                          # Source PDF files
├── parsed_data/                  # Extracted markdown content
│   ├── hw*.md                   # Individual parsed files
│   └── extraction_metadata.json # Extraction status
├── benchmark_dataset/            # Final benchmark dataset
│   ├── dataset.json             # JSON format
│   ├── dataset.jsonl            # JSONL format
│   └── huggingface_dataset/     # HuggingFace format
├── extract_pdfs.py              # PDF extraction script
├── create_benchmark.py          # Benchmark creation script
├── upload_to_hf.py              # HuggingFace upload script
├── run_pipeline.py              # Interactive pipeline runner
└── DATASET_CARD.md              # Dataset documentation
```

## Dataset Structure

Each problem in the dataset contains:
- `homework`: Homework identifier (e.g., "hw1", "hw2")
- `problem_number`: Problem number within the homework
- `content`: Full problem text and description
- `full_id`: Unique identifier (e.g., "hw1_problem1")

Example:
```json
{
  "homework": "hw1",
  "problem_number": "1",
  "content": "Problem statement...",
  "full_id": "hw1_problem1"
}
```

## Scripts

### extract_pdfs.py
Extracts content from PDF files in the `raw/` directory using SimpleTex OCR API.
- Converts PDFs to markdown format via OCR
- Saves parsed content to `parsed_data/`
- Creates extraction metadata

### create_benchmark.py
Processes parsed content into a structured benchmark dataset.
- Parses markdown content to extract individual problems
- Creates dataset in multiple formats
- Generates statistics and sample output

### upload_to_hf.py
Uploads the benchmark dataset to HuggingFace Hub.
```bash
python upload_to_hf.py username/repo-name [--private]
```

### run_pipeline.py
Interactive script that runs the complete pipeline with user prompts.

## Requirements

- Python 3.8+
- SimpleTex API token (OCR_UAT)
- HuggingFace account and token (for upload)

## License

MIT License - See LICENSE file for details

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
