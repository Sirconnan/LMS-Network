#!/bin/python
import socket, sys, threading
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

class Interface:

    __ip_list_use = []
    __ip = socket.gethostbyname(socket.gethostname())
    __nb_server = 0

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
    
    def new_server(self):
        if Interface.__nb_server >= 5:
            showinfo("Limit reached", "The max number of server is reached. (5 max)")
            return
        
        Interface.__nb_server += 1

        server_gui = Toplevel(self.gui)
        server_gui.configure(bg='gray25')

        Label(server_gui, text="IP of the server").pack()
        ip_input = Entry(server_gui)
        ip_input.pack()
        ip_input.insert(0, Interface.__ip)

        Label(server_gui, text="Port of the server").pack()
        port_input = Spinbox(server_gui, from_=49152, to=65535)
        port_input.pack()

        def start_server():
            ip = ip_input.get()
            port = port_input.get()

            octets = ip.split(".")

            if not (len(octets) == 4 and all(o.isdigit() and 0 <= int(o) <= 255 for o in octets)):
                showerror("Error IP", "Invalid format the IP. Expected format : \"127.0.0.1\"")
                return
            
            if ip in Interface.__ip_list_use:
                showerror("Error IP", "IP already used")
                return
            
            if not port.isdigit():
                showerror("Error Port", "Inva+lid format the port. Expected format : \"52152\"")
                return
            
            port = int(port)

            if not 49152 <= port <= 65535:
                showerror("Error Port", "Invalid port. Expected range : [49152-65535]")
                return

            if askyesno("Checking information", f"Are you sure of connect information:\n- IP: {ip}\n- Port: {port}"):
                Interface.__ip_list_use.append(ip)
                for widget in server_gui.winfo_children():
                    widget.destroy()
                
                Label(server_gui, text=f"Server started at {ip} on port {port}").pack()

                frame_stdout_server = Frame(server_gui)
                frame_stdout_server.pack(fill=BOTH, expand=True)

                text_stdout_server = Text(frame_stdout_server, wrap="word", height=10, width=50)
                text_stdout_server.pack(fill=BOTH, expand=True)

                sys.stdout = stdout_redirector(text_stdout_server) # => remplace the method of sys

                def run_server():
                    server_i = Server(ip, port)
                    server_i.Run_server()

                threading.Thread(target=run_server, daemon=True).start() # => Use trhead beacause the method Run_server bloc the TKinter instance
            
        
        Button(server_gui, text="Start server", command=start_server).pack()



tmp = Interface(1000, 1000, "Server App")

Button(tmp.gui, text="New server", command=tmp.new_server).pack()

frame_stdout_main = Frame(tmp.gui)
frame_stdout_main.pack(fill=BOTH, expand=True)

text_stdout_main = Text(frame_stdout_main, wrap="word", height=10, width=50)
text_stdout_main.pack(fill=BOTH, expand=True)

sys.stdout = stdout_redirector(text_stdout_main)
sys.stderr = stdout_redirector(text_stdout_main)



tmp.run()