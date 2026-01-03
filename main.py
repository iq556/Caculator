# main.py
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    # For type-checkers and linters only; won't be executed at runtime.
    from kivy.app import App  # type: ignore
    from kivy.uix.screenmanager import ScreenManager, Screen  # type: ignore
    from kivy.uix.popup import Popup  # type: ignore
    from kivy.uix.label import Label  # type: ignore
else:
    try:
        from kivy.app import App
        from kivy.uix.screenmanager import ScreenManager, Screen
        from kivy.uix.popup import Popup
        from kivy.uix.label import Label
        HAS_KIVY = True
    except Exception:
        # Fallback stubs so the module can be imported in environments without Kivy
        HAS_KIVY = False

        class App:
            def run(self):
                print("Kivy not available: App.run() called")

        class ScreenManager:
            pass

        class Screen:
            def __init__(self, **kwargs):
                self.ids = {}

        class Popup:
            def __init__(self, title='', content=None, size_hint=(None, None), size=(0, 0)):
                self.title = title
                self.content = content
                self.size_hint = size_hint
                self.size = size
            def open(self):
                print(f"Popup: {self.title}")
                if hasattr(self.content, 'text'):
                    print(self.content.text)

        class Label:
            def __init__(self, text=''):
                self.text = text

# Standard library imports
import sqlite3
import os
import math
from datetime import datetime

# Try to import optional Kivy modules with fallbacks for properties/storage used in this file
if TYPE_CHECKING:
    # For type checkers only; avoid runtime import errors in environments without Kivy
    from kivy.properties import BooleanProperty  # type: ignore
    from kivy.storage.jsonstore import JsonStore  # type: ignore
else:
    try:
        from kivy.properties import BooleanProperty  # type: ignore
        from kivy.storage.jsonstore import JsonStore  # type: ignore
    except Exception:
        class BooleanProperty:
            def __init__(self, default=False):
                self.default = default

        class JsonStore:
            def __init__(self, path):
                self._path = path
                self._store = {}
            def exists(self, key):
                return key in self._store
            def put(self, key, **kwargs):
                self._store[key] = kwargs
            def get(self, key):
                return self._store.get(key, {})

store = JsonStore("userprefs.json")  # Untuk remember me

