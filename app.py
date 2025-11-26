from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Buat database jika belum ada
def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS mobil (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            merek TEXT NOT NULL,
            model TEXT NOT NULL,
            tahun INTEGER NOT NULL,
            harga REAL NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# Halaman utama - tampilkan semua data
@app.route('/')
def index():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM mobil')
    data = cursor.fetchall()
    conn.close()
    return render_template('index.html', data=data)

# Tambah data mobil
@app.route('/tambah', methods=['GET', 'POST'])
def tambah():
    if request.method == 'POST':
        merek = request.form['merek']
        model = request.form['model']
        tahun = request.form['tahun']
        harga = request.form['harga']

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO mobil (merek, model, tahun, harga) VALUES (?, ?, ?, ?)', 
                       (merek, model, tahun, harga))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    return render_template('tambah.html')

# Hapus data mobil
@app.route('/hapus/<int:id>')
def hapus(id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM mobil WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
