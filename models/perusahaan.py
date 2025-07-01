from database import connect
from .karyawan import Karyawan

class Perusahaan:
    def __init__(self, nama, alamat, email, logo=None, id=None):
        self.id = id
        self.nama = nama
        self.alamat = alamat
        self.email = email
        self.logo = logo

    def simpan(self):
        conn = connect()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO perusahaan (nama, alamat, email, logo) VALUES (?, ?, ?, ?)",
            (self.nama, self.alamat, self.email, self.logo)
        )
        conn.commit()
        conn.close()

    def update(self):
        conn = connect()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE perusahaan SET nama=?, alamat=?, email=?, logo=? WHERE id=?",
            (self.nama, self.alamat, self.email, self.logo, self.id)
        )
        conn.commit()
        conn.close()

    @staticmethod
    def get_profil():
        conn = connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM perusahaan LIMIT 1")
        row = cursor.fetchone()
        conn.close()
        if row:
            return Perusahaan(row[1], row[2], row[3], row[4], row[0])
        return None

    def jumlah_karyawan(self):
        conn = connect()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM karyawan WHERE perusahaan_id=?", (self.id,))
        jumlah = cursor.fetchone()[0]
        conn.close()
        return jumlah
    
    # Tambah karyawan
    def tambah_karyawan(self, nama, usia, gaji, divisi):
        karyawan = Karyawan(nama, usia, gaji, divisi, self.id)
        karyawan.simpan()

    # Update gaji dan divisi karyawan
    def update_karyawan(self, karyawan_id, gaji_baru, divisi_baru):
        Karyawan.update(karyawan_id, gaji_baru, divisi_baru)

    # Hapus karyawan
    def hapus_karyawan(self, karyawan_id):
        Karyawan.hapus(karyawan_id)
