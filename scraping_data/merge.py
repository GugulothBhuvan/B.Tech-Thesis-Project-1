# -*- coding: utf-8 -*-
import os
import json

# Use raw string or forward slashes
input_folder = r"D:\BTP-NeerajGoyal\scraping_data\kgp-docs"
output_file = "merged_kgpdocs.txt"

with open(output_file, "w", encoding="utf-8") as outfile:
    for filename in os.listdir(input_folder):
        if filename.endswith(".json"):
            filepath = os.path.join(input_folder, filename)
            try:
                with open(filepath, "r", encoding="utf-8") as infile:
                    data = json.load(infile)
                    outfile.write(f"--- {filename} ---\n")
                    outfile.write(json.dumps(data, indent=2, ensure_ascii=False))
                    outfile.write("\n\n")
            except Exception as e:
                print(f"Error reading {filename}: {e}")

# Safe print for Windows consoles
try:
    print(f"\u2705 All JSON files merged into '{output_file}' successfully.")
except UnicodeEncodeError:
    print(f"[OK] All JSON files merged into '{output_file}' successfully.")
