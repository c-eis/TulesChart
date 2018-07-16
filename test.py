from tkinter import *
from PIL import Image, ImageTk

master = Tk()

chart = Canvas(master, width=600, height=600)
chart.pack()

image = Image.open("initial.png")
initial_image = ImageTk.PhotoImage(image)
h = ImageTk.PhotoImage(image).height()
w = ImageTk.PhotoImage(image).width()
chart.create_image((600,600),image=initial_image)

mainloop()