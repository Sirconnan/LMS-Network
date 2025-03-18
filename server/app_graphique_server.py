#!/bin/python
import socket
from server import Server
from tkinter import * 
from tkinter.messagebox import * 

class Interface:
    __ip = socket.gethostbyname(socket.gethostname())
    __nb_server = 0

    def __init__(self, width, height):
        self.gui = Tk()
        self.gui.geometry(f"{width}x{height}")
        self.gui.configure(bg='gray25')


    def run(self):
        try:
            self.gui.mainloop()
        except KeyboardInterrupt:
            self.gui.quit()
            exit()
    
    def new_server():
        Interface.__nb_server += 1
                
        server_gui = Interface(900,900)

        Label(server_gui.gui, text="IP of the server").pack()
        ip_input = Entry(server_gui.gui, validate="key", validatecommand=())
        ip_input.pack()
        ip_input.delete(0, END)
        ip_input.insert(0, Interface.__ip)

        Label(server_gui.gui, text="Port of the server").pack()
        port_input = Spinbox(server_gui.gui, from_=49152, to=65535)
        port_input.pack()

        server_gui.run()

        # ip = ip_input.get()
        # port = int(port_input.get())



tmp = Interface(1000, 1000)

Button(tmp.gui, text="New server", command=Interface.new_server).pack()

tmp.run()