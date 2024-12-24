import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import sqlite3

class Checkout(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry('1000x700')
        self.config(bg='#CFCDCD')
        self.title('Hotel Management System')

        # Initialize Database
        self.init_db()

        # Head Frame
        self.top_frame = tk.Frame(self, width=1000, height=80, bg='blue')
        self.top_label = tk.Label(self.top_frame, text="Checkout", font=('New Times Roman', 30, 'bold italic'), fg='white', bg='blue')
        self.top_label.pack(pady=10)
        self.top_frame.pack()
        self.top_frame.propagate(False)

        # Middle Frame for Room Entry and Lookup Button
        self.middle_frame = tk.Frame(self, width=100, bg='#CFCDCD')
        self.middle_frame.pack(pady=20)

        self.room_label = tk.Label(self.middle_frame, text='Room #:', font=('arial', 15), bg='#CFCDCD')
        self.room_label.grid(row=0, column=0, padx=20, pady=10)

        self.room_entry = tk.Entry(self.middle_frame)
        self.room_entry.grid(row=0, column=1, padx=20, pady=10)

        self.lookup_btn = tk.Button(self.middle_frame, text="Lookup", font=('arial', 12), bg='blue', fg='white', width=10, command=self.lookup_booking)
        self.lookup_btn.grid(row=0, column=2, padx=20, pady=10)

        # Treeview Table for Checkout Details
        self.columns = ("name", "address", "phone", "days", "room_type", "room_number", "price")
        self.tree = ttk.Treeview(self, columns=self.columns, show='headings', height=15)
        self.tree.pack(pady=20, fill="both", expand=True)

        # Define Treeview Column Headings
        self.tree.heading("name", text="Name")
        self.tree.heading("address", text="Address")
        self.tree.heading("phone", text="Phone")
        self.tree.heading("days", text="Days")
        self.tree.heading("room_type", text="Room Type")
        self.tree.heading("room_number", text="Room No")
        self.tree.heading("price", text="Price (₱)")

        # Adjust column widths
        self.tree.column("name", width=150)
        self.tree.column("address", width=200)
        self.tree.column("phone", width=100)
        self.tree.column("days", width=50)
        self.tree.column("room_type", width=100)
        self.tree.column("room_number", width=50)
        self.tree.column("price", width=100)

        # Scrollbar for Treeview
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=self.scrollbar.set)
        self.scrollbar.pack(side="right", fill="y")

        # Checkout Button at the Bottom
        self.checkout_btn = tk.Button(self, text="Checkout", font=('arial', 12), bg='green', fg='white', width=20, command=self.checkout)
        self.checkout_btn.pack(pady=20)

    def init_db(self):
        """Initialize the SQLite database."""
        self.conn = sqlite3.connect('system.db')
        self.cursor = self.conn.cursor()

        # Create bookings table if it doesn't exist
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

        # Create rooms table if it doesn't exist
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS rooms (
            room_number TEXT PRIMARY KEY,
            available INTEGER
        )''')

        self.conn.commit()

    def lookup_booking(self):
        """Look up booking details by room number and display in the Treeview."""
        room_number = self.room_entry.get().strip()

        if not room_number:
            messagebox.showwarning("Input Error", "Please enter a room number.")
            return

        self.cursor.execute('''SELECT name, address, phone, days, room_type, room_number, price
                               FROM bookings WHERE room_number = ?''', (room_number,))
        booking_details = self.cursor.fetchone()

        if booking_details:
            for item in self.tree.get_children():
                self.tree.delete(item)

            self.tree.insert("", "end", values=booking_details)
        else:
            messagebox.showerror("Error", f"No booking found for room {room_number}.")

    def checkout(self):
        """Handle the checkout process."""
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("No Selection", "Please select a booking from the table.")
            return

        selected_item = selected_item[0]
        selected_data = self.tree.item(selected_item)['values']
        name = selected_data[0]
        room_number = selected_data[5]

        try:
            self.cursor.execute('''DELETE FROM bookings WHERE room_number = ?''', (room_number,))
            self.conn.commit()

            self.cursor.execute('''UPDATE rooms SET available = 1 WHERE room_number = ?''', (room_number,))
            self.conn.commit()

            self.tree.delete(selected_item)

            messagebox.showinfo("Checkout",
                                f"Checkout successful for {name} (Room No: {room_number}). Room is now available.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred during checkout: {str(e)}")

        self.destroy()

    def destroy(self):
        """Close the database connection and the window."""
        self.conn.close()
        super().destroy()

if __name__ == "__main__":
    app = Checkout()
    app.mainloop()