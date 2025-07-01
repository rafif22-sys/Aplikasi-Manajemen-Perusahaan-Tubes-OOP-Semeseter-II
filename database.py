import sqlite3

DB_NAME = 'perusahaan.db'
import os

# Lokasi database relatif terhadap proyek
DB_PATH = os.path.join(os.path.dirname(__file__), 'data.db')

def connect():
    return sqlite3.connect(DB_NAME)


