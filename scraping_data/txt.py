import os
from PyPDF2 import PdfReader

# 🔧 Path to your merged PDF file
input_pdf = r"D:\BTP-NeerajGoyal\scraping_data\merged_kgpdocs.pdf"  # change this path
output_txt = "merged_output.txt"

# Open and read PDF
reader = PdfReader(input_pdf)

with open(output_txt, "w", encoding="utf-8") as txt_file:
    for page_num, page in enumerate(reader.pages, start=1):
        text = page.extract_text()
        if text:
            txt_file.write(f"--- Page {page_num} ---\n")
            txt_file.write(text)
            txt_file.write("\n\n")
        else:
            txt_file.write(f"--- Page {page_num}: (No extractable text) ---\n\n")

print(f"✅ Text extracted from '{input_pdf}' and saved to '{output_txt}'.")
