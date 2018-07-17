from tkinter import *
from PIL import Image, ImageTk
from tkinter.filedialog import askopenfilename, asksaveasfilename
from network import *

def gui_save_network():
    '''saves a network in a file (callback function of save_button)'''
    global network
    fname = asksaveasfilename() 
    network.save(fname)
   
   
def gui_show_network():
    '''draws a network using networkx and matplotlib and shows it(callback function of draw_button)'''
    global network
    network.show_network()
    info_label.config(text=network.name)
    image = Image.open("chart.png")
    h = ImageTk.PhotoImage(image).height()
    w = ImageTk.PhotoImage(image).width()
    new_height = window.winfo_screenheight()- 130
    new_width  = int(new_height * w / h)
    image = image.resize((new_width, new_height), Image.ANTIALIAS)
    chart_image = ImageTk.PhotoImage(image)
    chart_label.config(image=chart_image)
    chart_label.image = chart_image

    
def gui_draw_network():
    '''draws a network using networkx and matplotlib (callback function of draw_button)'''
    global network
    network.draw_network()
    info_label.config(text=network.name)
    image = Image.open("chart.png")
    h = ImageTk.PhotoImage(image).height()
    w = ImageTk.PhotoImage(image).width()
    new_height = window.winfo_screenheight()- 130
    new_width  = int(new_height * w / h)
    image = image.resize((new_width, new_height), Image.ANTIALIAS)
    chart_image = ImageTk.PhotoImage(image)
    chart_label.config(image=chart_image)
    chart_label.image = chart_image    
   
   
def gui_load_network():
    '''loads a network from a file (callback function of load_button)'''
    global network
    fname = askopenfilename() 
    network = load_network(fname)
    info_label.config(text=network.name)
    names_box.delete(0,names_box.size())
    for item in sorted(network.members()):
        names_box.insert(END, item) 
    gui_draw_network()

    
def gui_load_new():
    '''loads a new network from a textfile (callback function of load_new_button'''
    def gui_load_new_create():
        fname = askopenfilename()
        name = e_name.get()
        global network
        network = load_from_txt(fname, name)
        info_label.config(text=network.name)
        names_box.delete(0,names_box.size())
        for item in sorted(network.members()):
            names_box.insert(END, item) 
        load_new_window.destroy()
        gui_draw_network()
        
    load_new_window = Toplevel()
    load_new_window.title('Neues Netzwerk')
    load_new_window.geometry('160x160')
    l_name = Label(load_new_window, text='Name des neuen Netzwerks')
    e_name = Entry(load_new_window)
    b_create = Button(load_new_window, text='Erstellen', command=gui_load_new_create)
    l_name.pack()
    e_name.pack()
    b_create.pack()    
    
    
def gui_new_network():
    '''creates a window to create a new empty network (callback function of new_network_button)'''
    def gui_new_network_create():
        '''creates a new empty network (callback function b_create)'''
        name = e_name.get()
        global network
        network = Network(name)
        info_label.config(text=network.name)
        names_box.delete(0,names_box.size())
        for item in sorted(network.members()):
            names_box.insert(END, item) 
        new_network_window.destroy()
        gui_draw_network()
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
    '''creates a window to create a new network member (callback function of new_member_button)'''
    def gui_new_member_create():
        '''creates a new network member (callback function of b_create)'''
        member = e_name.get()
        global network
        network.add_member(member)
        names_box.delete(0,names_box.size())
        for item in sorted(network.members()):
            names_box.insert(END, item)    
        new_member_window.destroy()
        gui_draw_network()
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
    '''creates a window to create a new connection in the network (callback function of new_connection_button)'''
    def gui_new_connection_create():
        '''creates a new connection (callback function of b_create)'''
        member1 = listbox1.get(ACTIVE)
        member2 = listbox2.get(ACTIVE)
        global network
        network.add_connection([member1,member2])        
        gui_draw_network()
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
    for item in sorted(network.members()):
        listbox1.insert(END, item)
    listbox2 = Listbox(new_connection_window)
    for item in sorted(network.members()):
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
    '''loads another network and combines it with the actuall network (callback function of combine_networks_button)'''
    global network
    fname = askopenfilename() 
    network2 = load_network(fname)
    for i in network2.connections():
        network.add_connection(i)
    info_label.config(text=network.name)
    names_box.delete(0,names_box.size())
    for item in sorted(network.members()):
        names_box.insert(END, item) 
    gui_draw_network()

    
def gui_delete_connection():
    '''creates a window to delete a connection in the network (callback function of delete_connection_button)'''
    def gui_delete_connection_ok():
        '''deletes a connection (callback function of b_delete)'''
        member1 = listbox1.get(ACTIVE)
        member2 = listbox2.get(ACTIVE)
        global network
        network.delete_connection([member1,member2])
        delete_connection_window.destroy()
        gui_draw_network()
        
    delete_connection_window = Toplevel()
    delete_connection_window.title('Lösche Verbindung')
    delete_connection_window.geometry('600x300')
    
    l_name1 = Label(delete_connection_window, text='Person 1')
    l_name2 = Label(delete_connection_window, text='Person 2')
    
    b_delete = Button(delete_connection_window, text='Löschen', command=gui_delete_connection_ok)
    s1 = Scrollbar(delete_connection_window)
    s2 = Scrollbar(delete_connection_window)

    listbox1 = Listbox(delete_connection_window)
    for item in sorted(network.members()):
        listbox1.insert(END, item)
    listbox2 = Listbox(delete_connection_window)
    for item in sorted(network.members()):
        listbox2.insert(END, item)
        
    l_name1.pack(side=LEFT)
    listbox1.pack(side=LEFT)    
    s1.pack(side=LEFT)
    l_name2.pack(side=LEFT)
    listbox2.pack(side=LEFT)
    s2.pack(side=LEFT)
    b_delete.pack(side=LEFT)
    
    s1['command'] = listbox1.yview
    listbox1['yscrollcommand'] = s1.set
    s2['command'] = listbox2.yview
    listbox2['yscrollcommand'] = s2.set
    

