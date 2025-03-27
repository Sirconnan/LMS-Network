import socket
import ssl
import dns.resolver
import random
import json
from scapy.all import *
from diffie_helman_client import *


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
          self.error_sockets(e, tcp_socket)

        
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        context.load_verify_locations("/etc/ca-certificates/trust-source/ca.crt")
        #context.set_ciphers("TLS_AES_128_CCM_8_SHA256,TLS_AES_128_CCM_SHA256,TLS_AES_128_GCM_SHA256,TLS_AES_256_GCM_SHA384, TLS_CHACHA20_POLY1305_SHA256")
        # Force Diffie-Hellman
    
        
        Address = (self.ip_server, port_ecoute)
        
        # ===> try to connect to the server via the "Address"
        try:
            client_ssl = context.wrap_socket(tcp_socket, server_hostname=self.ip_server)
            client_ssl.connect(Address)
            
            
        except socket.error as e:
            self.error_sockets(e, client_ssl)


        
         # ==============================
        # Setting deffie_helman
        # ==============================

        try:
            
            json_liste = client_ssl.recv(Client.Taille_Bit).decode()
            print(json_liste)
            prime_number = json.loads(json_liste)[0]
            rcv_public_key = json.loads(json_liste)[1]
            
        except ValueError as e:
            print(f"Une erreur est survenue =====> {e}")
            exit()
            
       
        private_key = diffie_hellman_private_key(prime_number)
        public_key = diffie_hellman_public_key(private_key, prime_number)
        print(f"Public key :{public_key}\nPrivate key: {private_key}")
        
        try:
            client_ssl.send(str(public_key).encode())
            print("envoie public key")
            
            
        except socket.error as e:
            self.error_sockets(e, client_ssl)

            
        shared_key = diffie_hellman_shared_key(rcv_public_key, private_key, prime_number )
        print("shared key as been create")
        # ===> Send the client message
        try:
            diffie_message = diffie_hellman_encrypt(message, shared_key)
            client_ssl.send(diffie_message)
          
        except socket.error as e:
            self.error_sockets(e, client_ssl)

    
    
        print("Message envoyer a serveur")
        data = client_ssl.recv(Client.Taille_Bit)
        message_decrypt = diffie_hellman_decrypt(data, shared_key)
        
        if not data:
            print("Une erreur lors de la reception de la réponse du serveur")
            exit()
        
            
        # ===> close the socket
        client_ssl.close()
        
        print(f"Réponse serveur {message_decrypt}")
 
    # ---------------------------------------------
    # ---------------------------------------------
    def resolution_dns(self, domain ):
        
        try: 
            ip = socket.gethostbyname(domain)
            return f"{domain}: \n\t{ip}"
        except socket.error as e :
            self.error_sockets(e, tcp_socket)
    
    # ---------------------------------------------
    # ---------------------------------------------
    def reverse_resolution_dns(self):
        
        try:
            nom_domaine = socket.gethostbyaddr(self.ip_server)[0]
            return f"{self.ip_server}:\n\t{nom_domaine}"
        except socket.error as e:
            self.error_sockets(e)

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
    @staticmethod
    def error_sockets(error, sock=None):
        print(f"Erreur détectée ==> {error}")
        if sock:
            try:
                sock.close()
                print("Socket fermée correctement.")
            except Exception as close_error:
                print(f"Erreur lors de la fermeture du socket ==> {close_error}")
        exit(1)
        
    @staticmethod
    def exit_program(msg="Déconnexion..."):
        print(msg)
        exit(0)

# ---------------------------------------------
# ---------------------------------------------
            
