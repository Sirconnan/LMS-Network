import socket
import threading
import time

class Server:
    Taille_Bit = 1024
    Type_Ipv4 = socket.AF_INET
    Type_TCP = socket.SOCK_STREAM

    def __init__(self, ip_server = "127.0.0.1", port_ecoute = 2000):
        self.ip_server = ip_server
        self.port_ecoute = port_ecoute

    def Run_server(self):
        try:
            tcp_socket = socket.socket(Server.Type_Ipv4, Server.Type_TCP)
        except socket.error as e:
            print(f"Une erreur c'est produite {e}")
            exit()

        Adress = (self.ip_server, self.port_ecoute)
        tcp_socket.bind(Adress)

        while True:
            tcp_socket.listen()
            print("En écoute...")

            client, ip = tcp_socket.accept()
            print(f"Client connecter avec {ip}")

            data = client.recv(Server.Taille_Bit)
            if data:

                print(f"Message client: {data.decode()}")
                client.send("Message bien reçu !".encode())

            client.close()

server1 = Server("192.168.1.34", 2000)

server1.Run_server()