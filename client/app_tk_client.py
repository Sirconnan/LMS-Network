import tkinter as tk
import subprocess
from client import Client
from tkinter.messagebox import *

class Lms_network:
     # Class attribute to count the number of clients
    __nb_client = 0
    
      # Command to get the local IP address
    cmd_ip_client = "ip addr show wlan0 | grep 'inet ' | awk '{print $2}' | cut -d/ -f1"
    ip_client = subprocess.run(cmd_ip_client, shell=True, capture_output=True, text=True)
    
    def __init__(self):
         # Initialize main GUI window
        self.gui = tk.Tk()
        self.gui.config(bg='skyblue')
        self.gui.title("LMS Network")
        self.gui.geometry("400x400")
    
        
    def run_graphique(self):
         # Start the Tkinter main loop
        self.gui.mainloop()
        
    def start_new_client(self):
        Lms_network.__nb_client += 1
    
        self.instance_client = tk.Toplevel(self.gui)

        label_def_title = tk.Label(self.instance_client, 
                               text="Veuillez choisir une adresse IP ou un nom de domaine du serveur cible :", 
                               font=("Arial", 14)).pack(pady=20)
        
        label_def_ip = tk.Label(self.instance_client, text=f"Vôtre adresse Ip: {Lms_network.ip_client.stdout.strip()}", font=("Arial", 14)).pack()
       
        self.input_start_ip = tk.Entry(self.instance_client, font=("Arial", 14), width=50)
        self.input_start_ip.pack(pady=10)

        self.input_start_port = tk.Spinbox(self.instance_client, from_=1, to=65535)
        self.input_start_port.pack()
        
        
        
        submit_button = tk.Button(self.instance_client, text="Valider", command=self.callback, font=("Arial", 12)).pack(pady=20)
    
    def get_used_ports(self):
        cmd = "sudo netstat -nape --inet | awk '$1 == \"tcp\" {split($4, a, \":\"); print a[2]}'"
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        ports = result.stdout.strip().split('\n')
        return ports
    
    def callback(self):
        
        port_used = self.get_used_ports()
        ip_used = Lms_network.ip_client.stdout.strip()
        self.user_ip = self.input_start_ip.get()
        self.user_port = self.input_start_port.get()
    
        if ip_used == self.user_ip:
            showerror('Error', f"L' adresse ip {self.user_ip} est deja utiliser", parent=self.instance_client)

        elif self.user_port in port_used:
            showerror('Error', f'Le port {self.user_port} est deja utiliser', parent=self.instance_client)
        else:
         
            if askyesno('Confirmation',f"La configuration du serveur est-elle correcte ?\n\nAdresse saisie : {self.user_ip}\nPort : {self.user_port}", parent = self.instance_client):
                
                showinfo('Validation', "Client crée !", parent = self.instance_client)
                self.client_script = Client(self.user_ip)
                self.instance_client.destroy() 
                self.show_main_menu() 
            else:
                showwarning("Annulation", "Client annulé.", parent = self.instance_client)


    def show_main_menu(self):
        self.menu_window = tk.Toplevel(self.gui)
        self.menu_window.title("Menu Principal")
        self.menu_window.geometry("700x700")
        self.menu_window.config(bg='gray')

        tk.Button(self.menu_window, text="Requête Echo", command=self.requete_echo).pack(pady=10)
        tk.Button(self.menu_window, text="Menu DNS", command=self.menu_dns).pack(pady=10)
        tk.Button(self.menu_window, text="Scan de Ports", command=self.scan_ports).pack(pady=10)
        tk.Button(self.menu_window, text="Quitter", command=self.menu_window.destroy).pack(pady=10)
        
    def requete_echo(self):
        message = "test"
        try:
            port = int(self.user_port)
            self.client_script.Run_client(port, message)
        except ValueError:
            print("Problème de type sur le port")

    def menu_dns(self):
        print("DNS lancé")

    def scan_ports(self):
        print("Scan lancé")


# ===============================================

# ===============================================
instance1 = Lms_network()
tk.Button(instance1.gui, text="Crée un nouveaux client", command=instance1.start_new_client).pack(pady=20)
instance1.run_graphique()