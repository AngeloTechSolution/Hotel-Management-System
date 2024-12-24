import tkinter as tk
from tkinter import messagebox, Toplevel
import sqlite3

class RoomSelectionWindow:
    def __init__(self, parent, room_type):
        self.window = Toplevel(parent)
        self.window.geometry('400x300')
        self.window.title(f'Select {room_type} Room')

        self.room_type = room_type
        self.available_rooms = self.get_available_rooms(room_type)
        self.parent = parent  # Reference to parent window to pass selected data

        self.room_listbox = tk.Listbox(self.window, height=10, width=50)
        self.room_listbox.pack(pady=20)

        self.update_room_list()

        tk.Button(self.window, text="Select Room", command=self.select_room).pack(pady=10)
        tk.Button(self.window, text="Close", command=self.window.destroy).pack(pady=10)

    def get_available_rooms(self, room_type):
        """
        Fetch available rooms from the database based on the room type.
        """
        connection = sqlite3.connect("system.db")
        cursor = connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Rooms (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                room_number TEXT UNIQUE,
                room_type TEXT,
                is_occupied INTEGER DEFAULT 0
            )
        """)  # Ensure the Rooms table exists
        connection.commit()

        # Fetch available rooms for the specified room type
        cursor.execute("""
            SELECT room_number FROM Rooms WHERE room_type = ? AND is_occupied = 0
        """, (room_type,))
        rooms = [row[0] for row in cursor.fetchall()]
        connection.close()
        return rooms

    def update_room_list(self):
        """
        Refresh the room list displayed in the listbox.
        """
        self.room_listbox.delete(0, tk.END)
        for room in self.available_rooms:
            self.room_listbox.insert(tk.END, room)

    def select_room(self):
        """
        Mark the selected room as occupied in the database and update the UI.
        """
        selected_room = self.room_listbox.get(tk.ACTIVE)
        if selected_room:
            # Mark the room as occupied in the database
            connection = sqlite3.connect("system.db")
            cursor = connection.cursor()
            cursor.execute("""
                UPDATE Rooms SET is_occupied = 1 WHERE room_number = ?
            """, (selected_room,))
            connection.commit()
            connection.close()

            # Remove the room from the available list and update the UI
            self.available_rooms.remove(selected_room)
            self.update_room_list()

            # Pass the selected room number back to the parent window
            self.parent.selected_room_number = selected_room
            messagebox.showinfo("Room Selected", f"Room {selected_room} has been booked.")
            self.window.destroy()
        else:
            messagebox.showwarning("Select Room", "Please select a valid available room.")
