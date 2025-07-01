import streamlit as st
import os
from models.perusahaan import Perusahaan
from models.karyawan import Karyawan
from models.proyek import Proyek
from datetime import datetime
import pandas as pd
from streamlit.components.v1 import html

st.set_page_config(page_title="Manajemen Perusahaan", layout="wide")
st.title("📊 Aplikasi Manajemen Perusahaan Berbasis OOP")

# Sidebar Navigasi
st.sidebar.title("📁 Navigasi Menu")
menu = st.sidebar.radio(
    "Pilih halaman:",
    ["Profil Perusahaan", "Manajemen Karyawan", "Daftar Proyek","Riwayat Proyek", "Lihat Semua Data"]
)

# PROFIL PERUSAHAAN
if menu == "Profil Perusahaan":
    st.markdown("""
        <style>
            .profil-card {
                background-color: #f9f9f9;
                padding: 25px;
                border-radius: 10px;
                box-shadow: 0 4px 8px rgba(0,0,0,0.05);
                margin-bottom: 20px;
            }
            .profil-header {
                font-size: 24px;
                font-weight: 600;
                color: #333333;
                margin-bottom: 10px;
            }
            .profil-label {
                font-weight: 500;
                color: #444444;
            }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("## 🏢 Profil Perusahaan")

    profil = Perusahaan.get_profil()

    if profil is None:
        st.info("Silakan isi profil perusahaan terlebih dahulu.")

        with st.form("form_profil_perusahaan"):
            nama = st.text_input("📛 Nama Perusahaan")
            alamat = st.text_area("📍 Alamat Perusahaan")
            email = st.text_input("📧 Email Perusahaan")
            logo_file = st.file_uploader("🖼️ Upload Logo Perusahaan", type=["png", "jpg", "jpeg"])
            submitted = st.form_submit_button("💾 Simpan Profil")

            if submitted:
                if not nama.strip():
                    st.error("❌ Nama perusahaan tidak boleh kosong.")
                else:
                    logo_path = ""
                    if logo_file:
                        logo_path = f"logo_{nama}.png"
                        with open(logo_path, "wb") as f:
                            f.write(logo_file.read())
                    p = Perusahaan(nama, alamat, email, logo_path)
                    p.simpan()
                    st.success("✅ Profil perusahaan berhasil disimpan!")
                    st.rerun()

    else:
        with st.container():
            st.markdown("""
                <style>
                    .profil-box {
                        background-color: #fdfdfd;
                        padding: 20px;
                        border-radius: 10px;
                        box-shadow: 0 2px 6px rgba(0,0,0,0.1);
                        margin-bottom: 20px;
                    }
                    .profil-title {
                        font-size: 26px;
                        font-weight: bold;
                        color: #222;
                        margin-bottom: 10px;
                    }
                    .profil-item {
                        background-color: #f4f4f4;
                        padding: 10px 15px;
                        border-radius: 8px;
                        margin-bottom: 10px;
                        font-size: 15px;
                    }
                    .profil-item span {
                        font-weight: 500;
                        color: #444;
                    }
                </style>
            """, unsafe_allow_html=True)

            st.markdown("<div class='profil-box'>", unsafe_allow_html=True)

            col1, col2 = st.columns([3, 1])

            with col1:
                st.markdown(f"<div class='profil-title'>{profil.nama}</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='profil-item'><span>📧 Email:</span><br>{profil.email}</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='profil-item'><span>📍 Alamat:</span><br>{profil.alamat}</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='profil-item'><span>👨‍💼 Jumlah Karyawan:</span><br>{profil.jumlah_karyawan()}</div>", unsafe_allow_html=True)

            with col2:
                st.markdown(
                    """
                    <div style='
                        display: flex;
                        flex-direction: column;
                        justify-content: center;
                        align-items: center;
                        height: 100%;
                        min-height: 105px;
                    '>
                    """,
                    unsafe_allow_html=True
                )
                if profil.logo and os.path.exists(profil.logo):
                    st.image(profil.logo, width=150)
                else:
                    st.markdown("📷 Belum ada logo")
                st.markdown("</div>", unsafe_allow_html=True)



        with st.expander("✏️ Edit Profil"):
            nama = st.text_input("📛 Nama Perusahaan", profil.nama)
            email = st.text_input("📧 Email", profil.email)
            alamat = st.text_area("📍 Alamat", profil.alamat)
            logo_file = st.file_uploader("🖼️ Ganti Logo", type=["png", "jpg", "jpeg"])
            if st.button("💾 Update"):
                if not nama.strip():
                    st.error("❌ Nama perusahaan tidak boleh kosong.")
                else:
                    if logo_file:
                        logo_path = f"logo_{nama}.png"
                        with open(logo_path, "wb") as f:
                            f.write(logo_file.read())
                    else:
                        logo_path = profil.logo
                    profil.nama = nama
                    profil.email = email
                    profil.alamat = alamat
                    profil.logo = logo_path
                    profil.update()
                    st.success("✅ Profil berhasil diperbarui!")
                    st.rerun()



# MANAJEMEN KARYAWAN
elif menu == "Manajemen Karyawan":
    st.header("👩‍💼 Manajemen Karyawan")
    profil = Perusahaan.get_profil()

    if not profil:
        st.warning("Harap isi data perusahaan terlebih dahulu.")
    else:
        if "reset_karyawan_form" not in st.session_state:
            st.session_state.reset_karyawan_form = False

        if st.session_state.reset_karyawan_form:
            st.session_state.nama_karyawan = ""
            st.session_state.usia_karyawan = 18
            st.session_state.gaji_karyawan = 0
            st.session_state.divisi_karyawan = "Frontend"
            st.session_state.reset_karyawan_form = False

        with st.form("form_karyawan"):
            nama = st.text_input("Nama Karyawan", key="nama_karyawan")
            usia = int(st.number_input("Usia", min_value=18, max_value=70, key="usia_karyawan"))
            gaji = int(st.number_input("Gaji", min_value=0, key="gaji_karyawan"))
            divisi = st.selectbox("Divisi", ["Frontend", "Backend", "UI/UX", "Project Manager"], key="divisi_karyawan")

            submitted = st.form_submit_button("Tambah Karyawan")

            if submitted:
                if not nama.strip():
                    st.error("❌ Nama tidak boleh kosong.")
                elif gaji <= 0:
                    st.error("❌ Gaji harus lebih dari 0.")
                elif usia < 18:
                    st.error("❌ Usia minimal adalah 18 tahun.")
                else:
                    profil.tambah_karyawan(nama, usia, gaji, divisi)
                    st.success("✅ Karyawan berhasil ditambahkan")
                    st.session_state.reset_karyawan_form = True
                    st.rerun()


        # ✅ Tambahkan ini agar daftar karyawan muncul
        st.subheader("📋 Daftar Karyawan")
        data = Karyawan.semua()
        for row in data:
            k = Karyawan(row[1], row[2], row[3], row[4], row[5], row[0])
            mark = " ❗" if k.sedang_mengerjakan() else "⚪"
            st.markdown(f"**{k.nama}{mark}** | {k.divisi} | Rp{k.gaji:,} | Usia: {k.usia}")
            with st.expander("Kelola", expanded=False):
                nama_baru = st.text_input(f"Update Nama {k.nama}", value=k.nama, key=f"nama{k.id}")
                usia_baru = int(st.number_input(f"Update Usia {k.nama}", value=k.usia, min_value=18, max_value=70, key=f"usia{k.id}"))
                gaji_baru = int(st.number_input(f"Update Gaji {k.nama}", value=k.gaji, key=f"gaji{k.id}"))
                divisi_baru = st.text_input(f"Update Divisi {k.nama}", value=k.divisi, key=f"divisi{k.id}")

                if st.button("Update", key=f"update{k.id}"):
                    if not nama_baru.strip():
                        st.error("❌ Nama karyawan tidak boleh kosong.")
                    elif usia_baru < 18:
                        st.error("❌ Usia karyawan minimal 18 tahun.")
                    elif gaji_baru < 0:
                        st.error("❌ Gaji tidak boleh negatif.")
                    elif not divisi_baru.strip():
                        st.error("❌ Divisi tidak boleh kosong.")
                    else:
                        Karyawan.update(k.id, nama_baru, usia_baru, gaji_baru, divisi_baru)
                        st.success("✅ Data karyawan diperbarui")
                        st.rerun()


                if st.button("Pecat", key=f"hapus{k.id}"):
                    k.hapus(k.id)
                    st.warning("Karyawan dihapus")
                    st.rerun()



elif menu == "Daftar Proyek":
    st.header("📝 Daftar Proyek Aktif")
    profil = Perusahaan.get_profil()
    if not profil:
        st.warning("Silakan isi profil perusahaan terlebih dahulu.")
    else:
        with st.expander("➕ Tambah Proyek"):
            if "reset_form" not in st.session_state:
                st.session_state.reset_form = False

            if st.session_state.reset_form:
                st.session_state.proyek_nama = ""
                st.session_state.proyek_client = ""
                st.session_state.proyek_nilai = 0
                st.session_state.proyek_deadline = datetime.today()
                st.session_state.proyek_karyawan = []
                st.session_state.reset_form = False

            nama = st.text_input("Nama Proyek", key="proyek_nama")
            client = st.text_input("Nama Client", key="proyek_client")
            nilai = int(st.number_input("Nilai Proyek", min_value=0, key="proyek_nilai"))
            deadline = st.date_input("Deadline", key="proyek_deadline")

            karyawan_list = Karyawan.semua()
            id_karyawan_list = st.multiselect(
                "Pilih Karyawan:",
                options=[k[0] for k in karyawan_list],
                format_func=lambda x: f"{x} - {next(k[1] for k in karyawan_list if k[0] == x)}",
                key="proyek_karyawan"
            )

            if st.button("Simpan Proyek"):
                if not nama.strip() or not client.strip():
                    st.error("❌ Nama proyek dan nama client tidak boleh kosong.")
                elif nilai <= 0:
                    st.error("❌ Nilai proyek harus lebih dari 0.")
                elif len(id_karyawan_list) < 1:
                    st.error("❌ Setiap proyek harus memiliki minimal satu karyawan.")
                else:
                    proyek = Proyek(nama, str(deadline), 'Aktif', profil.id, client, nilai)
                    proyek.simpan()
                    for id_k in id_karyawan_list:
                        pekerja = Karyawan.dari_db(id_k)
                        if pekerja:
                            pekerja.mengerjakan_proyek(proyek.id)
                    st.success("✅ Proyek berhasil ditambahkan!")
                    st.session_state.reset_form = True
                    st.rerun()




        st.subheader("📋 Proyek Aktif")
        proyek_data = Proyek.aktif_saja()

        for row in proyek_data:
            with st.container():
                pekerja = Proyek.karyawan_untuk_proyek(row[0])

                # === BAGIAN ATAS (Checkbox + Tombol Batal) ===
                col1, col2 = st.columns([1, 1])
                with col1:
                    selesai = st.checkbox("Tandai sebagai selesai", key=f"selesai_{row[0]}")
                    if selesai and st.button("✅ Konfirmasi", key=f"konfirmasi_{row[0]}"):
                        Proyek.update_status(row[0], "Selesai")
                        st.success("Proyek selesai!")
                        st.rerun()

                with col2:
                    if st.button("🚫 Batal Proyek", key=f"batal_{row[0]}"):
                        Proyek.update_status(row[0], "Dibatalkan")
                        st.warning("Proyek dibatalkan!")
                        st.rerun()

                # === BOX HTML untuk Info Proyek ===
                konten_html = f"""
                <div style="
                    background-color: #fdfdfd;
                    padding: 20px;
                    border-radius: 10px;
                    border: 2px solid #e0e0e0;
                    box-shadow: 0 2px 6px rgba(0,0,0,0.1);
                    margin-bottom: 10px;
                    font-family: 'Segoe UI', sans-serif;
                ">
                    <strong>{row[1]}</strong> <br>
                    <b>Deadline:</b> {row[2]} <br>
                    <b>Client:</b> {row[5]} <br>
                    <b>Nilai:</b> Rp{row[6]:,} <br><br>
                    <b>👷 Dikerjakan oleh:</b><br>
                    <ul style="margin-top: 0;">
                """

                for k in pekerja:
                    karyawan_lengkap = Karyawan.dari_db(k[0])
                    if karyawan_lengkap:
                        konten_html += f"<li>{karyawan_lengkap.nama} ({karyawan_lengkap.divisi}) - ID: {karyawan_lengkap.id}</li>"
                    else:
                        konten_html += f"<li>{k[1]} (ID: {k[0]})</li>"

                konten_html += "</ul></div>"
                html(konten_html, height=240)

                # === EXPANDER EDIT === (di bawah box dan masih satu container)
                with st.expander("✏️ Edit Proyek", expanded=False):
                    new_deadline = st.date_input("Deadline Baru", value=datetime.strptime(row[2], "%Y-%m-%d"), key=f"deadline_{row[0]}")
                    new_nilai = int(st.number_input("Nilai Proyek", value=row[6], min_value=0, key=f"nilai_{row[0]}"))

                    karyawan_list = Karyawan.semua()
                    current_ids = [k[0] for k in pekerja]
                    selected_karyawan = st.multiselect(
                        "Update Karyawan",
                        options=[k[0] for k in karyawan_list],
                        default=current_ids,
                        format_func=lambda x: f"{x} - {next(k[1] for k in karyawan_list if k[0] == x)}",
                        key=f"karyawan_{row[0]}"
                    )

                    if st.button("💾 Simpan Perubahan", key=f"simpan_{row[0]}"):
                        if new_nilai <= 0:
                            st.error("❌ Nilai proyek harus lebih dari 0.")
                        elif len(selected_karyawan) < 1:
                            st.error("❌ Proyek harus dikerjakan minimal oleh satu karyawan.")
                        else:
                            Proyek.update_nilai_deadline(row[0], str(new_deadline), new_nilai)
                            Proyek.hapus_karyawan_dari_proyek(row[0])
                            for id_k in selected_karyawan:
                                pekerja = Karyawan.dari_db(id_k)
                                if pekerja:
                                    pekerja.mengerjakan_proyek(row[0])
                            st.success("✅ Proyek diperbarui!")
                            st.rerun()

                st.markdown("<hr style='margin-top:25px; margin-bottom:25px; border: 1px solid #ccc;'>", unsafe_allow_html=True)



elif menu == "Riwayat Proyek":
    st.header("📁 Riwayat Proyek Selesai")

    # Checkbox untuk melihat semua
    tampilkan_semua = st.checkbox("Tampilkan semua proyek selesai", value=True)

    semua_proyek_selesai = [p for p in Proyek.semua() if p[3] in ["Selesai", "Dibatalkan"]]

    proyek_selesai = []

    if tampilkan_semua:
        proyek_selesai = semua_proyek_selesai
    else:
        st.subheader("🔍 Filter Deadline Proyek")
        col1, col2 = st.columns(2)
        with col1:
            tanggal_mulai = st.date_input("Dari Tanggal")
        with col2:
            tanggal_akhir = st.date_input("Sampai Tanggal")

        for p in semua_proyek_selesai:
            try:
                deadline_date = datetime.strptime(p[2], "%Y-%m-%d").date()
                if tanggal_mulai <= deadline_date <= tanggal_akhir:
                    proyek_selesai.append(p)
            except:
                pass  # abaikan jika format tanggal salah
    proyek_selesai.sort(key=lambda x: datetime.strptime(x[2], "%Y-%m-%d"), reverse=True)
    if not proyek_selesai:
        st.info("Tidak ada proyek yang sesuai dengan kriteria.")
    else:
        st.markdown("""
            <style>
                .riwayat-box {
                    background-color: #f9f9f9;
                    padding: 20px;
                    margin-bottom: 20px;
                    border: 2px solid #e0e0e0;
                    border-radius: 10px;
                    box-shadow: 0 2px 5px rgba(0,0,0,0.05);
                }
                .judul-proyek {
                    font-weight: bold;
                    font-size: 18px;
                    color: #2c3e50;
                    margin-bottom: 10px;
                }
                .detail-proyek {
                    margin-left: 10px;
                    font-size: 15px;
                    line-height: 1.5;
                }
            </style>
        """, unsafe_allow_html=True)

        for row in proyek_selesai:
            pekerja = Proyek.karyawan_untuk_proyek(row[0])
            
            # Kumpulan data pekerja
            pekerja_html = ""
            for k in pekerja:
                karyawan_lengkap = Karyawan.dari_db(k[0])
                if karyawan_lengkap:
                    pekerja_html += f"<li>{karyawan_lengkap.nama} ({karyawan_lengkap.divisi}) - ID: {karyawan_lengkap.id}</li>"
                else:
                    pekerja_html += f"<li>{k[1]} (ID: {k[0]})</li>"

            # Tentukan icon berdasarkan status proyek
            ikon_status = "✅" if row[3] == "Selesai" else "❌"

            # Gabungkan seluruh isi box dalam satu markdown
            st.markdown(f"""
                <div class='riwayat-box'>
                    <div class='judul-proyek'>{ikon_status} {row[1]}</div>
                    <div class='detail-proyek'>
                        📅 <b>Deadline:</b> {row[2]}<br>
                        📄 <b>Status:</b> {row[3]}<br>
                        👤 <b>Client:</b> {row[5]}<br>
                        💰 <b>Nilai:</b> Rp{row[6]}<br><br>
                        🧑‍💼 <b>Dikerjakan oleh:</b>
                        <ul>
                            {pekerja_html}
                        </ul>
                    </div>
                </div>
            """, unsafe_allow_html=True)







# LIHAT SEMUA DATA
elif menu == "Lihat Semua Data":
    st.header("📊 Ringkasan Seluruh Data")
    perusahaan = Perusahaan.get_profil()
    if perusahaan:
        st.subheader("Perusahaan")
        st.write(f"Nama: {perusahaan.nama}")
        st.write(f"Email: {perusahaan.email}")

    st.subheader("Karyawan")
    karyawan_data = Karyawan.semua()
    karyawan_df = pd.DataFrame(karyawan_data, columns=["ID", "Nama", "Usia", "Gaji", "Divisi", "Perusahaan ID"])
    st.table(karyawan_df)

    st.subheader("Proyek")
    proyek_data = Proyek.semua()
    proyek_df = pd.DataFrame(proyek_data, columns=["ID", "Nama Proyek", "Deadline", "Status", "Perusahaan ID", "Client", "Nilai"])
    st.table(proyek_df)
