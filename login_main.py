import tkinter as tk
import sqlite3
import hashlib
from main import main
from tkinter import messagebox

conn = sqlite3.connect('system.db')
cursor = conn.cursor()
        
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL
)
''')

cursor.execute('SELECT * FROM users WHERE username = ?', ('admin',))
user = cursor.fetchone()

if not user:
    hashed_password = hashlib.sha256("admin123".encode()).hexdigest()
    cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', ('admin', hashed_password))
    conn.commit()

conn.close()

class Login(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry('1000x600')
        self.title("Hotel Management System")

        self.bg_image = tk.Canvas(self, width=900, height=500)
        self.bg_image.pack(fill="both", expand=True)
        self.image = tk.PhotoImage(file='C:\\Users\\Senpai\\PycharmProjects\\pythonExercise\\Codechum tkinter\\Hotel Management System\\images\\login_image_bg.png')
        self.bg_image.create_image(0, 0, image=self.image, anchor='nw')

        #Login Page
        self.main_frame = tk.Frame(self.bg_image, width=410, height=300, bg='#E9E9E9')
        self.main_frame.propagate(False)
        self.main_frame.pack(pady=140)

        self.main_head = tk.Frame(self.main_frame, width=410, height=80, bg='blue')
        self.main_head.propagate(False)
        self.main_head.pack()

        self.login_label = tk.Label(self.main_head, text="LUXURY GRANDE HOTEL", font=('times new roman', 20, 'bold italic'), bg='blue', fg='white')
        self.login_label.pack(pady=20)

        self.input_frame = tk.Frame(self.main_frame, width=300, height=100, bg='#E9E9E9')
        self.input_frame.propagate(False)
        self.input_frame.pack(pady=30)

        self.user_Label = tk.Label(self.input_frame, text="Username:", font=('arial', 15, 'bold'), bg='#E9E9E9')
        self.user_entry = tk.Entry(self.input_frame, width=20, font=('arial', 15))
        self.user_Label.grid(row=1, column=0, padx=20, pady=10)
        self.user_entry.grid(row=1, column=1)

        self.pass_label = tk.Label(self.input_frame, text="Password:", font=('arial', 15, 'bold'), bg='#E9E9E9')
        self.pass_entry = tk.Entry(self.input_frame, width=20, show='*', font=('arial', 15))
        self.pass_label.grid(row=2, column=0, padx=20, pady=10)
        self.pass_entry.grid(row=2, column=1)

        #Login Btn
        self.btn_frame = tk.Frame(self.main_frame, width=410, bg='black')
        self.btn_frame.pack(anchor='s')

        self.login_btn = tk.Button(self.btn_frame, text='Login', width=20, font=('arial', 15), fg='white', bg='blue', command=self.check_credentials)
        self.login_btn.grid(row=3, column=1)

    def check_credentials(self):
        username = self.user_entry.get()
        user_pass = self.pass_entry.get()

        self.user_entry.delete(0, tk.END)
        self.pass_entry.delete(0, tk.END)

        hashed_password = hashlib.sha256(user_pass.encode()).hexdigest()

        conn = sqlite3.connect('system.db')
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, hashed_password))
        user = cursor.fetchone()

        if user:
            self.destroy()
            main()

        else:
            messagebox.showerror(title="Error", message="Incorrect username or password. Please try again!")

if __name__ == "__main__":
    root = Login()
    root.mainloop()
