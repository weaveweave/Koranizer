import PyPDF2
import os

def extract_text_from_pdf(pdf_path):
    """Fungsi ekstraksi teks dari sumber [1]"""
    extracted_text = []
    try:
        with open(pdf_path, 'rb') as pdf_file:
            reader = PyPDF2.PdfReader(pdf_file) # [1]
            for page_num in range(len(reader.pages)):
                page = reader.pages[page_num]
                text = page.extract_text() # [1]
                if text: 
                    extracted_text.append(f"--- Page {page_num + 1} ---\n{text}\n") # [1]
            return "\n".join(extracted_text)
    except FileNotFoundError: # [2]
        print(f"Error: File '{pdf_path}' tidak ditemukan.")
        return None
    except Exception as e: # [2]
        print(f"Terjadi kesalahan pada {pdf_path}: {e}")
        return None

def batch_pdf_to_txt(input_folder, output_folder):
    # Buat folder output jika belum ada
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Looping semua file di folder input
    for filename in os.listdir(input_folder):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(input_folder, filename)
            print(f"Mengekstrak: {filename}...")
            
            text = extract_text_from_pdf(pdf_path)
            
            if text:
                # Tentukan nama file .txt (mengganti .pdf menjadi .txt)
                txt_filename = filename.replace(".pdf", ".txt")
                output_path = os.path.join(output_folder, txt_filename)
                
                # Simpan hasil ekstraksi ke file .txt [2, 3]
                with open(output_path, "w", encoding="utf-8") as txt_file:
                    txt_file.write(text)
                print(f"Berhasil disimpan ke: {output_path}")

# --- KONFIGURASI ---
folder_pdf_sumber = 'folder_pdf_anda'    # Ganti dengan folder isi PDF
folder_txt_hasil  = 'folder_hasil_teks' # Ganti dengan folder tujuan TXT

# Jalankan proses
batch_pdf_to_txt(folder_pdf_sumber, folder_txt_hasil)