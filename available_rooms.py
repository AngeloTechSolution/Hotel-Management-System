import tkinter as tk
from tkinter import ttk
import sqlite3


class AvailableRooms(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry('1000x700')
        self.title('Hotel Management System')

        # Header Frame
        self.head_frame = tk.Frame(self, width=1000, height=80, bg='blue')
        self.head_label = tk.Label(self.head_frame, text="Available Rooms", font=('New Times Roman', 30, 'bold italic'),
                                   fg='white', bg='blue')

        self.head_label.pack(pady=20)
        self.head_frame.propagate(False)
        self.head_frame.pack()

        # Filter Frame for Dropdown Menu
        self.filter_frame = tk.Frame(self, width=1000, height=50, bg='blue')
        self.filter_frame.pack(pady=20)

        # Room Type Dropdown
        self.room_types = ['All', 'Deluxe', 'General', 'Joint']
        self.room_type_combobox = ttk.Combobox(self.filter_frame, values=self.room_types, state="readonly", width=20)
        self.room_type_combobox.set('All')  # Default to 'All'
        self.room_type_combobox.bind('<<ComboboxSelected>>', self.populate_data)  # Trigger data population on selection
        self.room_type_combobox.pack()

        # Treeview for displaying room information
        self.columns = ("room_type", "room_number", "availability")
        self.tree = ttk.Treeview(self, columns=self.columns, show="headings", height=15)
        self.tree.pack(pady=20, fill="both", expand=True)

        # Define Treeview Column Headings
        self.tree.heading("room_type", text="Room Type")
        self.tree.heading("room_number", text="Room Number")
        self.tree.heading("availability", text="Availability")

        # Adjust column widths
        self.tree.column("room_type", width=150)
        self.tree.column("room_number", width=150)
        self.tree.column("availability", width=100)

        # Scrollbar for Treeview
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=self.scrollbar.set)
        self.scrollbar.pack(side="right", fill="y")

        # Initially populate data
        self.populate_data()

    def populate_data(self, event=None):
        """Fetch rooms from the database and populate the Treeview based on selected room type."""
        conn = sqlite3.connect('system.db')
        cursor = conn.cursor()

        # Get the selected room type from the dropdown
        selected_type = self.room_type_combobox.get()

        # Construct the SQL query based on the selected room type
        if selected_type == 'All':
            query = """
                SELECT room_type, room_number, 
                CASE WHEN available = 1 THEN 'Available' ELSE 'Not Available' END AS availability
                FROM rooms
            """
        else:
            query = """
                SELECT room_type, room_number, 
                CASE WHEN available = 1 THEN 'Available' ELSE 'Not Available' END AS availability
                FROM rooms WHERE room_type = ?
            """
            cursor.execute(query, (selected_type,))
            rows = cursor.fetchall()

        # Clear any existing data in the Treeview
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Execute the query and populate the Treeview with the results
        if selected_type == 'All':
            cursor.execute(query)
            rows = cursor.fetchall()

        for row in rows:
            self.tree.insert("", "end", values=row)

        conn.close()


if __name__ == "__main__":
    root = AvailableRooms()
    root.mainloop()
