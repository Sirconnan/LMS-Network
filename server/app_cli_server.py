from server import Server

boucle = True

print("==== Serveur Echo TCP IP V4 ====")

while boucle:
    ip = input("IP du serveur : ")
    octets = ip.split(".")
    if len(octets) == 4 and all(o.isdigit() and 0 <= int(o) <= 255 for o in octets):
        boucle = False
    else:
        print("Format d'IP invalide. Veuillez entrer une adresse au format correct (ex: 192.168.1.1).")

boucle = True

while boucle:
    try :
        port = int(input("Port du serveur [49152-65535] : "))
        if 49152 <= port <= 65535:
            boucle = False
        else:
            print("Choisir un port entre 49152 et 65535")
    except ValueError:
        print("Choisir un nombre !!")

server1 = Server(ip, port)

server1.Run_server()