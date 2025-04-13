import socket, ssl, threading, random, json

from OpenSSL import crypto
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


    def __init__(self, ip_server : str = "127.0.0.1", port_ecoute : int = 2000):
        # ===> Class attribut
        self.ip_server = ip_server
        self.port_ecoute = port_ecoute
        self.thread_etat = True

    def Run_server(self):
        tcp_socket = None
        server_ssl = None
        client = None

        # ===> Add parameter of tls connexion
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        context.load_cert_chain("/home/marietm/LMS-Network/server/server.crt", "/home/marietm/LMS-Network/server/server.key")
        # context.set_ciphers("TLS_AES_128_CCM_8_SHA256, TLS_AES_128_CCM_SHA256, TLS_AES_128_GCM_SHA256, TLS_AES_256_GCM_SHA384 , TLS_CHACHA20_POLY1305_SHA256")

        # ===> Define IP/TCP socket
        try:
            tcp_socket = socket.socket(Server.Type_Ipv4, Server.Type_TCP)
        except socket.error as e:
            Server.error_sockets(e, tcp_socket, server_ssl)

        # ===> Try to create IP/TCP socket
        try:
            tcp_socket.bind((self.ip_server, self.port_ecoute))
        except socket.error as e:
            Server.error_sockets(e, tcp_socket, server_ssl)
        
        # ===> Try to create secure connexion
        try:
            server_ssl = context.wrap_socket(tcp_socket, server_side=True)
        except ssl.SSLError as e:
            Server.error_sockets(e, tcp_socket, server_ssl)

        # ===> Listenig on the socket
        server_ssl.listen(5)
        server_ssl.settimeout(1)
        print("\nListen ...")

        while self.thread_etat:
            # ===> Try to accept the connecion of client    
            try:
                client, ip = server_ssl.accept()
                print(f"Client connect to ip : {ip}")
                
                # ===> Create a thread for clients
                client_thread = threading.Thread(target=Server.handle_client, args=(client,))
                client_thread.start()
            except socket.timeout:
                continue
            except socket.error as e:
                Server.error_sockets(e, tcp_socket, server_ssl)
            except KeyboardInterrupt:
                self.thread_etat = False
        print("Stop server")
        server_ssl.close()
        tcp_socket.close()
        return 0


    @staticmethod
    def handle_client(client):

        # ===> Create setting for Diffie Hellman
        prime_number = diffie_hellman_prime() # => Prime number
        private_key = diffie_hellman_private_key(prime_number) # => Pivate key
        public_key = diffie_hellman_public_key(private_key, prime_number) # => Public key
        print(f"Prime number: {prime_number}\nPivate Key: {private_key}\nPublic Key: {public_key}")

        # ===> Generate JSON whith the prime number and the public key

        data_diffie_helman = json.dumps([prime_number,public_key])
        data_diffie_helman_byte = data_diffie_helman.encode("utf-8")
        
        # ===> Try send to client
        try:
             client.send(data_diffie_helman_byte)
             print("\nPublic key and prime number send")
        except socket.error as e:
            Server.error_client(e, client)

        # ===> Try receve public key of the client
        try:
            data = client.recv(Server.Taille_Bit)
        except socket.error as e:
            Server.error_client(e, client)

        if not data:
            Server.error_client("No data received", client)
        
        try:
            recv_public_key = int(data.decode("utf-8"))
        except ValueError as e:
            Server.error_client(e, client)
            
        print("Client public key receved")
        
        # ===> Create the share key 
        shared_key = diffie_hellman_shared_key(recv_public_key, private_key, prime_number)
        print(f"Shared Key: {shared_key}")

        # ===> Try to receve date of client
        try:
            message_encrypt = client.recv(Server.Taille_Bit)
        except socket.error as e:
            Server.error_client(e, client)

        if not message_encrypt:
            Server.error_client("No data received", client)
        
        message_decrypt = diffie_hellman_decrypt(message_encrypt, shared_key)
        print(f"Message client: {message_decrypt}")

        message_encrypt = diffie_hellman_encrypt(message_decrypt, shared_key)

        # ===> Try to send the data to the client
        try:
            client.send(message_encrypt)
        except socket.error as e:
            Server.error_client(e, client)
        
        # ===> Close the connecion
        print("\nListen...")   
        client.close()
        return 0

    @staticmethod
    def gen_crt_server(contry, region, city, society, ip):

        # ===> Generate private key
        key = crypto.PKey()
        key.generate_key(crypto.TYPE_RSA, 2048)

        # ===> Generate request for certification  
        req = crypto.X509Req()
        req.get_subject().C = contry
        req.get_subject().ST = region
        req.get_subject().L = city
        req.get_subject().O = society
        req.get_subject().OU = society
        req.get_subject().CN = ip
        req.set_pubkey(key)
        req.sign(key, "sha512")

        # ===> Get the certifica of the ca
        with open("/home/marietm/LMS-Network/server/ca.crt", "rt") as f:
            ca_cert = crypto.load_certificate(crypto.FILETYPE_PEM, f.read())

        # ===> Get the key of the ca
        with open("/home/marietm/LMS-Network/server/ca.key", "rt") as f:
            ca_key = crypto.load_privatekey(crypto.FILETYPE_PEM, f.read())

        # ===> Sign the certifica by the ca
        cert = crypto.X509()
        cert.set_serial_number(random.getrandbits(64))
        cert.gmtime_adj_notBefore(0)
        cert.gmtime_adj_notAfter(365*24*60*60) 
        cert.set_subject(req.get_subject())
        cert.set_issuer(ca_cert.get_subject())
        cert.set_pubkey(req.get_pubkey())
        cert.add_extensions([
            crypto.X509Extension(b"subjectAltName", False, f"IP:{ip}".encode())
        ])
        cert.sign(ca_key, "sha512")

        # ===> Whrite the certificat in a file
        with open("/home/marietm/LMS-Network/server/server.key", "wt") as f:
            f.write(crypto.dump_privatekey(crypto.FILETYPE_PEM, key).decode())

         # ===> Whrite the key in a file
        with open("/home/marietm/LMS-Network/server/server.crt", "wt") as f:
            f.write(crypto.dump_certificate(crypto.FILETYPE_PEM, cert).decode())


    @staticmethod
    def error_sockets(error, sock, ssl):
        print(f"An error has occurred ==> {error}")
        if ssl is not None:
            ssl.close()
        sock.close()
        return 1
    
    @staticmethod
    def error_client(error, client):
        print(f"An error has occurred ==> {error}")
        print("\nListen...")
        client.close()
        return 1