import sqlite3  # Untuk interaksi dengan database SQLite
from tkinter import Tk, Label, Entry, Button, StringVar, messagebox, ttk  # Untuk membuat antarmuka GUI

# Fungsi untuk membuat database dan tabel jika belum ada
def create_database():
    # Membuka koneksi ke SQLite dan membuat tabel jika belum ada
    conn = sqlite3.connect('nilai_siswa.db')  # Koneksi ke database SQLite
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS nilai_siswa (  -- Membuat tabel jika belum ada
            id INTEGER PRIMARY KEY AUTOINCREMENT,  -- ID unik untuk setiap siswa
            nama_siswa TEXT,                       -- Nama siswa
            biologi INTEGER,                       -- Nilai Biologi
            fisika INTEGER,                        -- Nilai Fisika
            inggris INTEGER,                       -- Nilai Inggris
            prediksi_fakultas TEXT                 -- Prediksi fakultas berdasarkan nilai
        )
    ''')
    conn.commit()  # Menyimpan perubahan
    conn.close()  # Menutup koneksi database

# Fungsi untuk mengambil semua data dari tabel nilai_siswa
def fetch_data():
    # Membuka koneksi ke SQLite untuk membaca data
    conn = sqlite3.connect('nilai_siswa.db')  # Koneksi ke database
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM nilai_siswa")  # Query untuk mengambil semua data
    rows = cursor.fetchall()  # Menyimpan hasil query
    conn.close()  # Menutup koneksi database
    return rows

# Fungsi untuk menyimpan data siswa baru ke database
def save_to_database(nama, biologi, fisika, inggris, prediksi):
    # Membuka koneksi ke SQLite untuk menyimpan data baru
    conn = sqlite3.connect('nilai_siswa.db')  # Koneksi ke database
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO nilai_siswa (nama_siswa, biologi, fisika, inggris, prediksi_fakultas)
        VALUES (?, ?, ?, ?, ?)  -- Menyimpan data menggunakan parameter
    ''', (nama, biologi, fisika, inggris, prediksi))
    conn.commit()  # Menyimpan perubahan
    conn.close()  # Menutup koneksi database