# === Inisialisasi Database Login ===
def init_db():
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT NOT NULL
        )
    """)
    # Tambah user default jika belum ada
    c.execute("INSERT OR IGNORE INTO users (username, password) VALUES (?, ?)", ("admin", "1234"))
    conn.commit()
    conn.close()

class LoginScreen(Screen):
    remember_me = BooleanProperty(False)

    def on_pre_enter(self):
        # Auto-login jika remember me aktif
        if store.exists("user") and store.get("user")["remember"]:
            self.manager.current = "kalkulator"

    def login(self):
        username = self.ids.username.text
        password = self.ids.password.text
        self.remember_me = self.ids.remember_checkbox.active

        conn = sqlite3.connect("users.db")
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        result = c.fetchone()
        conn.close()

        if result:
            store.put("user", username=username, remember=self.remember_me)
            self.manager.current = "kalkulator"
        else:
            Popup(title="Login Gagal",
                  content=Label(text="Username atau password salah."),
                  size_hint=(None, None), size=(300, 200)).open()

class KalkulatorScreen(Screen):
    def hitung(self, operasi):
        try:
            a = float(self.ids.input_a.text)
            b = float(self.ids.input_b.text) if self.ids.input_b.text else 0

            if operasi == "+":
                hasil = a + b
            elif operasi == "-":
                hasil = a - b
            elif operasi == "*":
                hasil = a * b
            elif operasi == "/":
                hasil = a / b if b != 0 else "Error: ÷ 0"
            elif operasi == "^":
                hasil = math.pow(a, b)
            elif operasi == "%":
                hasil = a % b
            elif operasi == "√":
                hasil = math.sqrt(a) if a >= 0 else "Error: akar negatif"
            else:
                hasil = "Operasi tidak dikenal"

            self.ids.output.text = f"Hasil: {hasil}"
            self.simpan_log(a, operasi, b, hasil)

        except ValueError:
            Popup(title="Input Error",
                  content=Label(text="Harus berupa angka!"),
                  size_hint=(None, None), size=(300, 200)).open()

    def simpan_log(self, a, operasi, b, hasil):
        waktu = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        baris = f"[{waktu}] {a} {operasi} {b} = {hasil}\n"
        with open("hasil_log.txt", "a") as f:
            f.write(baris)

    def lihat_log(self):
        try:
            with open("hasil_log.txt", "r") as f:
                isi = f.read()
            Popup(title="Riwayat", content=Label(text=isi),
                  size_hint=(0.9, 0.9)).open()
        except FileNotFoundError:
            Popup(title="Riwayat", content=Label(text="Belum ada data."),
                  size_hint=(None, None), size=(300, 200)).open()

class KalkulatorApp(App):
    def build(self):
        init_db()
        sm = ScreenManager()
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(KalkulatorScreen(name='kalkulator'))
        return sm
import math
from datetime import datetime

# ===== Login Screen =====
class LoginScreen(Screen):
    def login(self):
        username = self.ids.username.text
        password = self.ids.password.text

        if username == "admin" and password == "1234":
            self.manager.current = "kalkulator"
        else:
            popup = Popup(title='Login Gagal',
                          content=Label(text='Username/password salah'),
                          size_hint=(None, None), size=(300, 200))
            popup.open()

# ===== Kalkulator Screen =====
class KalkulatorScreen(Screen):
    def hitung(self, operasi):
        try:
            a = float(self.ids.input_a.text)
            b = float(self.ids.input_b.text) if self.ids.input_b.text else 0

            if operasi == "+":
                hasil = a + b
            elif operasi == "-":
                hasil = a - b
            elif operasi == "*":
                hasil = a * b
            elif operasi == "/":
                hasil = a / b if b != 0 else "Error: ÷ 0"
            elif operasi == "^":
                hasil = math.pow(a, b)
            elif operasi == "%":
                hasil = a % b
            elif operasi == "√":
                hasil = math.sqrt(a) if a >= 0 else "Error: akar negatif"
            else:
                hasil = "Operasi tidak dikenal"

            self.ids.output.text = f"Hasil: {hasil}"
            self.simpan_log(a, operasi, b, hasil)

        except ValueError:
            popup = Popup(title='Error',
                          content=Label(text='Input harus berupa angka!'),
                          size_hint=(None, None), size=(300, 200))
            popup.open()

    def simpan_log(self, a, operasi, b, hasil):
        waktu = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        baris = f"[{waktu}] {a} {operasi} {b} = {hasil}\n"
        with open("hasil_log.txt", "a") as f:
            f.write(baris)

    def lihat_log(self):
        try:
            with open("hasil_log.txt", "r") as f:
                isi = f.read()
            popup = Popup(title="Riwayat", content=Label(text=isi),
                          size_hint=(0.9, 0.9))
            popup.open()
        except FileNotFoundError:
            popup = Popup(title="Riwayat", content=Label(text="Belum ada data."),
                          size_hint=(None, None), size=(300, 200))
            popup.open()

# ===== App & Screen Manager =====
class KalkulatorApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(KalkulatorScreen(name='kalkulator'))
        return sm
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from kivy.uix.boxlayout import BoxLayout  # type: ignore
    from kivy.uix.popup import Popup  # type: ignore
    from kivy.uix.label import Label  # type: ignore
else:
    try:
        from kivy.uix.boxlayout import BoxLayout  # type: ignore
        from kivy.uix.popup import Popup  # type: ignore
        from kivy.uix.label import Label  # type: ignore
    except Exception:
        # Fallback stubs so the module can be imported in environments without Kivy
        class BoxLayout:
            def __init__(self, **kwargs):
                self.children = []
                self.ids = {}
            def add_widget(self, widget):
                self.children.append(widget)

        class Popup:
            def __init__(self, title='', content=None, size_hint=(None, None), size=(0, 0)):
                self.title = title
                self.content = content
                self.size_hint = size_hint
                self.size = size
            def open(self):
                # simple console fallback
                print(f"Popup: {self.title}")
                if hasattr(self.content, 'text'):
                    print(self.content.text)

        class Label:
            def __init__(self, text=''):
                self.text = text

import math
from datetime import datetime

class Kalkulator(BoxLayout):
    def hitung(self, operasi):
        try:
            a = float(self.ids.input_a.text)
            b = float(self.ids.input_b.text) if self.ids.input_b.text else 0

            if operasi == "+":
                hasil = a + b
            elif operasi == "-":
                hasil = a - b
            elif operasi == "*":
                hasil = a * b
            elif operasi == "/":
                hasil = a / b if b != 0 else "Error: ÷ 0"
            elif operasi == "^":
                hasil = math.pow(a, b)
            elif operasi == "%":
                hasil = a % b
            elif operasi == "√":
                hasil = math.sqrt(a) if a >= 0 else "Error: akar negatif"
            else:
                hasil = "Operasi tidak dikenal"

            self.ids.output.text = f"Hasil: {hasil}"
            self.simpan_log(a, operasi, b, hasil)

        except ValueError:
            self.popup("Input tidak valid!")

    def popup(self, pesan):
        box = BoxLayout()
        box.add_widget(Label(text=pesan))
        popup = Popup(title='Error', content=box, size_hint=(None, None), size=(300, 200))
        popup.open()

    def simpan_log(self, a, operasi, b, hasil):
        waktu = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        baris = f"[{waktu}] {a} {operasi} {b} = {hasil}\n"
        with open("hasil_log.txt", "a") as f:
            f.write(baris)

    def lihat_log(self):
        try:
            with open("hasil_log.txt", "r") as f:
                isi = f.read()
            self.popup(isi)
        except FileNotFoundError:
            self.popup("Belum ada perhitungan.")

