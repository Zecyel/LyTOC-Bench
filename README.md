# LyTOC Benchmark

This repository contains a benchmark dataset extracted from homework PDFs.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up environment variables:
```bash
cp .env.example .env
# Edit .env and add your API keys
```

3. Extract content from PDFs:
```bash
python extract_pdfs.py
```

4. Create the benchmark dataset:
```bash
python create_benchmark.py
```

## Dataset Structure

The benchmark dataset includes homework problems and solutions extracted from PDF files.

## Upload to HuggingFace

```bash
python upload_to_hf.py
```
