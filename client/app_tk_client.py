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
        # Increment client count and create new config window
        Lms_network.__nb_client += 1
        # Instruction label    
        self.instance_client = tk.Toplevel(self.gui)
        
        label_def_title = tk.Label(self.instance_client, 
                               text="Veuillez choisir une adresse IP ou un nom de domaine du serveur cible :", 
                               font=("Arial", 14)).pack(pady=20)
        
        # Show local IP address
        label_def_ip = tk.Label(self.instance_client, text=f"Vôtre adresse Ip: {Lms_network.ip_client.stdout.strip()}", font=("Arial", 14)).pack()
       
        # Input field for server IP/domain
        self.input_start_ip = tk.Entry(self.instance_client, font=("Arial", 14), width=50)
        self.input_start_ip.pack(pady=10)

        # Port selection spinbox
        self.input_start_port = tk.Spinbox(self.instance_client, from_=1, to=65535)
        self.input_start_port.pack()
        
        
        
        submit_button = tk.Button(self.instance_client, text="Valider", command=self.callback, font=("Arial", 12)).pack(pady=20)
    
    def get_used_ports(self):
        # Get all TCP ports currently in use
        cmd = "sudo netstat -nape --inet | awk '$1 == \"tcp\" {split($4, a, \":\"); print a[2]}'"
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        ports = result.stdout.strip().split('\n')
        return ports
    
    def callback(self):
        # Validate IP and port, then create client
        port_used = self.get_used_ports()
        ip_used = Lms_network.ip_client.stdout.strip()
        self.user_ip = self.input_start_ip.get()
        self.user_port = self.input_start_port.get()

        # Check if IP is already used
        if ip_used == self.user_ip:
            showerror('Error', f"L' adresse ip {self.user_ip} est deja utiliser", parent=self.instance_client)

        # Check if port is already used
        elif self.user_port in port_used:
            showerror('Error', f'Le port {self.user_port} est deja utiliser', parent=self.instance_client)
        # Ask for confirmation before creating the client
        else:
         
            if askyesno('Confirmation',f"La configuration du serveur est-elle correcte ?\n\nAdresse saisie : {self.user_ip}\nPort : {self.user_port}", parent = self.instance_client):
                
                showinfo('Validation', "Client crée !", parent = self.instance_client)
                self.client_script = Client(self.user_ip)
                self.instance_client.destroy() 
                self.show_main_menu() 
            else:
                showwarning("Annulation", "Client annulé.", parent = self.instance_client)


    def show_main_menu(self):
        # Create a new window for the main menu
        self.menu_window = tk.Toplevel(self.gui)
        self.menu_window.title("Menu Principal")
        self.menu_window.geometry("700x700")
        self.menu_window.config(bg='midnight blue')
        
        # Menu buttons for different actions
        tk.Button(self.menu_window, text="Requête Echo", command=self.requete_echo).pack(pady=10)
        tk.Button(self.menu_window, text="Menu DNS", command=self.menu_dns).pack(pady=10)
        tk.Button(self.menu_window, text="Scan de Ports", command=self.menu_scan_port).pack(pady=10)
        tk.Button(self.menu_window, text="Quitter", command=self.menu_window.destroy).pack(pady=10)
        
    def requete_echo(self):
        # Send test echo request
        message = "test"
        try:
            port = int(self.user_port)
            self.client_script.Run_client(port, message)
        except ValueError:
            print("Problème de type sur le port")

    def menu_dns(self):
            # Create a new window for DNS menu
        self.dns_window = tk.Toplevel(self.gui)
        self.dns_window.title("DNS Menu")
        self.dns_window.geometry("1000x600")
        self.dns_window.config(bg='midnight blue')

        tk.Label(self.dns_window, text="<<< DNS Menu >>>", font=("Arial", 18, "bold"), bg='lightblue').pack(pady=20)

        # Entry for domain or IP input
        tk.Label(self.dns_window, text="Enter a domain or IP:", bg='lightblue').pack()
        self.dns_input = tk.Entry(self.dns_window, font=("Arial", 14), width=40)
        self.dns_input.pack(pady=10)

        # Text box to show DNS responses
        self.dns_output = tk.Text(self.dns_window, height=15, width=70, bg='white')
        self.dns_output.pack(pady=20)

        # Buttons for DNS options
        tk.Button(self.dns_window, text="DNS Resolution", command=self.dns_resolution).pack(pady=5)
        tk.Button(self.dns_window, text="Reverse DNS", command=self.reverse_dns).pack(pady=5)
        tk.Button(self.dns_window, text="DNS Record Lookup", command=self.dns_registre).pack(pady=5)
        tk.Button(self.dns_window, text="Close", command=self.dns_window.destroy).pack(pady=20)
        
        
    def dns_resolution(self):
        
        reponse = self.client_script.resolution_dns(self.dns_input.get())
        self.dns_output.insert(tk.END, reponse, "\n")
    
    def reverse_dns(self):
        reponse = self.client_script.reverse_resolution_dns()
        self.dns_output.insert(tk.END, reponse)
        
    def dns_registre(self):
        reponse = self.client_script.resolution_dns(self.dns_input)
        self.dns_output.insert(reponse)
        
    def menu_scan_port(self):
        self.scan_window = tk.Toplevel(self.gui)
        self.scan_window.title("SCAN Menu")
        self.scan_window.geometry("1000x600")
        self.scan_window.config(bg='midnight blue')

        tk.Label(self.scan_window, text="<<< SCAN Menu >>>", font=("Arial", 18, "bold"), bg='lightblue').pack(pady=20)

        # Entry for domain or IP input
        tk.Label(self.scan_window, text="Enter ip and port number (22, 80, 443, ...)", bg='lightblue').pack()
        self.scan_input = tk.Entry(self.dns_window, font=("Arial", 14), width=40)
        self.pack(pady=20)
        
        self.scan_output = tk.Text(self.scan_window, height=15, width=70, bg='white')
        self.scan_output.pack(pady=20)
        
        tk.Button(self.scan_window, text="Start SCAN", command=self.scan_ports).pack(pady=5)
        tk.Button(self.scan_window, text="Close", command=self.scan_window.destroy).pack(pady=5)

    def scan_ports(self):
        ports = self.scan_input.split(",")
        liste_ports = []

        for iport in ports:
                    liste_ports.append(int(iport))

        if len(liste_ports) > 1:
            self.scan_output.insert("Scaning...")
            reponse = self.client_script.run_scan(liste_ports)
            self.scan_output.insert(reponse)
        
        elif len(liste_ports) == 1 : 
            self.scan_output.insert("Scanning...")
            reponse = self.client_script.scan_port(liste_ports)
            self.scan_output.insert(reponse)
        else:
            self.scan_output.insert("Select a port number")

# ===============================================

# ===============================================
instance1 = Lms_network()
tk.Button(instance1.gui, text="Crée un nouveaux client", command=instance1.start_new_client).pack(pady=20)
instance1.run_graphique()