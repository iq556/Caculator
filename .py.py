# kalkulator_gui.py

import tkinter as tk
from tkinter import messagebox
import datetime

# ==== Fungsi Perhitungan ====

def tambah(a, b): return a + b
def kurang(a, b): return a - b
def kali(a, b): return a * b
def bagi(a, b):
    if b == 0:
        return "Error: Pembagian dengan nol!"
    return a / b

# ==== Logging Riwayat ====

def log_hasil(op, a, b, hasil):
    waktu = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    dengan = f"{a} {op} {b} = {hasil}"
    log_entry = f"[{waktu}] {dengan}\n"

    with open("riwayat_kalkulator.txt", "a") as f:
        f.write(log_entry)

# ==== Fungsi Saat Tombol Ditekan ====

def hitung(operasi):
    try:
        angka1 = float(entry1.get())
        angka2 = float(entry2.get())

        if operasi == "+":
            hasil = tambah(angka1, angka2)
        elif operasi == "-":
            hasil = kurang(angka1, angka2)
        elif operasi == "×":
            hasil = kali(angka1, angka2)
        elif operasi == "÷":
            hasil = bagi(angka1, angka2)

        hasil_label.config(text=f"Hasil: {hasil}")
        log_hasil(operasi, angka1, angka2, hasil)

    except ValueError:
        messagebox.showerror("Input Error", "Masukkan angka yang valid!")

# ==== GUI Tkinter ====

root = tk.Tk()
root.title("Kalkulator GUI")
root.geometry("300x350")
root.resizable(False, False)

tk.Label(root, text="Angka Pertama").pack(pady=5)
entry1 = tk.Entry(root)
entry1.pack(pady=5)

tk.Label(root, text="Angka Kedua").pack(pady=5)
entry2 = tk.Entry(root)
entry2.pack(pady=5)

tk.Label(root, text="Operasi").pack(pady=10)

frame = tk.Frame(root)
frame.pack()

tk.Button(frame, text="+", width=5, command=lambda: hitung("+")).grid(row=0, column=0, padx=5)
tk.Button(frame, text="-", width=5, command=lambda: hitung("-")).grid(row=0, column=1, padx=5)
tk.Button(frame, text="×", width=5, command=lambda: hitung("×")).grid(row=0, column=2, padx=5)
tk.Button(frame, text="÷", width=5, command=lambda: hitung("÷")).grid(row=0, column=3, padx=5)

hasil_label = tk.Label(root, text="Hasil: ", font=("Arial", 12))
hasil_label.pack(pady=20)

def lihat_log():
    try:
        with open("riwayat_kalkulator.txt", "r") as f:
            log = f.read()
        messagebox.showinfo("Riwayat Perhitungan", log)
    except FileNotFoundError:
        messagebox.showinfo("Riwayat Perhitungan", "Belum ada perhitungan dilakukan.")

tk.Button(root, text="Lihat Riwayat", command=lihat_log).pack(pady=10)

root.mainloop()
