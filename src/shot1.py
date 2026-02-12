import PyPDF2

def extract_text_from_pdf(pdf_path):
    """
    Extracts text from a text-based PDF file.

    Args:
        pdf_path (str): Path to the PDF file.

    Returns:
        str: Extracted text from the PDF.
    """
    extracted_text = []

    try:
        with open(pdf_path, 'rb') as pdf_file:
            reader = PyPDF2.PdfReader(pdf_file)

            for page_num in range(len(reader.pages)):
                page = reader.pages[page_num]
                text = page.extract_text()
                if text:  # Only append non-empty text
                    extracted_text.append(f"--- Page {page_num + 1} ---\n{text}\n")

        return "\n".join(extracted_text)

    except FileNotFoundError:
        print(f"Error: File '{pdf_path}' not found.")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

# Example usage
if __name__ == "__main__":
    pdf_file = "new1-20.pdf"  # Replace with your PDF file path
    text = extract_text_from_pdf(pdf_file)

    if text:
        print("Extracted Text:")
        print(text)
        # Optionally, save to a .txt file
        with open("extracted_textNeo.txt", "w", encoding="utf-8") as txt_file:
            txt_file.write(text)
        print("\nText saved to 'extracted_text.txt'.")
