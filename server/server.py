import socket
import ssl
import threading

#===============================================
#   Class Server
#       -Atttributs:
#           - ip_server = choice the ip addres to define listenig
#           - port_ecoute = the port to the listening
#       
#       -Methods:
#           -Run_client(self)
#               => Allow to run listening the request of client
#===============================================

class Server:
    #  attribut
    Taille_Bit = 1024
    Type_Ipv4 = socket.AF_INET
    Type_TCP = socket.SOCK_STREAM

    def __init__(self, ip_server = "127.0.0.1", port_ecoute = 2000):
        # Class attribut
        self.ip_server = ip_server
        self.port_ecoute = port_ecoute

    def Run_server(self):
        tcp_socket = None
        client = None

        # ===> Define IP/TCP socket
        try:
            tcp_socket = socket.socket(Server.Type_Ipv4, Server.Type_TCP)
        except socket.error as e:
            print(f"Une erreur c'est produite lors de la création de la socket : {e}")
            return
        
        # ===> Add parameter of tls connexion
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        context.load_cert_chain("./server.crt", "./server.key")
        context.set_ciphers("DHE-RSA-AES256-GCM-SHA384")

        # ===> Try to create IP/TCP socket
        try:
            tcp_socket.bind((self.ip_server, self.port_ecoute))
        except socket.error as e:
            print(f"Une erreur c'est produite lors de l'écoute : {e}")
            return

        # ===> Listenig on the socket
        tcp_socket.listen(5)
        print("En écoute...")

        # ===> Create secure connexion
        server_ssl = context.wrap_socket(tcp_socket, server_side=True)

        while True:
            # ===> Try to accept the connecion of client    
            try:
                client, ip = server_ssl.accept()
                print(f"Client connecter avec {ip}")
            except socket.error as e:
                print(f"Une erreur c'est produite lors de la connexion avec le client : {e}")
                server_ssl.close()
                return
            # ===> Create a thread for clients
            client_thread = threading.Thread(target=Server.handle_client, args=(client, tcp_socket, server_ssl))
            client_thread.start()  # Démarrage du thread pour gérer le client
            
    def handle_client(client, tcp_socket, server_ssl):
        # ===> Try to receve date of client
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

        # ===> Try to send the data to the client
        try:
            client.send(data)
        except socket.error as e:
            print(f"Une erreur c'est produit lors de l'envoi sur le client : {e}")
            client.close()
            return
        
        # ===> Close the connecion    
        client.close()

server1 = Server("192.168.1.34", 2000)

server1.Run_server()