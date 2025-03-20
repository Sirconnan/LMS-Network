#!/bin/python
import socket, sys, threading, psutil, time
from server import Server
from tkinter import * 
from tkinter.messagebox import * 


class stdout_redirector: # ====> Create class for redirect the stdout flux
    # => This class replace the method sys.stdout because the function print() is
    # a compat of sys.stdout.write. So we rempalce sys.stdout with this class for
    # redirect the flux in Tkinter text widget

    def __init__(self, text_widget): # ====> Init the object whit the Tkinter text widget
        self.text_widget = text_widget

    def write(self, message): # ====> Override the method write for write in the Tkinter text widget
        self.text_widget.insert(END, message) # => Insert at the end of the object text
        self.text_widget.see(END) # => Scroll a the end automatically 
    
    def flush(self): # ====> For app use the method sys.stdout.flush
        pass

class Interface:

    __IP = socket.gethostbyname(socket.gethostname())
    __NB_SERVER = 0

    def __init__(self, width:int = 100, height:int = 100, text:str = "Server"):
        self.gui = Tk()
        self.gui.geometry(f"{width}x{height}")
        self.gui.configure(bg='gray25')
        self.gui.title(text)


    def run(self):
        try:
            self.gui.mainloop()
        except KeyboardInterrupt:
            self.gui.quit()
            exit()
    
    def create_server(self):
        if Interface.__NB_SERVER >= 5:
            showinfo("Limit reached", "The max number of server is reached. (5 max)")
            return
        
        Interface.__NB_SERVER += 1

        server_gui = Toplevel(self.gui)
        server_gui.configure(bg='gray25')
        server_gui.geometry("1000x400")

        Label(server_gui, text="IP of the server").pack()
        ip_input = Entry(server_gui)
        ip_input.pack()
        ip_input.insert(0, Interface.__IP)

        Label(server_gui, text="Port of the server").pack()
        port_input = Spinbox(server_gui, from_=1024, to=65535)
        port_input.pack()
        
        Button(server_gui, text="Start server", command=lambda: Interface.start_server(ip_input, port_input, server_gui)).pack()
    
    @staticmethod
    def start_server(ip_input, port_input, server_gui):
        ip = ip_input.get()
        port = port_input.get()

        connection = psutil.net_connections(kind="inet") # => 
        list_open_port = {conn.laddr.port for conn in connection}

        octets = ip.split(".")

        if not (len(octets) == 4 and all(o.isdigit() and 0 <= int(o) <= 255 for o in octets)):
            showerror("Error IP", "Invalid format the IP. Expected format : \"127.0.0.1\"")
            return
        
        if not port.isdigit():
            showerror("Error Port", "Invalid format the port. Expected format : \"52152\"")
            return
        
        port = int(port)

        if not 1024 <= port <= 65535:
            showerror("Error Port", "Invalid port. Expected range : [1024-65535]")
            return
        
        if port in list_open_port:
            showerror("Error Port", "Port already used")
            return

        if askyesno("Checking information", f"Are you sure of connect information:\n- IP: {ip}\n- Port: {port}"):
            for widget in server_gui.winfo_children():
                widget.destroy()
            
            Label(server_gui, text=f"Server started at {ip} on port {port}").pack()

            frame_stdout_server = Frame(server_gui)
            frame_stdout_server.pack(fill=BOTH, expand=True)

            text_stdout_server = Text(frame_stdout_server, wrap="word", height=10, width=50)
            text_stdout_server.pack(fill=BOTH, expand=True)

            stdout_redirector_server = stdout_redirector(text_stdout_server)
            sys.stdout = stdout_redirector_server # => Remplace the method of sys

            server_i = Server(ip, port)

            thread_server = threading.Thread(target=lambda: server_i.Run_server(), daemon=True) # => Use trhead beacause the method Run_server bloc the TKinter instance
            thread_server.start()

            Button(server_gui, text="Stop Server", command=lambda: Interface.stop_server(thread_server, server_gui, server_i)).pack(side="top")
            server_gui.protocol("WM_DELETE_WINDOW", lambda: Interface.stop_server(thread_server, server_gui, server_i))

    @staticmethod
    def stop_server(thread_server, server_gui, server_i):
        server_i.thread_etat = False
        thread_server.join()
        server_gui.destroy()
        Interface.__NB_SERVER -= 1
    
tmp = Interface(500, 500, "Server App")

Button(tmp.gui, text="New server", command=tmp.create_server).pack()

frame_stdout_main = Frame(tmp.gui)
frame_stdout_main.pack(fill=BOTH, expand=True)

text_stdout_main = Text(frame_stdout_main, wrap="word", height=10, width=50)
text_stdout_main.pack(fill=BOTH, expand=True)

stdout_redirector_main = stdout_redirector(text_stdout_main)
sys.stdout = stdout_redirector_main
sys.stderr = stdout_redirector_main

tmp.run()