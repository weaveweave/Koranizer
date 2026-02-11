# Koranizer: Automated Bank Statement Parser

**Koranizer** is a Python-based utility designed to streamline the process of extracting and transforming Indonesian bank statements (Rekening Koran) into structured Excel data.

---

## ## Features

* **Batch Processing**: Convert multiple PDF statements simultaneously.
* **Text Extraction**: High-speed extraction using `PyPDF2`.
* **Automated Parsing**: Uses Regular Expressions (Regex) to identify dates, transaction descriptions, and amounts.
* **Excel Export**: Organized output with account headers and clean transaction tables.

---

## ## Project Structure

```text
Koranizer/
├── src/
│   ├── pdftotxtLOOPER.py
│   └── txttoexcelLOOPER.py
├── folder_pdf_anda/    # Place source PDFs here
├── .gitignore
├── requirements.txt
└── README.md

```

---

## ## Prerequisites

Ensure your environment is ready before running the automation.

1. **Python Installation**: Download and install the latest version of Python from [python.org](https://www.python.org).
   **Windows users**: Ensure "Add Python to PATH" is checked during installation.
   **macOS users**: (optional) install newest version via (brew install python)
3. **Required Libraries**: Open your **Terminal** (macOS) or **Command Prompt** (Windows) and run:
```bash
pip install -r requirements.txt
```

3. **Directory Setup**:
   * Download as .zip
   * Extract zip in a dedicated project folder

---

## ## Operation Guide

### ### Phase 1: PDF to Text Extraction

This step converts raw PDF data into searchable text files.

* **Prepare Input**: Create a folder named `folder_pdf_anda` and place your PDF statements there.
* **Configuration**: Open `pdftotxtLOOPER.py` and verify the folder names in the `# --- KONFIGURASI ---` section.
* **Execution**:
* **Windows**: `python src/pdftotxtLOOPER.py`
* **macOS**: `python3 src/pdftotxtLOOPER.py`


* **Output**: Extracted `.txt` files will appear in `folder_hasil_teks`.

### ### Phase 2: Text to Excel Conversion

This step parses the text data into a structured financial spreadsheet.

* **Configure Paths**: Open `txttoexcelLOOPER.py` and update the `folder_sumber` and `folder_hasil` variables with the absolute paths of your directories.
* **Execution**:
* **Windows**: `python src/txttoexcelLOOPER.py`
* **macOS**: `python3 src/txttoexcelLOOPER.py`


* **Output**: Finalized `.xlsx` files will be generated in your designated output folder.

---
