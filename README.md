# Retail Sales ETL Engine: PDF to Structured Insights

*(https://lookerstudio.google.com/u/0/reporting/d19b9fa2-7e77-42c3-a9c7-2c59cee2fc7e/page/uhojF)*

<img width="100%" alt="Retail ETL Dashboard" src="https://github.com/user-attachments/assets/545b1fc9-eeb2-41c0-ae6e-4bc3c25d92da" />

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Pandas](https://img.shields.io/badge/Pandas-Data_Processing-150458?style=flat&logo=pandas&logoColor=white)](https://pandas.pydata.org/)
[![Regex](https://img.shields.io/badge/Regex-Pattern_Matching-4285F4?style=flat&logo=google-cloud&logoColor=white)](https://docs.python.org/3/library/re.html)
[![Looker Studio](https://img.shields.io/badge/Looker_Studio-BI-4285F4?style=flat&logo=looker&logoColor=white)](https://lookerstudio.google.com/)

## Introduction

This project provides a robust solution for a common challenge in the retail industry: extracting and transforming data from **unstructured PDF reports** into a clean, relational database. 

Legacy ERP systems often generate sales data exclusively in PDF format, which prevents granular analysis. This ETL (Extract, Transform, Load) engine automates the parsing of thousands of lines, using advanced **Regular Expressions (Regex)** and heuristic categorization to build a structured pipeline for Business Intelligence.

## Features

* **High-Precision Extraction:** Utilizes `PDFPlumber` to navigate complex report layouts and extract raw text without losing data integrity.
* **Regex Sanitization:** Advanced pattern matching to decouple client identities from metadata and formatting artifacts.
* **Heuristic Categorization:** A layered logic engine that maps over 11,000 units into product Families and Sub-groups (e.g., Topwear, Bottomwear) based on inconsistent descriptions.
* **Attribute Normalization:** Automated standardization of color variations and typo correction (e.g., "CARAMELHO" to "CARAMELO") using word boundary protection.

## Installation

Clone the repository and install the dependencies for PDF processing:

```bash
git clone [https://github.com/bttisrael/retail-etl-engine.git](https://github.com/bttisrael/retail-etl-engine.git)
cd retail-etl-engine
pip install pdfplumber pandas openpyxl
```
## Usage & Sample Code
Place your vendas.pdf in the root folder and run the script. Below is a snippet of the Regex Engine developed to sanitize descriptions and categorize products:

```Python
import re
import pandas as pd

# Word Boundary Protection to avoid substring errors (e.g., ALÇA vs CALÇA)
def categorize_product(description):
    if re.search(r'\b(CALCA|BERMUDA|SHORT)\b', description):
        return 'Bottomwear'
    elif re.search(r'\b(VESTIDO|MACACAO)\b', description):
        return 'One-piece'
    elif re.search(r'\b(BLUSA|REGATA|T-SHIRT)\b', description):
        return 'Topwear'
    return 'Accessories'


# Cleaning formatting noise from descriptions
df['clean_description'] = df['raw_text'].apply(lambda x: re.sub(r'\d{2}/\d{2}/\d{4}|TEL:.*', '', x))
```
## Experiments and Diagnostics
The development of this ETL engine addressed several technical hurdles:

* **95% Automation**: Reduced data preparation time from hours of manual entry to a few seconds.

* **Category Accuracy**: Implementation of Layered Logic (identifying "Dresses" before "Blouses") prevented classification errors common in substring matching.

* **Business Insights**: This script serves as the primary data engine for the Ophyum Modas Performance Dashboard, enabling SKU-level tracking and customer retention metrics.

## Reference
[1] McKinney, W. (2012). Python for Data Analysis: Data Wrangling with Pandas, NumPy, and IPython.
