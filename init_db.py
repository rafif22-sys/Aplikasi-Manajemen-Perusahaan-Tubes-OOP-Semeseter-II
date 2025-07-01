import sqlite3

conn = sqlite3.connect('perusahaan.db')
cursor = conn.cursor()

# Tabel Perusahaan
cursor.execute("""
CREATE TABLE IF NOT EXISTS perusahaan (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nama TEXT NOT NULL,
    alamat TEXT,
    email TEXT,
    logo TEXT          
)
""")

# Tabel Karyawan
cursor.execute("""
CREATE TABLE IF NOT EXISTS karyawan (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nama TEXT NOT NULL,
    usia INTEGER NOT NULL CHECK(usia > 17),
    gaji INTEGER NOT NULL CHECK(gaji > 0),
    divisi TEXT,
    perusahaan_id INTEGER,
    FOREIGN KEY (perusahaan_id) REFERENCES perusahaan(id)
)
""")

# Tabel Proyek
cursor.execute("""
CREATE TABLE IF NOT EXISTS proyek (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nama TEXT NOT NULL,
    deadline TEXT,
    status TEXT,
    perusahaan_id INTEGER,
    FOREIGN KEY (perusahaan_id) REFERENCES perusahaan(id)
)
""")


# Abaikan error jika sudah ada kolom logo

# Tambah kolom baru ke tabel proyek
try:
    cursor.execute("ALTER TABLE proyek ADD COLUMN client TEXT NOT NULL")
except sqlite3.OperationalError:
    pass

try:
    cursor.execute("ALTER TABLE proyek ADD COLUMN nilai INTEGER NOT NULL CHECK(nilai > 0)")
except sqlite3.OperationalError:
    pass

# Relasi antara karyawan dan proyek (Many-to-Many)
cursor.execute("""
    CREATE TABLE IF NOT EXISTS karyawan_proyek (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        karyawan_id INTEGER,
        proyek_id INTEGER,
        FOREIGN KEY(karyawan_id) REFERENCES karyawan(id),
        FOREIGN KEY(proyek_id) REFERENCES proyek(id)
    )
""")


conn.commit()
conn.close()
