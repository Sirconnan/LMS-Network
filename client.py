import socket
import ssl

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
    
    def __init__(self, ip_server, port_ecoute, message):
        # Class attribut
        self.ip_server = ip_server
        self.port_ecoute = port_ecoute 
        self.message = message
        
    # Instance method
    def Run_client(self):
        
        # ===> Create IP/TCP socket
        try:
            tcp_socket = socket.socket(Client.Type_Ipv4, Client.Type_TCP)
            
        except socket.error as e:
          print(f"Une erreur est survenue =====> {e}")
          exit()
        
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        Address = (self.ip_server, self.port_ecoute)
        
        # ===> try to connect to the server via the "Address"
        try:
            client_ssl = context.wrap_socket(tcp_socket, server_hostname=self.ip_server)
            client_ssl.connect(Address)
            
        except socket.error as e:
            print(f"Une erreur est survenue =====> {e}")
            exit()
        
        # ===> Send the client message
        try:
          client_ssl.send(self.message.encode("utf8"))
          
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
       

client1 = Client("192.168.1.34", 2000, "Hello sale neuil")
client1.Run_client()