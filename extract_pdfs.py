import os
import json
from pathlib import Path
from llama_parse import LlamaParse
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def extract_pdfs():
    """Extract content from all PDFs in the raw/ directory using llama-parse."""

    # Initialize LlamaParse
    parser = LlamaParse(
        api_key=os.getenv("LLAMA_CLOUD_API_KEY"),
        result_type="markdown",  # Get markdown output
        verbose=True
    )

    # Create output directory
    output_dir = Path("parsed_data")
    output_dir.mkdir(exist_ok=True)

    # Get all PDF files
    raw_dir = Path("raw")
    pdf_files = sorted(raw_dir.glob("*.pdf"))

    print(f"Found {len(pdf_files)} PDF files to process")

    # Process each PDF
    results = {}
    for pdf_file in pdf_files:
        print(f"\nProcessing {pdf_file.name}...")
        try:
            # Parse the PDF
            documents = parser.load_data(str(pdf_file))

            # Extract text content
            content = "\n\n".join([doc.text for doc in documents])

            # Save the parsed content
            output_file = output_dir / f"{pdf_file.stem}.md"
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(content)

            # Store metadata
            results[pdf_file.stem] = {
                "original_file": pdf_file.name,
                "parsed_file": str(output_file),
                "status": "success",
                "content_length": len(content)
            }

            print(f"✓ Successfully parsed {pdf_file.name}")
            print(f"  Content length: {len(content)} characters")

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

    print(f"\n{'='*50}")
    print(f"Extraction complete!")
    print(f"Processed: {len(results)} files")
    print(f"Success: {sum(1 for r in results.values() if r['status'] == 'success')}")
    print(f"Failed: {sum(1 for r in results.values() if r['status'] == 'failed')}")
    print(f"Metadata saved to: {metadata_file}")

    return results

if __name__ == "__main__":
    extract_pdfs()
