import pandas as pd
import re
import os

def extract_transaction_data(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
        lines = [line.strip() for line in content.split('\n') if line.strip()]

    # 1. Ekstraksi Informasi Header (Nama & No Rekening)
    acc_no_match = re.search(r'Account No\s+:\s+(\d+)', content)
    account_no = acc_no_match.group(1) if acc_no_match else "NOMOR_REKENING" # Sesuai sumber [1]
    
    # Nama pemilik biasanya muncul sebelum "Periode Transaksi"
    name_match = re.search(r'Statement Date\s+:\s+\d{2}/\d{2}/\d{2}\s+(.*?)\s+Periode Transaksi', content, re.DOTALL)
    owner_name = name_match.group(1).strip() if name_match else "NAMA_PEMILIK" # Sesuai sumber [5]

    # 2. Pola Regex
    date_pattern = r'^\d{2}/\d{2}/\d{2} \d{2}:\d{2}:\d{2}$' # Format Tanggal & Jam [1, 2]
    teller_pattern = r'^(\d{7}|[A-Za-z0-9]{6}|[A-Za-z]{8})$' # 7 digit angka spt 0852036 [1]
    money_pattern = r'^-?[\d,]+\.\d{2}$' # Format XXX,XXX.XX [1, 3]
    special_keywords = ['interest account', 'tax', 'monthly fee atm']

    transactions = []
    i = 0
    while i < len(lines):
        if re.match(date_pattern, lines[i]):
            tanggal = lines[i]
            desc_parts = []
            j = i + 1
            
            # Deteksi Transaksi Khusus
            is_special = False
            temp_j = j
            while temp_j < len(lines) and not re.match(money_pattern, lines[temp_j]) and not re.match(teller_pattern, lines[temp_j]):
                if any(keyword in lines[temp_j].lower() for keyword in special_keywords):
                    is_special = True
                temp_j += 1

            if is_special:
                while j < len(lines) and not re.match(money_pattern, lines[j]):
                    desc_parts.append(lines[j])
                    j += 1
                teller_id = "" 
            else:
                while j < len(lines) and not re.match(teller_pattern, lines[j]) and not re.match(money_pattern, lines[j]):
                    desc_parts.append(lines[j])
                    j += 1
                
                if j < len(lines) and re.match(teller_pattern, lines[j]):
                    teller_id = lines[j]
                    j += 1
                else:
                    teller_id = ""

            try:
                if j + 2 < len(lines):
                    debet, kredit, saldo = lines[j], lines[j+1], lines[j+2]
                    if all(re.match(money_pattern, m) for m in [debet, kredit, saldo]):
                        transactions.append({
                            "Tanggal Transaksi": tanggal,
                            "Uraian Transaksi": " ".join(desc_parts),
                            "Teller/User ID": teller_id,
                            "Debet": debet,
                            "Kredit": kredit,
                            "Saldo": saldo
                        })
                        i = j + 3
                        continue
            except IndexError:
                break
        i += 1
    
    return owner_name, account_no, transactions

def batch_process_txt_to_excel(input_folder, output_folder):
    # Buat folder output jika belum ada
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Loop semua file .txt di folder input
    for filename in os.listdir(input_folder):
        if filename.endswith(".txt"):
            file_path = os.path.join(input_folder, filename)
            print(f"Memproses: {filename}...")
            
            owner, acc_no, data = extract_transaction_data(file_path)
            
            if data:
                df = pd.DataFrame(data)
                # Nama file output mengikuti nama file input (txt ke xlsx)
                output_filename = filename.replace(".txt", ".xlsx")
                output_path = os.path.join(output_folder, output_filename)
                
                with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
                    pd.DataFrame([["Nama:", owner], ["No Rek:", acc_no], ["", ""]]).to_excel(writer, index=False, header=False, startrow=0)
                    df.to_excel(writer, index=False, startrow=4)
                print(f"Selesai! Disimpan ke: {output_path}")
            else:
                print(f"Peringatan: Tidak ada data transaksi ditemukan di {filename}")

# --- KONFIGURASI FOLDER ---
folder_sumber = './folder_txt'   # Ganti dengan path folder berisi file .txt
folder_hasil  = './folder_excel' # Ganti dengan path folder tujuan Excel

# Jalankan proses
batch_process_txt_to_excel(folder_sumber, folder_hasil)