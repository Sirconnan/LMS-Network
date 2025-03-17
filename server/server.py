import socket
import ssl
import threading
import random

from diffie_helman_server import * 

#===============================================
#   Class Server
#       -Attributs:
#           - ip_server = choice the ip addres to define listenig
#           - port_ecoute = the port to the listening
#       
#       -Methods:
#           -Run_client(self)
#               => Allow to run listening the request of client
#===============================================

class Server:
    # ===>  Attribut
    Taille_Bit = 1024
    Type_Ipv4 = socket.AF_INET
    Type_TCP = socket.SOCK_STREAM

    def __init__(self, ip_server = "127.0.0.1", port_ecoute = 2000):
        # ===> Class attribut
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
        context.load_cert_chain("/home/marietm/res403/server/server.crt", "/home/marietm/res403/server/server.key")
        #context.set_ciphers("DHE-RSA-AES256-GCM-SHA384")

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
            except KeyboardInterrupt:
                print("Stop server")
                exit()

            # ===> Create a thread for clients
            client_thread = threading.Thread(target=Server.handle_client, args=(client, tcp_socket, server_ssl))
            client_thread.start()

    def handle_client(client, tcp_socket, server_ssl):

        # ===> Create setting for Diffie Hellman
        prime_number = diffie_hellman_prime() # Prime number
        private_key = diffie_hellman_private_key(prime_number) # Pivate key
        public_key = diffie_hellman_public_key(private_key, prime_number) # Public key
        print(f"Nb_premier: {prime_number}\nClef priver: {private_key}\nClef publique: {public_key}")

        # ===> Send to client the prime number and the public key
        try:
             client.send(str(prime_number).encode())
             client.send(str(public_key).encode())
             print("Clef publique et nombre premier envoyer")
        except socket.error as e:
            print(f"Une erreur c'est produit lors de l'envoi sur le client : {e}")
            client.close()
            return

        # ===> Receve public key of the client
        try:
            data = client.recv(Server.Taille_Bit)
            if data:
                recv_public_key = int(data.decode())
                print("Clef public client reçu")
            else:
                print("Connexion perdu avec le client")
                client.close()
                return
        except socket.error as e:
            print(f" Une erreur c'est produite lors de la réception du message du client : {e}")
            client.close()
            return
        
        # ===> Create the share key 
        shared_key = diffie_hellman_shared_key(recv_public_key, private_key, prime_number)
        print(f"Clef partager: {shared_key}")

        # ===> Try to receve date of client
        try:
            message = client.recv(Server.Taille_Bit)
            if message:
                message = diffie_hellman_decrypt(message.decode(), shared_key)
                print(f"Message client: {message.decode()}")
            else:
                print("Connexion perdu avec le client")
                client.close()
                return
        except socket.error as e:
            print(f" Une erreur c'est produite lors de la réception du message du client : {e}")
            client.close()
            return

        # ===> Try to send the data to the client
        try:
            message = diffie_hellman_encrypt(message, shared_key)
            client.send(message.encode())
        except socket.error as e:
            print(f"Une erreur c'est produit lors de l'envoi sur le client : {e}")
            client.close()
            return
        
        # ===> Close the connecion
        print("\nEn écoute...")   
        client.close()