def gui_delete_member():
    '''creates a window to delete a memer of the network (callback function of delete_connection_button)'''
    def gui_delete_member_ok():
        '''deletes a connection (callback function of b_delete)'''
        member = listbox.get(ACTIVE)
        id = listbox.index(ACTIVE)
        global network
        network.delete_member(member)
        names_box.delete(id)
        delete_member_window.destroy()
        gui_draw_network()
        
    global network
    delete_member_window = Toplevel()
    delete_member_window.title('Lösche Person')
    delete_member_window.geometry('600x300')
    
    l_name = Label(delete_member_window, text='Name')
    
    b_delete = Button(delete_member_window, text='Löschen', command=gui_delete_member_ok)
    s = Scrollbar(delete_member_window)

    listbox = Listbox(delete_member_window)
    for item in sorted(network.members()):
        listbox.insert(END, item)
    
    l_name.pack(side=LEFT)
    listbox.pack(side=LEFT)    
    s.pack(side=LEFT)
    b_delete.pack(side=LEFT)
    
    s['command'] = listbox.yview
    listbox['yscrollcommand'] = s.set
    
    
def gui_rename():
    '''creates a window to rename a memer of the network (callback function of rename_button)'''
    def gui_rename_ok():
        '''renames a member (callback function of b_rename)'''
        member = listbox.get(ACTIVE)
        new_member = e_name.get()
        global network
        network.rename_member(member, new_member)
        names_box.delete(0,names_box.size())
        for item in sorted(network.members()):
            names_box.insert(END, item) 
        rename_window.destroy()
        gui_draw_network()
        
    rename_window = Toplevel()
    rename_window.title('Bennene Person um')
    rename_window.geometry('600x300')
    
    l_name1 = Label(rename_window, text='Alter Name')
    l_name2 = Label(rename_window, text='Neuer Name')
    e_name = Entry(rename_window)
    b_rename = Button(rename_window, text='Umbenennen', command=gui_rename_ok)
    s = Scrollbar(rename_window)

    listbox = Listbox(rename_window)
    for item in sorted(network.members()):
        listbox.insert(END, item)
    
    l_name1.pack(side=LEFT)
    listbox.pack(side=LEFT)    
    s.pack(side=LEFT)
    l_name2.pack(side=LEFT)
    e_name.pack(side=LEFT)
    b_rename.pack(side=LEFT)
    
    s['command'] = listbox.yview
    listbox['yscrollcommand'] = s.set
    
### MAIN ###    
global network
network = Network('Leer',{})
#network.draw_network()

#network = create_HGW_network()
#network.draw_network()


# Create Window
window = Tk()
window.title('Tules Chart')
#window.geometry('600x600')
window.geometry("{0}x{1}+0+0".format(window.winfo_screenwidth(), window.winfo_screenheight()))

# Images
img_h = window.winfo_screenheight()- 130
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

chart_label = Label(master=window, image=initial_image)
chart_label.place(x=110, y=160, width=new_width, height=img_h)


#Create Buttons and Labels
exit_button = Button(window, text='Beenden', command=window.quit)
info_label = Label(window, text=network.name)
load_button = Button(window, text='Chart laden', command=gui_load_network)
load_new_button = Button(window, text='Chart aus .txt erstellen', command=gui_load_new)
save_button = Button(window, text='Chart speichern', command=gui_save_network)
draw_button = Button(window, text='Chart zeichnen', command=gui_show_network)
new_network_button = Button(window, text='Chart erstellen', command=gui_new_network)
new_member_button = Button(window, text='Person erstellen', command=gui_new_member)
new_connection_button = Button(window, text='Verbindung erstellen', command=gui_new_connection)
combine_networks_button = Button(window, text='Charts verbinden', command=gui_combine_networks)
delete_connection_button = Button(window, text='Verbindung löschen', command=gui_delete_connection)
delete_member_button = Button(window, text='Person löschen', command=gui_delete_member)
rename_button = Button(window, text='Person umbenennen', command=gui_rename)
names_box = Listbox(window, height=3)
for item in sorted(network.members()):
        names_box.insert(END, item)
s = Scrollbar(window)
s['command'] = names_box.yview
names_box['yscrollcommand'] = s.set
        
        
# Load Buttons in Window

chart_label.pack()
info_label.pack()
names_box.pack(side=LEFT)
s.pack(side=LEFT)
load_button.pack(side=LEFT)
load_new_button.pack(side=LEFT)
new_network_button.pack(side=LEFT)
save_button.pack(side=LEFT)
draw_button.pack(side=LEFT)
new_member_button.pack(side=LEFT)
new_connection_button.pack(side=LEFT)
rename_button.pack(side=LEFT)
combine_networks_button.pack(side=LEFT)
delete_connection_button.pack(side=LEFT)
delete_member_button.pack(side=LEFT)
exit_button.pack(side=LEFT) 


# Wait for user command
window.mainloop()

    
