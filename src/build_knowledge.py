from pypdf import PdfReader
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent

pdf_path = project_root / "documents" / "Apple_2025_Annual_Report.pdf"

reader = PdfReader(str(pdf_path))

print(f"Loaded {len(reader.pages)} pages")

full_text = ""

for page in reader.pages:
    text = page.extract_text()

    if text:
        full_text += text + "\n"

print("Characters extracted:", len(full_text))

output_file = project_root / "documents" / "apple_report.txt"

with open(output_file, "w", encoding="utf-8") as f:
    f.write(full_text)

print("Knowledge base saved!")