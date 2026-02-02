#  Retail Sales ETL Engine: PDF to Structured Insights

This project provides a robust solution for a common challenge in the retail industry: extracting and transforming data from **unstructured PDF reports** into a clean, relational database ready for Business Intelligence (BI).



##  The Challenge
Legacy retail management systems often generate sales reports exclusively in PDF format, which prevents granular data analysis. The key technical hurdles addressed here were:

1.  **String Sanitization:** Removing "noise" such as phone numbers, dates, and formatting artifacts from client names using advanced pattern matching.
2.  **Heuristic Categorization:** Mapping over 11,000 units into product Families and Sub-groups (e.g., Topwear, Bottomwear, Intimates) based solely on inconsistent text descriptions.
3.  **Attribute Normalization:** Standardizing color variations and fixing common typos (e.g., mapping "BRANCA" to "WHITE" or correcting "CARAMELHO" to "CARAMELO") to ensure SKU integrity.

##  Technical Stack
* **Python:** The core language for high-speed data processing.
* **PDFPlumber:** Used for high-precision text extraction from complex PDF layouts.
* **Pandas:** Orchestrates data cleaning, transformation, and exporting to CSV.
* **Regex (Regular Expressions):** The logic engine used for deep text parsing and sanitization.

##  Key Technical Features
* **Regex Sanitization:** Implemented specialized patterns to decouple client identity from report metadata.
* **Layered Logic Categorization:** Developed a priority-based hierarchy to prevent misclassification (e.g., identifying "Dresses" before "Blouses" to avoid substring errors).
* **Word Boundary Protection:** Utilized `\b` Regex tokens to ensure terms like "ALÇA" (Strap) are not confused with "CALÇA" (Pants).
* **Multi-Level Mapping:** Exhaustive search for colors and materials within descriptions to enrich inventory and sales mix analysis.

##  Business Impact
* **95% Automation:** Reduced data preparation time from hours of manual entry to a few seconds.
* **Data Reliability:** Eliminated human error in product categorization.
* **Prescriptive Power:** This script serves as the **Data Engine** for the **Ophyum Modas Performance Dashboard**, enabling retention metrics and product performance tracking.



##  Installation & Usage
1.  **Install dependencies:**
    ```bash
    pip install pdfplumber pandas openpyxl
    ```
2.  **Prepare your file:** Place your `vendas.pdf` file in the project root.
3.  **Run the script:**
    ```bash
    python Etl-Ophyum.py
    ```
4.  **Output:** The script generates `base_vendas_limpa.csv`, ready for consumption in **Looker Studio**, **Power BI**, or **Tableau**.

---
**Live Project:** [View Ophyum Modas Dashboard](https://lookerstudio.google.com/u/0/reporting/d19b9fa2-7e77-42c3-a9c7-2c59cee2fc7e/page/uhojF)

*Developed by Israel Buratto - Analytics & Business Intelligence*
