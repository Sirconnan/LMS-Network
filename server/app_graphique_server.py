#!/home/marietm/Downloads/tmpp2/bin/python

import socket, sys, threading, psutil, time
from server import Server
from tkinter import * 
from tkinter.messagebox import * 
from tkinter.filedialog import *



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
    __NB_CERTIFICAT =0

    def __init__(self, width:int = 100, height:int = 100, text:str = "Server"):
        self.gui = Tk()
        self.gui.geometry(f"{width}x{height}")
        self.gui.configure(bg='gray25')
        self.gui.title(text)

        self.server_gui = None
        self.ip_input_srv = Interface.__IP
        self.port_input = None
        self.server_i = None
        self.thread_server = None

        self.cert_gui = None
        self.contry_input = "FR"
        self.region_input = "Haute-Savoie"
        self.city_input = "Annecy"
        self.society_input = "MS Secure"
        self.ip_input_crt = Interface.__IP
        self.path_ca_crt  = None
        self.path_ca_key = None

        return None


    def run(self):
        try:
            self.gui.mainloop()
        except KeyboardInterrupt:
            self.gui.quit()
            exit()
        
        return None

    
    def create_server(self):
        if Interface.__NB_SERVER >= 5:
            showinfo("Limit reached", "The max number of server is reached. (5 max)")
            return 1
        
        Interface.__NB_SERVER += 1

        self.server_gui = Toplevel(self.gui)
        self.server_gui.configure(bg='gray25')
        self.server_gui.geometry("1000x400")

        Label(self.server_gui, text="IP of the server").pack()
        self.ip_input_srv = Entry(self.server_gui)
        self.ip_input_srv.pack()
        self.ip_input_srv.insert(0, Interface.__IP)

        Label(self.server_gui, text="Port of the server").pack()
        self.port_input = Spinbox(self.server_gui, from_=1024, to=65535)
        self.port_input.pack()
        
        Button(self.server_gui, text="Start server", command=self.__start_server).pack()

        return None

        
    def __start_server(self):
        ip = self.ip_input_srv.get()
        port = self.port_input.get()

        connection = psutil.net_connections(kind="inet") 
        list_open_port = {conn.laddr.port for conn in connection}

        octets = ip.split(".")

        if not (len(octets) == 4 and all(o.isdigit() and 0 <= int(o) <= 255 for o in octets)):
            showerror("Error IP", "Invalid format the IP. Expected format : \"127.0.0.1\".")
            return 1
        
        if not port.isdigit():
            showerror("Error Port", "Invalid format the port. Expected format : \"52152\".")
            return 1
        
        port = int(port)

        if not 1024 <= port <= 65535:
            showerror("Error Port", "Invalid port. Expected range : [1024-65535].")
            return 1
        
        if port in list_open_port:
            showerror("Error Port", "Port already used.")
            return 1

        if askyesno("Checking information", f"Are you sure of connect information:\n- IP: {ip}\n- Port: {port}."):
            for widget in self.server_gui.winfo_children():
                widget.destroy()
            
            Label(self.server_gui, text=f"Server started at {ip} on port {port}.").pack()

            self.server_i = Server(ip, port)

            self.thread_server = threading.Thread(target= self.server_i.Run_server, daemon=True) # => Use trhead beacause the method Run_server bloc the TKinter instance
            self.thread_server.start()

            Button(self.server_gui, text="Stop Server", command=self.__stop_server).pack()
            self.server_gui.protocol("WM_DELETE_WINDOW", self.__stop_server)

        return None


    def __stop_server(self):
        self.server_i.thread_etat = False
        self.server_gui.destroy()
        Interface.__NB_SERVER -= 1
        
        return None
    
    def setting_crt(self):
        if Interface.__NB_CERTIFICAT >= 1:
            showinfo("Limit reached", "The max number of created certificat is reached. (1 max)")
            return 1

        Interface.__NB_CERTIFICAT += 1

        self.cert_gui = Toplevel(self.gui)
        self.cert_gui.configure(bg='gray25')
        self.cert_gui.geometry("1000x400")

        Label(self.cert_gui, text="Contry").pack()
        self.contry_input = Entry(self.cert_gui)
        self.contry_input.pack()
        self.contry_input.insert(0, "FR")

        Label(self.cert_gui, text="Region").pack()
        self.region_input = Entry(self.cert_gui)
        self.region_input.pack()
        self.region_input.insert(0, "Haute-Savoie")

        Label(self.cert_gui, text="City").pack()
        self.city_input = Entry(self.cert_gui)
        self.city_input.pack()
        self.city_input.insert(0, "Annecy")

        Label(self.cert_gui, text="Society").pack()
        self.society_input = Entry(self.cert_gui)
        self.society_input.pack()
        self.society_input.insert(0, "MS Secure")

        Label(self.cert_gui, text="IP of the server").pack()
        self.ip_input_crt = Entry(self.cert_gui)
        self.ip_input_crt.pack()
        self.ip_input_crt.insert(0, Interface.__IP)
        
        Button(self.cert_gui, text="Path to the certificat of the CA", command=lambda: self.__request_path(1)).pack()
        Button(self.cert_gui, text="Path to the certificat of the CA", command=lambda: self.__request_path(2)).pack()
       

        Button(self.cert_gui, text="Generate certificat", command=self.__generate_crt).pack()

        return None

    
    def __request_path(self, request):
            if request == 1:
                self.path_ca_crt = askopenfilename(title="Open certificat CA",filetypes=[("certificat file","*.pem"),("certificat file","*.crt")])
            elif request == 2:
                self.path_ca_key = askopenfilename(title="Open key CA",filetypes=[("key file","*.pem"),("key file","*.key")])
    
    def __generate_crt(self):

        contry = self.contry_input.get()
        region =self.region_input.get()
        city = self.city_input.get()
        society = self.society_input.get()
        ip = self.ip_input_crt.get()
        octets = ip.split(".")
        
        if not (len(octets) == 4 and all(o.isdigit() and 0 <= int(o) <= 255 for o in octets)):
            showerror("Error IP", "Invalid format the IP. Expected format : \"127.0.0.1\".")
            return 1
        
        if self.path_ca_crt == None:
            showerror("Error CA", "No path for the certificat of CA.")
            return 1
        
        if self.path_ca_key == None:
            showerror("Error CA", "No path for the key of CA.")
            return 1

        print(f"{contry}\n{region}\n{city}\n{society}\n{ip}\n{self.path_ca_crt}\n{self.path_ca_key}")

        Server.gen_crt_server(contry, region,city,society,ip)

        Interface.__NB_CERTIFICAT -= 1
        self.cert_gui.destroy()

        return None

        
    
main = Interface(500, 500, "Server App")

Button(main.gui, text="New server", command=main.create_server).pack()
Button(main.gui, text="New certificat", command=main.setting_crt).pack()


frame_stdout_main = Frame(main.gui)
frame_stdout_main.pack(fill=BOTH, expand=True)

text_stdout_main = Text(frame_stdout_main, wrap="word", height=10, width=50)
text_stdout_main.pack(fill=BOTH, expand=True)

stdout_redirector_main = stdout_redirector(text_stdout_main)
sys.stdout = stdout_redirector_main
sys.stderr = stdout_redirector_main
main.run()