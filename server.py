import socket

class Server:
    Taille_Bit = 1024
    Type_Ipv4 = socket.AF_INET
    Type_TCP = socket.SOCK_STREAM

    def __init__(self, ip_server = "127.0.0.1", port_ecoute = 2000):
        self.ip_server = ip_server
        self.port_ecoute = port_ecoute

    def Run_server(self):
        tcp_socket = None
        client = None
        
        try:
            tcp_socket = socket.socket(Server.Type_Ipv4, Server.Type_TCP)
        except socket.error as e:
            print(f"Une erreur c'est produite lors de la création de la socket : {e}")
            return

        Adress = (self.ip_server, self.port_ecoute)

        try:
            tcp_socket.bind(Adress)
        except socket.error as e:
            print(f"Une erreur c'est produite lors de l'écoute : {e}")
            return


        tcp_socket.listen()
        print("En écoute...")

        try:
            client, ip = tcp_socket.accept()
            print(f"Client connecter avec {ip}")
        except socket.error as e:
            print(f"Une erreur c'est produite lors de la connexion avec le client : {e}")
            tcp_socket.close()
            return

        try:
            data = client.recv(Server.Taille_Bit)
            if data:
                print(f"Message client: {data.decode()}")
            else:
                print("Connexion perdu avec le client")
        except socket.error as e:
            print(f" Une erreur c'est produite lors de la réception du message du client : {e}")
            client.close()
            return

        try:
            client.send("Message bien reçu !".encode())
        except socket.error as e:
            print(f"Une erreur c'est produit lors de l'envoi sur le client : {e}")
            client.close()
            return
            
        client.close()
        tcp_socket.close()

server1 = Server("192.168.1.34", 2000)

server1.Run_server()