import tkinter as tk
from checkin_form import checkin_form
from checkout import Checkout
from guestList import GuestList
from available_rooms import AvailableRooms

class main(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry('1200x700')
        self.config(bg='#D2CECE')
        self.title('Hotel Management System')

        #Left and right container
        self.left_canvas = tk.Canvas(self, width=600, height=700)
        self.right_frame = tk.Frame(self, width=600, height=700, bg='#D2CECE')

        self.left_canvas.place(x=0, y=0)
        self.right_frame.place(x=600, y=0)

        #left canvas content
        self.left_img = tk.PhotoImage(file='C:\\Users\\Senpai\\PycharmProjects\\pythonExercise\\Codechum tkinter\\Hotel Management System\\images\\pexels-michael-block-1691617-3225531.png')
        self.left_canvas.create_image(300, 300, image=self.left_img, anchor='center')

        #right content
        self.right_label = tk.Label(self.right_frame, text="LUXURY GRANDE\nHOTEL", font=('New Times Roman', 30, 'bold italic'), bg='#D2CECE')
        self.right_label.pack(pady=50, padx=120)

        self.catchPhrase = tk.Label(self.right_frame, text='"Where Elegance Meets Comfort, Every Stay is a Grand Experience."',
                                    font=('New Times Roman', 10, 'normal italic'), bg='#D2CECE')
        self.catchPhrase.pack(pady=0)

        self.btn_frame = tk.Frame(self.right_frame, width=400, height=400, bg='#D2CECE')
        self.btn_frame.pack(pady=50, padx=20)

        self.check_in_btn = tk.Button(self.btn_frame, text='Check In',
                                      width=50, height=2, bg='#E5E4E4', font=('arial', 10, 'bold'),
                                      command=self.check_in)

        self.check_out_btn = tk.Button(self.btn_frame, text="Check Out",
                                       width=50, height=2, bg='#E5E4E4', font=('arial', 10, 'bold'),
                                       command=self.check_out)

        self.guest_list_btn = tk.Button(self.btn_frame, text="Show Guest List",
                                        width=50, height=2, bg='#E5E4E4', font=('arial', 10, 'bold'),
                                        command=self.guest_list)

        self.guest_info_btn = tk.Button(self.btn_frame, text='Available Rooms', width=50,
                                        height=2, bg='#E5E4E4', font=('arial', 10, 'bold'),
                                        command=self.available_rooms)

        self.exit_btn = tk.Button(self.btn_frame, text='Exit',
                                  width=50, height=2,bg='#E5E4E4', font=('arial', 10, 'bold'),
                                  command=self.exit)

        self.check_in_btn.pack()
        self.check_out_btn.pack(pady=10)
        self.guest_list_btn.pack(pady=10)
        self.guest_info_btn.pack(pady=10)
        self.exit_btn.pack(pady=10)

    def check_in(self):
        checkin_form()

    def check_out(self):
        Checkout()

    def guest_list(self):
        GuestList()

    def available_rooms(self):
        AvailableRooms()

    def exit(self):
        self.destroy()


if __name__ == "__main__":
    root = main()
    root.mainloop()
