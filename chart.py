from tkinter import *
from PIL import Image, ImageTk
from tkinter.filedialog import askopenfilename, asksaveasfilename
import network
 
def gui_save_network():
    global network
    fname = asksaveasfilename() 
    network = network.save(fname)
   
def gui_draw_network():
    global network
    network.draw_network()
    info_label.config(text=network.name)
    image = Image.open("chart.png")
    h = ImageTk.PhotoImage(image).height()
    w = ImageTk.PhotoImage(image).width()
    #new_chart_label= Label(master=window, image=chart_image)
    #new_chart_label.place(x=110, y=160, width=w, height=h)
    new_height = window.winfo_screenheight()- 180
    new_width  = int(new_height * w / h)
    image = image.resize((new_width, new_height), Image.ANTIALIAS)
    chart_image = ImageTk.PhotoImage(image)
    #chart_canvas.create_image((100,250),image=chart_image)

    chart_label.config(image=chart_image)
    chart_label.image = chart_image
    #new_chart_label.pack()
    
def gui_load_network():
    global network
    fname = askopenfilename() 
    network = load_network(fname)
    info_label.config(text=network.name)
    
    
def gui_new_network():
    def gui_new_network_create():
        name = e_name.get()
        global network
        network = Network(name)
        info_label.config(text=network.name)
        new_network_window.destroy()
    new_network_window = Toplevel()
    new_network_window.title('Neues Netzwerk')
    new_network_window.geometry('160x160')
    l_name = Label(new_network_window, text='Name des neuen Netzwerks')
    e_name = Entry(new_network_window)
    b_create = Button(new_network_window, text='Erstellen', command=gui_new_network_create)
    l_name.pack()
    e_name.pack()
    b_create.pack()

def gui_new_member():
    def gui_new_member_create():
        member = e_name.get()
        global network
        network.add_member(member)
        new_member_window.destroy()
    new_member_window = Toplevel()
    new_member_window.title('Neue Person')
    new_member_window.geometry('160x160')
    l_name = Label(new_member_window, text='Name der neuen Person')
    e_name = Entry(new_member_window)
    b_create = Button(new_member_window, text='Erstellen', command=gui_new_member_create)
    l_name.pack()
    e_name.pack()
    b_create.pack()
    
def gui_new_connection():
    def gui_new_connection_create():
        #member1 = listbox1.curselection()
        items1 = listbox1.curselection()
        try:
            items1 = map(int, items1)
        except ValueError: pass
        items1 = map(lambda i,d=self.data: d[i], items1)
        member2 = listbox2.curselection()
        global network
        network.add_connection([member1,member2])
        new_connection_window.destroy()
        
    new_connection_window = Toplevel()
    new_connection_window.title('Neue Verbindung')
    new_connection_window.geometry('600x300')
    
    l_name1 = Label(new_connection_window, text='Person 1')
    l_name2 = Label(new_connection_window, text='Person 2')
    
    b_create = Button(new_connection_window, text='Erstellen', command=gui_new_connection_create)
    s1 = Scrollbar(new_connection_window)
    s2 = Scrollbar(new_connection_window)

    listbox1 = Listbox(new_connection_window)
    for item in network.members():
        listbox1.insert(END, item)
    listbox2 = Listbox(new_connection_window)
    for item in network.members():
        listbox2.insert(END, item)
        
    l_name1.pack(side=LEFT)
    listbox1.pack(side=LEFT)    
    s1.pack(side=LEFT)
    l_name2.pack(side=LEFT)
    listbox2.pack(side=LEFT)
    s2.pack(side=LEFT)
    b_create.pack(side=LEFT)
    
    s1['command'] = listbox1.yview
    listbox1['yscrollcommand'] = s1.set
    s2['command'] = listbox2.yview
    listbox2['yscrollcommand'] = s2.set
    

def gui_combine_networks():
    global network
    fname = askopenfilename() 
    network2 = load_network(fname)
    for i in network2.connections():
        network.add_connection(i)
    info_label.config(text=network.name)

global network
network = Network('Leer',{})
#network.draw_network()

#network = create_HGW_network()
#network.draw_network()
#print("New network")
#network.save()
#new_network = load_network('HGW')
#print(new_network)

# Create Window
window = Tk()
window.title('Tules Chart')
#window.geometry('600x600')
window.geometry("{0}x{1}+0+0".format(window.winfo_screenwidth(), window.winfo_screenheight()))

# Images
img_h = window.winfo_screenheight()- 180
# initial image
image = Image.open("initial.png")
h = ImageTk.PhotoImage(image).height()
w = ImageTk.PhotoImage(image).width()
new_height = img_h
new_width  = int(new_height * w / h)
image = image.resize((new_width, new_height), Image.ANTIALIAS)
initial_image = ImageTk.PhotoImage(image)
# chart image
image = Image.open("chart.png")
h = ImageTk.PhotoImage(image).height()
w = ImageTk.PhotoImage(image).width()
new_height = img_h
new_width  = int(new_height * w / h)
image = image.resize((new_width, new_height), Image.ANTIALIAS)
chart_image = ImageTk.PhotoImage(image)

#chart_canvas = Canvas(window, width=400, height=400)
chart_label = Label(master=window, image=initial_image)
chart_label.place(x=110, y=160, width=new_width, height=img_h)


#Create Buttons and Labels
exit_button = Button(window, text='Beenden', command=window.quit)
info_label = Label(window, text=network.name)
load_button = Button(window, text='Chart Laden', command=gui_load_network)
save_button = Button(window, text='Chart Speichern', command=gui_save_network)
draw_button = Button(window, text='Zeichnen', command=gui_draw_network)
new_network_button = Button(window, text='Erstelle neues Netzwerk', command=gui_new_network)
new_member_button = Button(window, text='Fuege neue Person hinzu', command=gui_new_member)
new_connection_button = Button(window, text='Fuege neue Verbindung hinzu', command=gui_new_connection)
combine_networks_button = Button(window, text='Verbinde Netzwerke', command=gui_combine_networks)

# Load Buttons in Window
#chart_canvas.pack()
chart_label.pack()
info_label.pack()
load_button.pack(side=LEFT)
new_network_button.pack(side=LEFT)
save_button.pack(side=LEFT)
draw_button.pack(side=LEFT)
new_member_button.pack(side=LEFT)
new_connection_button.pack(side=LEFT)
combine_networks_button.pack(side=LEFT)
exit_button.pack(side=LEFT) 

#chart_canvas.create_image((100,250),image=initial_image)

# Wait for user command
window.mainloop()


    
