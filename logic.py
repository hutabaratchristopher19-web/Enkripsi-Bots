# ==============================================
# ✅ SEMUA IMPORT DI ATAS
# ==============================================
import sqlite3

# ==============================================
# ✏️ KAMU ISI DAFTAR GANTI HURUF — KAYAK KAMUS
# ==============================================
ATURAN_GANTI = {
    "A": "X", "B": "Y", "C": "Z", "D": "P", "E": "Q",
    "F": "R", "G": "S", "H": "T", "I": "U", "J": "V",
    "K": "W", "L": "A", "M": "B", "N": "C", "O": "D",
    "P": "E", "Q": "F", "R": "G", "S": "H", "T": "I",
    "U": "J", "V": "K", "W": "L", "X": "M", "Y": "N",
    "Z": "O"
}

KUNCI_RAHASIA = "ganti_kata_rahasia_kamu"  # ✏️ Ganti kata rahasia kamu

# ==============================================
# 1. PANGKALAN DATA — SIMPAN SEMUA KATA
# ==============================================
def siapkan_database():
    """Buat tempat simpan kalau belum ada"""
    conn = sqlite3.connect("catatan.db")
    c = conn.cursor()
    
    c.execute("""
        CREATE TABLE IF NOT EXISTS riwayat (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            kata_asal TEXT NOT NULL,
            setelah_ganti TEXT,
            setelah_enkripsi TEXT,
            waktu TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    conn.commit()
    conn.close()

def simpan_ke_db(kata_asal, setelah_ganti, setelah_enkripsi):
    """Simpan 1 kata ke catatan"""
    conn = sqlite3.connect("catatan.db")
    c = conn.cursor()
    
    c.execute("""
        INSERT INTO riwayat (kata_asal, setelah_ganti, setelah_enkripsi)
        VALUES (?, ?, ?)
    """, (kata_asal, setelah_ganti, setelah_enkripsi))
    
    conn.commit()
    conn.close()

# ==============================================
# 2. GANTI HURUF — TERJEMAHKAN KATA
# ==============================================
def ganti_huruf(kata):
    """Ubah huruf per huruf sesuai daftar, spasi/tanda dibiarkan"""
    kata = kata.upper()
    hasil = ""
    
    for huruf in kata:
        if huruf in ATURAN_GANTI:
            hasil += ATURAN_GANTI[huruf]  # Ganti sesuai kamus
        else:
            hasil += huruf  # Kalau tidak ada di daftar, biarkan apa adanya
    
    return hasil

# ==============================================
# 3. ENKRIPSI — KUNCI RAHASIA
# ==============================================
def enkripsi(teks, kunci):
    """Acak hasil ganti huruf pakai kunci rahasia"""
    hasil = ""
    
    for i, huruf in enumerate(teks):
        geser = ord(kunci[i % len(kunci)]) % 128
        huruf_baru = chr((ord(huruf) + geser) % 65536)
        hasil += huruf_baru
    
    return hasil

# ==============================================
# 4. PROSES PESAN — KAYAK PENERJEMAH
# ==============================================
def proses_pesan(isi_pesan):
    """
    Contoh masuk: !bola tas lampu
    Keluar:
    bola → jadi apa → dienkripsi jadi apa
    tas  → jadi apa → dienkripsi jadi apa
    lampu→ jadi apa → dienkripsi jadi apa
    """
    
    siapkan_database()
    
    # Cek awalan harus pakai !
    if not isi_pesan.startswith("!"):
        return "⚠️ Awali dengan !\nContoh: !bola\nAtau: !bola tas lampu"
    
    # Ambil semua kata setelah ! → dipisah jadi daftar
    daftar_kata = isi_pesan[1:].strip().split()
    
    if not daftar_kata:
        return "⚠️ Tulis kata setelah !\nContoh: !bola"
    
    # Siapkan jawaban
    jawaban = f"📖 Hasil Terjemahan ({len(daftar_kata)} kata):\n"
    jawaban += "─" * 45 + "\n"
    
    # Proses SATU PER SATU kayak kamus
    for nomor, kata in enumerate(daftar_kata, 1):
        # Langkah 1: ganti huruf
        hasil_ganti = ganti_huruf(kata)
        
        # Langkah 2: enkripsi hasil ganti huruf
        hasil_enkripsi = enkripsi(hasil_ganti, KUNCI_RAHASIA)
        
        # Simpan ke pangkalan data
        simpan_ke_db(kata, hasil_ganti, hasil_enkripsi)
        
        # Tampilkan hasil kayak penerjemah
        jawaban += f"{nomor}. 「 {kata} 」\n"
        jawaban += f"    ↳ Ganti huruf: {hasil_ganti}\n"
        jawaban += f"    ↳ Dienkripsi: {hasil_enkripsi}\n\n"
    
    jawaban += "📝 Semua sudah disimpan ke catatan!"
    return jawaban

if __name__ == "__main__":
    # Contoh penggunaan
    contoh_pesan = "!bola senin matematika"
    hasil = proses_pesan(contoh_pesan)
    print(hasil)
