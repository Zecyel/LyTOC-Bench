---
license: mit
task_categories:
- question-answering
- text-generation
language:
- en
size_categories:
- n<1K
---

# LyTOC Benchmark Dataset

## Dataset Description

This dataset contains homework problems extracted from PDF files, designed for evaluating language models on academic problem-solving tasks.

### Dataset Summary

The LyTOC Benchmark is a collection of homework problems and exercises extracted from academic materials. Each entry includes:
- Homework identification (homework number)
- Problem number within the homework
- Full problem content
- Unique identifier

### Supported Tasks

- **Question Answering**: Answer academic homework problems
- **Text Generation**: Generate solutions to homework problems
- **Problem Understanding**: Comprehend and analyze problem statements

### Languages

- English (en)

## Dataset Structure

### Data Instances

Each instance in the dataset contains:

```json
{
  "homework": "hw1",
  "problem_number": "1",
  "content": "Problem statement and description...",
  "full_id": "hw1_problem1"
}
```

### Data Fields

- `homework` (string): Identifier for the homework set (e.g., "hw1", "hw2")
- `problem_number` (string): Problem number within the homework
- `content` (string): Full text of the problem statement
- `full_id` (string): Unique identifier combining homework and problem number

### Data Splits

Currently, the dataset consists of a single split containing all problems.

## Dataset Creation

### Source Data

The dataset was created by extracting content from homework PDF files using LlamaParse.

#### Data Collection

- **Source**: Academic homework PDFs
- **Extraction Method**: LlamaParse (automatic PDF parsing)
- **Processing**: Content structured into individual problems

#### Data Processing

1. PDF files parsed using LlamaParse to extract markdown content
2. Content split into individual problems using pattern matching
3. Each problem assigned unique identifiers
4. Data formatted for HuggingFace datasets

### Annotations

The dataset does not include human annotations or solutions. It contains only problem statements as extracted from the source PDFs.

## Considerations for Using the Data

### Social Impact

This dataset is intended for educational and research purposes, specifically for evaluating AI models on academic problem-solving tasks.

### Discussion of Biases

The dataset reflects the content and style of the source homework materials. Users should be aware that:
- Problems may vary in difficulty and subject matter
- Content is limited to the specific homeworks included
- Extraction quality depends on PDF structure and formatting

### Other Known Limitations

- Parsing quality may vary depending on PDF formatting
- Mathematical formulas and special symbols may not be perfectly preserved
- Figures and diagrams from PDFs are not included in text extraction

## Additional Information

### Licensing Information

This dataset is released under the MIT License.

### Citation Information

If you use this dataset, please cite:

```bibtex
@misc{lytoc-benchmark,
  title={LyTOC Benchmark Dataset},
  author={Your Name},
  year={2025},
  howpublished={\\url{https://huggingface.co/datasets/username/lytoc-benchmark}}
}
```

### Contributions

Dataset created using Claude Code and LlamaParse.
