import os
from PyPDF2 import PdfMerger

# 🔧 Folder containing your PDF files
input_folder = r"D:\BTP-NeerajGoyal\scraping_data\kgp-docs"  # change this to your path
output_file = "merged_kgpdocs.pdf"

# Initialize PDF merger
merger = PdfMerger()

# Sort the files alphabetically (optional but neat)
pdf_files = sorted(
    [f for f in os.listdir(input_folder) if f.lower().endswith(".pdf")]
)

if not pdf_files:
    print("⚠️ No PDF files found in the folder!")
else:
    for filename in pdf_files:
        filepath = os.path.join(input_folder, filename)
        try:
            merger.append(filepath)
            print(f"📄 Added: {filename}")
        except Exception as e:
            print(f"❌ Error adding {filename}: {e}")

    # Write merged file
    merger.write(output_file)
    merger.close()

    print(f"\n✅ All PDFs merged into '{output_file}' successfully.")
