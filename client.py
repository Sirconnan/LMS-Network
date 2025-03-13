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
        
        try:
            tcp_socket = socket.socket(Client.Type_Ipv4, Client.Type_TCP)
            
        except socket.error as e:
          print(f"Une erreur est survenue =====> {e}")
          exit()
            
        Address = (self.ip_server, self.port_ecoute)
        
        try:
            tcp_socket.connect(Address)
            
        except socket.error as e:
            print(f"Une erreur est survenue =====> {e}")
            exit()
          
        try:
          tcp_socket.send(self.message.encode("utf8"))
          
        except socket.error as e:
            print(f"Une erreur est survenue =====> {e}")
            exit()
    
    
        print("Message envoyer a serveur")
        
        if not data:
            print("Une erreur lors de la reception de la réponse du serveur")
            exit()
            
        else:
            data = tcp_socket.recv(Client.Taille_Bit)
        
        tcp_socket.close()
        
        print(f"Réponse serveur {data.decode()}")
       

client1 = Client("192.168.1.34", 2000, "Hello sale neuil")
client1.Run_client()