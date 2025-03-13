import socket
import ssl
import dns.resolver
from scapy.all import *

#===============================================
#   Class Client
#       -Atttributs:
#           - ip_server = choice the ip addres to test the server
#           - port_ecoute = the port or list port that you would try
#       
#       -Methods:
#           -Run_client(self)
#               => Allow to run the request to the server
#===============================================
class Client:
    Taille_Bit = 1024
    Type_Ipv4 = socket.AF_INET
    Type_TCP = socket.SOCK_STREAM
    
    def __init__(self, ip_server ):
        # Class attribut
        self.ip_server = ip_server
        
    # ---------------------------------------------
    # ---------------------------------------------
    def Run_client(self, port_ecoute,  message):
        
        # ===> Create IP/TCP socket
        try:
            tcp_socket = socket.socket(Client.Type_Ipv4, Client.Type_TCP)
            
        except socket.error as e:
          print(f"Une erreur est survenue =====> {e}")
          exit()
        
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        context.load_verify_locations("./ca.crt")
        # Force Diffie-Hellman
        context.set_ciphers("DHE-RSA-AES256-GCM-SHA384")  
        
        Address = (self.ip_server, port_ecoute)
        
        # ===> try to connect to the server via the "Address"
        try:
            client_ssl = context.wrap_socket(tcp_socket, server_hostname=self.ip_server)
            client_ssl.connect(Address)
            
        except socket.error as e:
            print(f"Une erreur est survenue =====> {e}")
            exit()
        
        # ===> Send the client message
        try:
          client_ssl.send(message.encode("utf8"))
          
        except socket.error as e:
            print(f"Une erreur est survenue =====> {e}")
            exit()
    
    
        print("Message envoyer a serveur")
        data = client_ssl.recv(Client.Taille_Bit)
        
        if not data:
            print("Une erreur lors de la reception de la réponse du serveur")
            exit()
        
            
        # ===> close the socket
        client_ssl.close()
        
        print(f"Réponse serveur {data.decode()}")
 
    # ---------------------------------------------
    # ---------------------------------------------
    def resolution_dns(self, domain ):
        
        try: 
            ip = socket.gethostbyname(domain)
            print(f"{domain}: \n\t{ip}")
        except socket.error as e :
            print(f"echec de la résolution dns: {e}") 
    
    # ---------------------------------------------
    # ---------------------------------------------
    def reverse_resolution_dns(self):
        
        try:
            nom_domaine = socket.gethostbyaddr(ip)[0]
            print(f"{ip}:\n\t{nom_domaine}")
        except socket.error as e:
            print(f"echec de la résolution dns: {e}")

    # ---------------------------------------------
    # ---------------------------------------------
    def get_dns_records(self, domain):
        record_types = ["A", "AAAA", "MX", "NS", "CNAME", "TXT"]
        
        for record_type in record_types:
            try:
                answers = dns.resolver.resolve(domain, record_type)
                print(f"{record_type} Records:")
                for answer in answers:
                    print(f"  {answer}")
                    
            except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN):
                print(f"Aucun enregistrement {record_type} trouvé.")
            except dns.resolver.LifetimeTimeout:
                print(f"Timeout lors de la résolution de {record_type}.")

    # ---------------------------------------------
    # ---------------------------------------------
    def scan_port(self, ports):
        result, _ = sr(IP(dst=self.ip_server)/TCP(dport=ports, flags="S"))
        result.summary( lambda s,r: r.sprintf("%TCP.sport% \t \t %TCP.flags%") )

    # ---------------------------------------------
    # ---------------------------------------------
    def run_scan(self, ports):
        result, _ = sr(IP(dst=self.ip_server)/TCP(dport=ports, flags="S"))
    
        for _, reponse in result:
            flags = reponse.sprintf("%TCP.flags%")
            ports = reponse.sprintf("%TCP.sport%")

            if flags == "SA":
                print(f"Port {ports}: \tOuvert")
            elif flags == "RA":
                print(f"Port {ports} : \tFermer")
            else:
                print(f"Port {ports} : \tFiltrer")
                
                

# ---------------------------------------------
# ---------------------------------------------
# ---------------------------------------------
            
# client1 = Client("192.168.1.34")
# # port = [80,80,2222]
# # client1.run_scan(port)
# client1.Run_client(2000, "neuil")