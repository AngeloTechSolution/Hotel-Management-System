import tkinter as tk
from tkinter import messagebox
import sqlite3

class checkin_form(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.geometry('1000x700')
        self.title('Hotel System Management')

        self.init_db()
        self.init_rooms()

        self.canvas_bg = tk.Canvas(self, width=1000, height=700, bg='#CFCDCD')
        self.canvas_bg.pack(fill='both', expand=True)

        self.top_frame = tk.Frame(self.canvas_bg, width=800, height=80,
                                  borderwidth=2, highlightthickness=2, bg='blue')
        self.top_label = tk.Label(self.top_frame, text="Check In", font=('New Times Roman', 30, 'bold italic'), fg='white', bg='blue')

        self.top_frame.pack(pady=10)
        self.top_frame.propagate(False)
        self.top_label.pack(pady=10)

        self.form_frame = tk.Frame(self.canvas_bg, width=800, height=800, relief="ridge", borderwidth=2)
        self.form_frame.pack(padx=20, pady=20)
        self.form_frame.propagate(False)

        # Name Entry
        self.name_label = tk.Label(self.form_frame, text="Enter Your Name:", font=('arial', 15, 'bold'))
        self.name_label.grid(row=0, column=0, padx=50, pady=5, sticky="w")
        self.name_entry = tk.Entry(self.form_frame, width=50)
        self.name_entry.grid(row=0, column=1, padx=10, pady=5)

        # Address Entry
        self.add_label = tk.Label(self.form_frame, text="Address:", font=('arial', 15, 'bold'))
        self.add_label.grid(row=1, column=0, padx=50, pady=5, sticky='w')
        self.add_entry = tk.Entry(self.form_frame, width=50)
        self.add_entry.grid(row=1, column=1, padx=10, pady=5)

        # Phone Number Entry
        self.number_label = tk.Label(self.form_frame, text="Phone Number:", font=('arial', 15, 'bold'))
        self.number_label.grid(row=2, column=0, padx=50, pady=5, sticky='w')
        self.number_entry = tk.Entry(self.form_frame, width=50)
        self.number_entry.grid(row=2, column=1, padx=50, pady=5)

        # Number of Days Entry
        self.days_label = tk.Label(self.form_frame, text="Number of Days:", font=('arial', 10))
        self.days_label.grid(row=3, column=0, padx=10, pady=25, sticky="e")
        self.days_entry = tk.Entry(self.form_frame)
        self.days_entry.grid(row=3, column=1, padx=10, pady=5)

        # Room Choice
        self.room_label = tk.Label(self.form_frame, text="Choose your room:", font=('arial', 10, 'bold'))
        self.room_label.grid(row=4, column=0, padx=0, pady=5, sticky='e')

        self.room_frame = tk.Frame(self.form_frame)
        self.room_frame.grid(row=4, column=1, padx=20)

        self.room_var = tk.IntVar()
        self.deluxe_rb = tk.Radiobutton(self.room_frame, text="Deluxe", variable=self.room_var, value=5000, command=self.display_price)
        self.deluxe_rb.grid(row=5, column=2, padx=10)
        self.general_rb = tk.Radiobutton(self.room_frame, text="General", variable=self.room_var, value=3500, command=self.display_price)
        self.general_rb.grid(row=5, column=3, sticky='w', padx=10)
        self.joint_rb = tk.Radiobutton(self.room_frame, text="Joint", variable=self.room_var, value=2500, command=self.display_price)
        self.joint_rb.grid(row=5, column=4, sticky='w', padx=10)

        # Price Display
        self.price_frame = tk.Frame(self.form_frame)
        self.price_frame.grid(row=6, column=1, sticky='w', pady=20, padx=40)

        self.price_label = tk.Label(self.price_frame, text="Price:", font=('arial', 10, 'bold'))
        self.price_label.grid(row=7, column=0, sticky='e')
        self.price = tk.Label(self.price_frame, text="₱0.00", font=('arial', 10, 'bold'))
        self.price.grid(row=7, column=1, sticky='e')

        # Submit Button
        self.submit_btn = tk.Button(self.form_frame, text="Submit", font=('arial', 12), bg='blue', fg='white', width=10, activebackground='gray', command=self.save_info)
        self.submit_btn.grid(row=10, column=0, columnspan=2, pady=20)

    def init_db(self):
        """Initialize the SQLite database and create the tables if they don't exist."""
        self.conn = sqlite3.connect('system.db')
        self.cursor = self.conn.cursor()

        # Create bookings table
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            address TEXT,
            phone TEXT,
            days INTEGER,
            room_type TEXT,
            room_number TEXT,
            price REAL
        )''')

        # Create rooms table
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS rooms (
            room_number TEXT PRIMARY KEY,
            room_type TEXT,
            available INTEGER
        )''')
        self.conn.commit()

    def init_rooms(self):
        """Add rooms to the database with specific room numbers."""
        rooms = {
            'Deluxe': ['D201', 'D202', 'D203', 'D204', 'D205'],
            'General': ['G201', 'G202', 'G203', 'G204', 'G205'],
            'Joint': ['J201', 'J202', 'J203', 'J204', 'J205']
        }

        for room_type, room_numbers in rooms.items():
            for room_number in room_numbers:
                self.cursor.execute('''INSERT OR IGNORE INTO rooms (room_number, room_type, available)
                                       VALUES (?, ?, ?)''', (room_number, room_type, 1))

        self.conn.commit()

    def display_price(self):
        self.selected_room = self.room_var.get()
        self.days = self.days_entry.get()

        # Check if the days entry is valid
        try:
            self.number = int(self.days)
            if self.number <= 0:
                raise ValueError("Days must be greater than zero.")
        except ValueError:
            messagebox.showwarning(title='Warning', message="Invalid Days Input! Please enter a valid number.")
            return

        # Calculate the total price
        self.total_price = self.number * self.selected_room
        self.price.config(text=f"₱{self.total_price:.2f}")

    def save_info(self):
        name = self.name_entry.get().strip()
        address = self.add_entry.get().strip()
        phone = self.number_entry.get().strip()
        days = self.days_entry.get().strip()
        room_type = 'Deluxe' if self.room_var.get() == 5000 else 'General' if self.room_var.get() == 3500 else 'Joint'
        price = self.total_price

        if not (name and address and phone and days and room_type):
            messagebox.showerror("Error", "All fields are required!")
            return

        try:
            days = int(days)

            # Check for available rooms
            self.cursor.execute('''SELECT COUNT(*) FROM rooms WHERE room_type = ? AND available = 1''', (room_type,))
            available_rooms = self.cursor.fetchone()[0]

            if available_rooms < 1:
                messagebox.showerror("No Rooms Available", f"No available {room_type} rooms.")
                return

            # Select and book a room
            self.cursor.execute('''SELECT room_number FROM rooms WHERE room_type = ? AND available = 1 LIMIT 1''', (room_type,))
            room = self.cursor.fetchone()

            if room:
                room_number = room[0]
                self.cursor.execute('''UPDATE rooms SET available = 0 WHERE room_number = ?''', (room_number,))  # Mark as occupied
                self.cursor.execute('''INSERT INTO bookings (name, address, phone, days, room_type, room_number, price)
                                       VALUES (?, ?, ?, ?, ?, ?, ?)''', (name, address, phone, days, room_type, room_number, price))
                self.conn.commit()

                messagebox.showinfo("Booking Successful", f"Room {room_number} booked successfully!")
                self.destroy()
            else:
                messagebox.showerror("Error", "Failed to book the room.")
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter valid information for all fields.")
        except Exception as e:
            messagebox.showerror("Error", str(e))
        self.destroy()

if __name__ == "__main__":
    app = checkin_form()
    app.mainloop()
