import tkinter as tk
from tkinter import ttk
import sqlite3

class GuestList(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.geometry('1000x700')
        self.config(bg='#CFCDCD')
        self.title("Hotel Management System")

        # Header Frame
        self.head_frame = tk.Frame(self, width=1000, height=100, bg='blue')
        self.head_label = tk.Label(self.head_frame, text="Guest List", font=('New Times Roman', 30, 'bold italic'), fg='white', bg='blue')
        self.head_frame.propagate(False)
        self.head_frame.pack()
        self.head_label.pack(pady=20)

        self.option_frame = tk.Frame(self, width=100, bg='#CFCDCD')
        self.option_frame.pack()

        self.dropdown_label = tk.Label(self.option_frame, text="Select Room:", font=('arial', 10, 'bold'), bg='#CFCDCD')
        self.dropdown_label.grid(row=0, column=0, pady=30)

        # Room type options for the combobox
        self.room_options = ["All", "Deluxe", "General", "Joint"]

        # Combobox for selecting room type
        self.room_combobox = ttk.Combobox(self.option_frame, values=self.room_options, state="readonly", width=20)
        self.room_combobox.set("All")  # Default to "All"
        self.room_combobox.grid(row=0, column=1, padx=10)
        self.room_combobox.bind("<<ComboboxSelected>>", self.filter_data)  # Bind selection event

        # Treeview Table
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

        # Populate Table with Data
        self.populate_data()

    def populate_data(self):
        """Fetch data from the database and populate the Treeview."""
        conn = sqlite3.connect('system.db')
        cursor = conn.cursor()

        # Fetch all guest data
        cursor.execute("SELECT name, address, phone, days, room_type, room_number, price FROM bookings")  # Updated query
        rows = cursor.fetchall()

        # Clear any existing data in the Treeview
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Insert data into the Treeview
        for row in rows:
            self.tree.insert("", "end", values=row)

        conn.close()

    def filter_data(self, event=None):
        """Filter the Treeview data based on the selected room type."""
        selected_option = self.room_combobox.get()  # Get selected room type

        conn = sqlite3.connect('system.db')
        cursor = conn.cursor()

        # Query based on the selected room type
        if selected_option == "All":
            cursor.execute("SELECT name, address, phone, days, room_type, room_number, price FROM bookings")
        else:
            cursor.execute(
                "SELECT name, address, phone, days, room_type, room_number, price FROM bookings WHERE room_type = ?",
                (selected_option,)
            )
        rows = cursor.fetchall()

        # Clear the Treeview
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Insert filtered data
        for row in rows:
            self.tree.insert("", "end", values=row)

        conn.close()

if __name__ == "__main__":
    root = GuestList()
    root.mainloop()
