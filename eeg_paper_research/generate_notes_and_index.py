import fitz
import os
import re
import csv
import pandas as pd

# Let's inspect the text from each PDF to extract precise details
def get_pdf_text_sample(pdf_path, max_pages=15):
    doc = fitz.open(pdf_path)
    text = ""
    for i in range(min(len(doc), max_pages)):
        text += f"\n--- Page {i+1} ---\n" + doc[i].get_text()
    return text

print("Extracting full text and generating notes...")
