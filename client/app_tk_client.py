import tkinter as tk
import subprocess
from tkinter.messagebox import *

class Lms_network:
    
    __nb_client = 0
    cmd_ip_client = "ip addr show wlan0 | grep 'inet ' | awk '{print $2}' | cut -d/ -f1"
    ip_client = subprocess.run(cmd_ip_client, shell=True, capture_output=True, text=True)
    
    def __init__(self):
        self.gui = tk.Tk()
        self.gui.config(bg='skyblue')
        self.gui.title("LMS Network")
        self.gui.geometry("400x200")
    
    def run_graphique(self):
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
        user_ip = self.input_start_ip.get()
        user_port = self.input_start_port.get()
    
        if ip_used == user_ip:
            showerror('Error', f"L' adresse ip {ip_used} est deja utiliser", parent=self.instance_client)

        elif user_port in port_used:
            showerror('Error', f'Le port {user_port} est deja utiliser', parent=self.instance_client)
        else:
         
            if askyesno('Confirmation',f"La configuration du serveur est-elle correcte ?\n\nAdresse saisie : {user_ip}\nPort : {user_port}", parent = self.instance_client):
                showinfo('Validation', "Client crée !", parent = self.instance_client)
            else:
                showwarning("Annulation", "Client annulé.", parent = self.instance_client)

instance1 = Lms_network()
tk.Button(instance1.gui, text="Crée un nouveaux client", command=instance1.start_new_client).pack(pady=20)
instance1.run_graphique()
