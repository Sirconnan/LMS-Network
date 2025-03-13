import socket

class Client:
    Taille_Bit = 1024
    Type_Ipv4 = socket.AF_INET
    Type_TCP = socket.SOCK_STREAM
    
    def __init__(self, ip_server, port_ecoute, message):
        self.ip_server = ip_server
        self.port_ecoute = port_ecoute
        self.message = message
        
    
    def Run_client(self):
        tcp_socket = socket.socket(Client.Type_Ipv4, Client.Type_TCP)
        
        Address = (self.ip_server, self.port_ecoute)
        tcp_socket.connect(Address)

        tcp_socket.send(self.message.encode("utf8"))
        print("Message envoyer")
        
        data = tcp_socket.recv(Client.Taille_Bit)
        
        tcp_socket.close()
        
        print(f"Réponse serveur {data.decode()}")
       
        
client1 = Client("192.168.1.34", 2000, "Hello sale neuil")
client1.Run_client()