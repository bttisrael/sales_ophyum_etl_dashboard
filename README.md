📊 Retail Sales ETL Engine: PDF to Structured Insights
This project automates the extraction and transformation of sales data from unstructured PDF reports into a clean, relational, and categorized database ready for Business Intelligence (BI) and executive dashboards.

🎯 The Challenge
Most legacy retail systems generate reports in PDF format, which creates a significant barrier to historical and granular data analysis. The key challenges addressed here were:

String Sanitization: Removing "noise" (phone numbers, formatting artifacts, dates) from client names using advanced pattern matching.

Heuristic Categorization: Mapping over 11,000 sold units into Families and Sub-groups (e.g., Topwear, Bottomwear) based solely on inconsistent text descriptions.

Color Normalization: Standardizing spelling variations and typos (e.g., mapping "BRANCA" to "WHITE" or fixing common typos like "CARAMELHO") to ensure SKU integrity.

🛠️ Technical Stack
Python: The core language for data processing.

PDFPlumber: High-precision text extraction from PDF documents.

Pandas: Data manipulation, cleaning, and exporting to CSV/SQL.

Regex (Regular Expressions): The logic engine used for complex text parsing and data sanitization.

⚙️ Key Technical Features
Regex Sanitization: Implemented specialized patterns to decouple client identity from report metadata.

Layered Logic Categorization: Developed a priority-based hierarchy (e.g., identifying "Dresses" before "Blouses" to prevent substring misclassification).

Word Boundary Protection: Utilized \b Regex tokens to ensure terms like "ALÇA" (Strap) were not confused with "CALÇA" (Pants).

Attribute Mapping: Exhaustive search for color and material attributes within descriptions to enrich SKU-level inventory analysis.

📊 Business Impact
95% Automation: Reduced data preparation time from hours of manual entry to seconds.

Data Reliability: Eliminated human error in product counting and categorization.

Prescriptive Power: This script serves as the "data engine" for the Ophyum Modas performance dashboard, enabling retention metrics and product mix optimization.

📂 Installation & Usage
Install dependencies:

Bash
pip install pdfplumber pandas openpyxl
Place your vendas.pdf file in the project root.

Run the script:

Bash
python sales_etl.py
The base_vendas_limpa.csv will be generated, ready for consumption in tools like Looker Studio, Power BI, or Tableau.

Live Client Dashboard: View Live Dashboard
