from database import connect

class Karyawan:
    def __init__(self, nama, usia, gaji, divisi, perusahaan_id, id=None):
        self.id = id
        self.nama = nama
        self.usia = usia
        self.gaji = gaji
        self.divisi = divisi
        self.perusahaan_id = perusahaan_id

    def simpan(self):
        conn = connect()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO karyawan (nama, usia, gaji, divisi, perusahaan_id)
            VALUES (?, ?, ?, ?, ?)
        """, (self.nama, self.usia, self.gaji, self.divisi, self.perusahaan_id))
        conn.commit()
        conn.close()

    def mengerjakan_proyek(self, proyek_id):
        conn = connect()
        cursor = conn.cursor()

        # Cek apakah sudah ada relasi
        cursor.execute("""
            SELECT 1 FROM karyawan_proyek 
            WHERE karyawan_id = ? AND proyek_id = ?
        """, (self.id, proyek_id))
        sudah_ada = cursor.fetchone()

        if not sudah_ada:
            cursor.execute("""
                INSERT INTO karyawan_proyek (karyawan_id, proyek_id)
                VALUES (?, ?)
            """, (self.id, proyek_id))
            conn.commit()

        conn.close()


    def sedang_mengerjakan(self):
        conn = connect()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT COUNT(*)
            FROM karyawan_proyek kp
            JOIN proyek p ON kp.proyek_id = p.id
            WHERE kp.karyawan_id = ? AND p.status = 'Aktif'
        """, (self.id,))
        hasil = cursor.fetchone()[0]
        conn.close()
        return hasil > 0



    @staticmethod
    def semua():
        conn = connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM karyawan")
        data = cursor.fetchall()
        conn.close()
        return data

    @staticmethod
    def update(karyawan_id, nama_baru, usia_baru, gaji_baru, divisi_baru):
        conn = connect()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE karyawan SET nama=?, usia=?, gaji=?, divisi=? WHERE id=?",
            (nama_baru, usia_baru, gaji_baru, divisi_baru, karyawan_id)
        )
        conn.commit()
        conn.close()

    @staticmethod
    def dari_db(karyawan_id):
        conn = connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM karyawan WHERE id=?", (karyawan_id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return Karyawan(row[1], row[2], row[3], row[4], row[5], row[0])
        return None


    @staticmethod
    def hapus(karyawan_id):
        conn = connect()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM karyawan WHERE id=?", (karyawan_id,))
        conn.commit()
        conn.close()
