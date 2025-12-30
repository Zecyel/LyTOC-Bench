"""
Extract content from PDF files using SimpleTex OCR API.

This script processes all PDF files in the raw/ directory and converts them
to markdown format using OCR, saving results to parsed_data/.

Environment:
    OCR_UAT: SimpleTex API token (required)
"""

import io
import os
import json
from pathlib import Path
import fitz
from PIL import Image
import requests
from tqdm import tqdm
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

UAT = os.getenv("OCR_UAT")


def pillow_image_to_file_binary(image):
    """Convert PIL image to binary data for API upload."""
    bytes_io = io.BytesIO()
    image.save(bytes_io, format='PNG')
    return bytes_io.getvalue()


def pdf_ocr(image):
    """Perform OCR on a single image using SimpleTex API."""
    api_url = "https://server.simpletex.cn/api/doc_ocr/"
    header = {"token": UAT}
    img_file = {"file": pillow_image_to_file_binary(image)}
    res = requests.post(api_url, files=img_file, data={}, headers=header).json()
    return res["res"]["content"]


def normalize_punctuation(content):
    """Replace Chinese punctuation with English equivalents."""
    replacements = {
        '，': ',', '。': '.', '、': ',', '；': ';', '：': ':',
        '？': '?', '！': '!', '"': '"', '"': '"', ''': "'",
        ''': "'", '（': '(', '）': ')', '【': '[', '】': ']',
        '《': '<', '》': '>', '．': '.',
    }
    for cn_char, en_char in replacements.items():
        content = content.replace(cn_char, en_char)
    return content


def extract_pdf(pdf_path, dpi=100):
    """
    Extract content from a single PDF file using OCR.

    Args:
        pdf_path: Path to PDF file
        dpi: DPI for image conversion (default 100)

    Returns:
        List of page contents
    """
    with open(pdf_path, 'rb') as f:
        pdf_binary = f.read()

    doc = fitz.open("pdf", pdf_binary)
    total_pages = doc.page_count

    pages_content = []

    for page_index in tqdm(range(total_pages), desc=f"Processing {pdf_path.name}"):
        try:
            # Convert page to image
            page = doc[page_index]
            pix = page.get_pixmap(dpi=dpi)
            image = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

            # OCR processing
            content = pdf_ocr(image)

            # Normalize punctuation
            content = normalize_punctuation(content)

            pages_content.append({
                "page_index": page_index,
                "content": content
            })

        except Exception as e:
            print(f"\nError processing page {page_index}: {str(e)}")
            pages_content.append({
                "page_index": page_index,
                "content": "",
                "error": str(e)
            })

    return pages_content


def extract_pdfs():
    """Extract content from all PDFs in the raw/ directory."""

    # Validate environment
    if not UAT:
        print("Error: OCR_UAT environment variable not set")
        print("Please add OCR_UAT to your .env file")
        print("Get your token from: https://simpletex.cn")
        return

    # Create output directory
    output_dir = Path("parsed_data")
    output_dir.mkdir(exist_ok=True)

    # Get all PDF files
    raw_dir = Path("raw")
    if not raw_dir.exists():
        print("Error: raw/ directory not found")
        return

    pdf_files = sorted(raw_dir.glob("*.pdf"))

    if not pdf_files:
        print("No PDF files found in raw/ directory")
        return

    print(f"Found {len(pdf_files)} PDF files to process")
    print("="*60)

    # Process each PDF
    results = {}

    for pdf_file in pdf_files:
        print(f"\nProcessing {pdf_file.name}...")

        try:
            # Extract content
            pages_content = extract_pdf(pdf_file)

            # Combine all pages into markdown
            markdown_content = "\n\n---\n\n".join([
                page["content"] for page in pages_content if page["content"]
            ])

            # Save as markdown
            output_file = output_dir / f"{pdf_file.stem}.md"
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(markdown_content)

            # Save as JSONL (with page info)
            jsonl_file = output_dir / f"{pdf_file.stem}.jsonl"
            with open(jsonl_file, "w", encoding="utf-8") as f:
                for page in pages_content:
                    f.write(json.dumps(page, ensure_ascii=False) + '\n')

            # Store metadata
            results[pdf_file.stem] = {
                "original_file": pdf_file.name,
                "parsed_file": str(output_file),
                "jsonl_file": str(jsonl_file),
                "status": "success",
                "total_pages": len(pages_content),
                "content_length": len(markdown_content)
            }

            print(f"✓ Successfully parsed {pdf_file.name}")
            print(f"  Pages: {len(pages_content)}")
            print(f"  Content length: {len(markdown_content)} characters")

        except Exception as e:
            print(f"✗ Error parsing {pdf_file.name}: {str(e)}")
            results[pdf_file.stem] = {
                "original_file": pdf_file.name,
                "status": "failed",
                "error": str(e)
            }

    # Save metadata
    metadata_file = output_dir / "extraction_metadata.json"
    with open(metadata_file, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    print(f"\n{'='*60}")
    print(f"Extraction complete!")
    print(f"Processed: {len(results)} files")
    print(f"Success: {sum(1 for r in results.values() if r['status'] == 'success')}")
    print(f"Failed: {sum(1 for r in results.values() if r['status'] == 'failed')}")
    print(f"Metadata saved to: {metadata_file}")

    return results


if __name__ == "__main__":
    extract_pdfs()