# Fungsi untuk memperbarui data siswa berdasarkan ID
def update_database(record_id, nama, biologi, fisika, inggris, prediksi):
    # Membuka koneksi ke SQLite untuk memperbarui data
    conn = sqlite3.connect('nilai_siswa.db')  # Koneksi ke database
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE nilai_siswa
        SET nama_siswa = ?, biologi = ?, fisika = ?, inggris = ?, prediksi_fakultas = ?
        WHERE id = ?  -- Memperbarui berdasarkan ID
    ''', (nama, biologi, fisika, inggris, prediksi, record_id))
    conn.commit()  # Menyimpan perubahan
    conn.close()  # Menutup koneksi database

# Fungsi untuk menghapus data siswa berdasarkan ID
def delete_database(record_id):
    # Membuka koneksi ke SQLite untuk menghapus data
    conn = sqlite3.connect('nilai_siswa.db')  # Koneksi ke database
    cursor = conn.cursor()
    cursor.execute('DELETE FROM nilai_siswa WHERE id = ?', (record_id,))  # Menghapus berdasarkan ID
    conn.commit()  # Menyimpan perubahan
    conn.close()  # Menutup koneksi database

# Fungsi untuk menghitung prediksi fakultas berdasarkan nilai
def calculate_prediction(biologi, fisika, inggris):
    # Logika prediksi berdasarkan nilai tertinggi
    if biologi > fisika and biologi > inggris:
        return "Kedokteran"  # Prediksi Kedokteran jika nilai Biologi tertinggi
    elif fisika > biologi and fisika > inggris:
        return "Teknik"  # Prediksi Teknik jika nilai Fisika tertinggi
    elif inggris > biologi and inggris > fisika:
        return "Bahasa"  # Prediksi Bahasa jika nilai Inggris tertinggi
    else:
        return "Tidak Diketahui"  # Prediksi default jika nilai sama

# Fungsi untuk menambahkan data siswa
def submit():
    try:
        # Mendapatkan nilai dari input
        nama = nama_var.get()
        biologi = int(biologi_var.get())
        fisika = int(fisika_var.get())
        inggris = int(inggris_var.get())

        if not nama:
            raise Exception("Nama siswa tidak boleh kosong.")  # Validasi nama kosong

        # Menghitung prediksi fakultas
        prediksi = calculate_prediction(biologi, fisika, inggris)
        save_to_database(nama, biologi, fisika, inggris, prediksi)  # Menyimpan data

        messagebox.showinfo("Sukses", f"Data berhasil disimpan!\nPrediksi Fakultas: {prediksi}")
        clear_inputs()  # Membersihkan input
        populate_table()  # Memperbarui tabel
    except ValueError as e:
        messagebox.showerror("Error", f"Input tidak valid: {e}")  # Menangani error input

# Fungsi untuk memperbarui data siswa
def update():
    try:
        if not selected_record_id.get():
            raise Exception("Pilih data dari tabel untuk di-update!")  # Validasi jika ID belum dipilih

        # Mendapatkan nilai dari input
        record_id = int(selected_record_id.get())
        nama = nama_var.get()
        biologi = int(biologi_var.get())
        fisika = int(fisika_var.get())
        inggris = int(inggris_var.get())

        if not nama:
            raise ValueError("Nama siswa tidak boleh kosong.")  # Validasi nama kosong

        # Menghitung prediksi fakultas
        prediksi = calculate_prediction(biologi, fisika, inggris)
        update_database(record_id, nama, biologi, fisika, inggris, prediksi)  # Memperbarui data

        messagebox.showinfo("Sukses", "Data berhasil diperbarui!")
        clear_inputs()  # Membersihkan input
        populate_table()  # Memperbarui tabel
    except ValueError as e:
        messagebox.showerror("Error", f"Kesalahan: {e}")  # Menangani error input

# Fungsi untuk menghapus data siswa
def delete():
    try:
        if not selected_record_id.get():
            raise Exception("Pilih data dari tabel untuk dihapus!")  # Validasi jika ID belum dipilih

        record_id = int(selected_record_id.get())  # Mendapatkan ID dari input
        delete_database(record_id)  # Menghapus data berdasarkan ID
        messagebox.showinfo("Sukses", "Data berhasil dihapus!")
        clear_inputs()  # Membersihkan input
        populate_table()  # Memperbarui tabel
    except ValueError as e:
        messagebox.showerror("Error", f"Kesalahan: {e}")  # Menangani error input

# Fungsi untuk membersihkan input di form
def clear_inputs():
    nama_var.set("")
    biologi_var.set("")
    fisika_var.set("")
    inggris_var.set("")
    selected_record_id.set("")

# Fungsi untuk memperbarui isi tabel dengan data dari database
def populate_table():
    for row in tree.get_children():
        tree.delete(row)  # Menghapus semua data lama di tabel
    for row in fetch_data():
        tree.insert('', 'end', values=row)  # Menambahkan data baru ke tabel

# Fungsi untuk mengisi input form dari data tabel yang dipilih
def fill_inputs_from_table(event):
    try:
        selected_item = tree.selection()[0]  # Mendapatkan item yang dipilih
        selected_row = tree.item(selected_item)['values']  # Mendapatkan nilai dari item

        # Mengisi form dengan data dari tabel
        selected_record_id.set(selected_row[0])
        nama_var.set(selected_row[1])
        biologi_var.set(selected_row[2])
        fisika_var.set(selected_row[3])
        inggris_var.set(selected_row[4])
    except IndexError:
        messagebox.showerror("Error", "Pilih data yang valid!")  # Menangani kesalahan jika tidak ada yang dipilih

# Inisialisasi database
create_database()

# Membuat GUI menggunakan Tkinter
root = Tk()
root.title("Prediksi Fakultas Siswa")

# Variabel untuk input
nama_var = StringVar()
biologi_var = StringVar()
fisika_var = StringVar()
inggris_var = StringVar()
selected_record_id = StringVar()  # Untuk menyimpan ID record yang dipilih

# Membuat form input
Label(root, text="Nama Siswa").grid(row=0, column=0, padx=10, pady=5)
Entry(root, textvariable=nama_var).grid(row=0, column=1, padx=10, pady=5)

Label(root, text="Nilai Biologi").grid(row=1, column=0, padx=10, pady=5)
Entry(root, textvariable=biologi_var).grid(row=1, column=1, padx=10, pady=5)

Label(root, text="Nilai Fisika").grid(row=2, column=0, padx=10, pady=5)
Entry(root, textvariable=fisika_var).grid(row=2, column=1, padx=10, pady=5)

Label(root, text="Nilai Inggris").grid(row=3, column=0, padx=10, pady=5)
Entry(root, textvariable=inggris_var).grid(row=3, column=1, padx=10, pady=5)

# Membuat tombol aksi
Button(root, text="Tambah Data", command=submit).grid(row=4, column=0, padx=10, pady=10)
Button(root, text="Update Data", command=update).grid(row=4, column=1, padx=10, pady=10)
Button(root, text="Hapus Data", command=delete).grid(row=5, column=0, padx=10, pady=10)
Button(root, text="Bersihkan Input", command=clear_inputs).grid(row=5, column=1, padx=10, pady=10)

# Membuat tabel untuk menampilkan data
columns = ("ID", "Nama", "Biologi", "Fisika", "Inggris", "Prediksi Fakultas")
tree = ttk.Treeview(root, columns=columns, show='headings')
tree.heading("ID", text="ID")
tree.heading("Nama", text="Nama")
tree.heading("Biologi", text="Biologi")
tree.heading("Fisika", text="Fisika")
tree.heading("Inggris", text="Inggris")
tree.heading("Prediksi Fakultas", text="Prediksi Fakultas")
tree.grid(row=6, column=0, columnspan=2, pady=10)

# Menangani event klik pada tabel
tree.bind('<Double-1>', fill_inputs_from_table)

# Memperbarui tabel saat pertama kali aplikasi dibuka
populate_table()

# Menjalankan aplikasi
root.mainloop()