from database import connect


class Proyek:
    def __init__(self, nama, deadline, status, perusahaan_id, client=None, nilai=None, id=None):
        self.id = id
        self.nama = nama
        self.deadline = deadline
        self.status = status
        self.perusahaan_id = perusahaan_id
        self.client = client
        self.nilai = nilai

    def simpan(self):
        conn = connect()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO proyek (nama, deadline, status, perusahaan_id, client, nilai)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (self.nama, self.deadline, self.status, self.perusahaan_id, self.client, self.nilai))
        self.id = cursor.lastrowid
        conn.commit()
        conn.close()


    @staticmethod
    def semua():
        conn = connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM proyek")
        data = cursor.fetchall()
        conn.close()
        return data

    @staticmethod
    def update_status(proyek_id, status_baru):
        conn = connect()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE proyek SET status=? WHERE id=?
        """, (status_baru, proyek_id))
        conn.commit()
        conn.close()

    @staticmethod
    def karyawan_untuk_proyek(proyek_id):
        conn = connect()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT k.id, k.nama FROM karyawan k
            JOIN karyawan_proyek kp ON k.id = kp.karyawan_id
            WHERE kp.proyek_id = ?
        """, (proyek_id,))
        hasil = cursor.fetchall()
        conn.close()
        return hasil
    
    @staticmethod
    def aktif_saja():
        conn = connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM proyek WHERE status = 'Aktif'")
        data = cursor.fetchall()
        conn.close()
        return data
    
    @staticmethod
    def hapus_karyawan_dari_proyek(proyek_id):
        conn = connect()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM karyawan_proyek WHERE proyek_id = ?", (proyek_id,))
        conn.commit()  # ⬅️ Penting agar DELETE benar-benar tersimpan
        conn.close()

    
    @staticmethod
    def update_nilai_deadline(proyek_id, deadline_baru, nilai_baru):
        conn = connect()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE proyek SET deadline = ?, nilai = ? WHERE id = ?
        """, (deadline_baru, nilai_baru, proyek_id))
        conn.commit()
        conn.close()




