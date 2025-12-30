---
license: mit
task_categories:
- question-answering
- text-generation
language:
- en
tags:
- theory-of-computation
- algorithms
- computer-science
- homework
- exercises
size_categories:
- n<1K
pretty_name: LyTOC Benchmark
---

# LyTOC Benchmark Dataset

A curated collection of Theory of Computation and Algorithms homework exercises, extracted from academic PDFs using OCR and structured for machine learning evaluation.

## Dataset Description

### Dataset Summary

The LyTOC (Logic and Theory of Computation) Benchmark contains 27 carefully extracted exercises from 9 homework assignments covering fundamental topics in theoretical computer science. Each exercise is preserved with its original LaTeX mathematical notation, making it suitable for evaluating language models on formal reasoning tasks.

**Key Features:**
- 27 exercises across 9 homework assignments
- Topics: automata theory, complexity theory, Turing machines, formal languages, algorithm analysis
- LaTeX mathematical notation preserved
- Structured with exercise numbers
- Clean extraction with OCR post-processing

### Supported Tasks

- **Question Answering**: Answer theoretical computer science questions
- **Mathematical Reasoning**: Solve problems involving formal proofs and mathematical notation
- **Text Generation**: Generate solutions to computational theory problems
- **Educational Assessment**: Evaluate understanding of CS theory concepts

### Languages

- English (en)

## Dataset Structure

### Data Instances

Each instance represents a single exercise:

```json
{
  "homework": "hw1",
  "exercise_number": "3",
  "content": "Let $\\Sigma = \\{0, 1\\}$. Let language\n\n$$L = \\{w \\in \\{0, 1\\}^* : w \\text{ has an unequal number of 0's and 1's}\\}.$$\n\nProve $L^* = \\Sigma^*$.",
  "full_id": "hw1_ex3"
}
```

### Data Fields

- `homework` (string): Homework identifier (e.g., "hw1", "hw2", "hw13")
- `exercise_number` (string): Exercise number within the homework (e.g., "1", "2", "3")
- `content` (string): Full exercise text including LaTeX mathematical notation
- `full_id` (string): Unique identifier for the exercise (e.g., "hw1_ex3", "hw2_ex3_1")

### Data Splits

The dataset consists of a single split containing all 27 exercises.

## Dataset Statistics

- **Total Exercises**: 27
- **Homeworks**: 9 (hw1, hw2, hw3, hw5, hw6, hw9, hw10, hw11, hw13)
- **Average Content Length**: ~200-500 characters per exercise

### Topic Distribution

The exercises cover the following topics:

- **Asymptotic Analysis**: Big-O notation, growth rates
- **Finite Automata**: DFA, NFA, regular expressions
- **Formal Languages**: Regular languages, context-free languages
- **Turing Machines**: Decidability, computability
- **Complexity Theory**: P, NP, NP-completeness, reductions
- **Algorithm Design**: Time complexity, space complexity

## Dataset Creation

### Source Data

The dataset was created from homework assignments in a Theory of Computation and Algorithms course.

#### Data Collection

- **Source**: Academic homework PDFs (9 files)
- **Extraction Method**: SimpleTex OCR API
- **Processing**: Automated regex-based exercise splitting
- **Quality Control**: Manual verification of extraction accuracy

#### Data Processing Pipeline

1. **PDF to Image**: Convert each PDF page to high-resolution images
2. **OCR Processing**: Extract text using SimpleTex OCR API
3. **Punctuation Normalization**: Convert Chinese punctuation to English equivalents
4. **Exercise Splitting**: Use regex patterns to identify exercise boundaries
6. **Metadata Generation**: Create unique identifiers and structure data

### Annotations

The dataset does not include solutions or annotations. It contains only problem statements as extracted from the source materials.

## Considerations for Using the Data

### Recommended Uses

- Evaluating language models on formal reasoning tasks
- Training models for mathematical problem understanding
- Benchmarking CS theory knowledge in AI systems
- Educational tool development for computer science

### Limitations

- **No Solutions**: The dataset contains only problem statements, not solutions
- **OCR Artifacts**: Some mathematical notation may have minor OCR errors
- **Limited Scope**: Covers specific topics in theory of computation and algorithms
- **No Visual Content**: Diagrams and figures from PDFs are not included
- **Language**: English only

### Ethical Considerations

This dataset is intended for educational and research purposes. Users should:
- Respect academic integrity when using for educational purposes
- Not use for automated homework completion systems
- Cite appropriately when using in research

## Additional Information

### Licensing Information

This dataset is released under the MIT License.

### Citation Information

If you use this dataset in your research, please cite:

```bibtex
@misc{lytoc-benchmark-2025,
  title={LyTOC Benchmark: Theory of Computation and Algorithms Exercise Dataset},
  author={LyTOC Contributors},
  year={2025},
  howpublished={\\url{https://huggingface.co/datasets/lytoc-benchmark}}
}
```

### Dataset Curators

Dataset created using:
- SimpleTex OCR API for PDF extraction
- Custom Python scripts for data processing
- Claude Code for automation and quality assurance

### Contact

For questions or issues regarding this dataset, please open an issue on the dataset repository.

## Usage Example

```python
from datasets import load_dataset

# Load the dataset
dataset = load_dataset("Zecyel/LyTOC")

# Access an exercise
exercise = dataset['train'][0]
print(f"Exercise ID: {exercise['full_id']}")
print(f"Content: {exercise['content']}")

# Filter by homework
hw1_exercises = [ex for ex in dataset['train'] if ex['homework'] == 'hw1']
print(f"Homework 1 has {len(hw1_exercises)} exercises")
```

## Version History

- **v1.0.0** (2025-12-30): Initial release with 27 exercises from 9 homework assignments
