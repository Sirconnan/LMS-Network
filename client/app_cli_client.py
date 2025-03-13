from client import Client

def cli_enable(choix_client):
    
    
    while choix_client != 4:
        print("+-------------------+")
        print("|  === Menu CLI === |")
        print("+------------------+")
        print("| 1. Requête echo   |")
        print("| 2. Dns            |")
        print("| 3. Scan de port   |")
        print("| 4. Quiter         |")
        print("+-------------------+ \n\n")
        
        try:
            choix_client = int(input("=>"))
        except ValueError as e:
            print("Vous devez choisir un nombre du tableau")
        
        if choix_client == 1:
            try: 
                port = int(input("Sur qu'elle port écoute vôtre serveur\n=>"))
            except ValueError:
                print("Veuillez saisir un nombre entier")
            
            message = input("Quelle est vôtre message a transmettre :\n=> ")
                
            client_cli_1.Run_client(port, message)

        elif choix_client == 2:
            choix_client_2 = 0
            
            while choix_client_2 != 4 :
                print("+-------------------+")
                print("|  === Menu CLI === |")
                print("+------------------+")
                print("| 1. Resolution Dns |")
                print("| 2. Reverse Dns    |")
                print("| 3. Registre Dns   |")
                print("| 4. Retour         |")
                print("+-------------------+ \n\n")

                try:
                    choix_client_2 = int(input("=>"))
                except ValueError as e:
                    print("Vous devez choisir un nombre du tableau") 
                    
                if choix_client_2 == 1:
                    domaine = input("Veuillez choisir un domain:\n=>")
                    client_cli_1.resolution_dns(domaine)
                
                elif choix_client_2 == 2:
                    client_cli_1.reverse_resolution_dns()
                
                elif choix_client_2 == 3:
                    domaine = input("Veuillez choisir un domain:\n=>")
                    client_cli_1.get_dns_records(domaine)
        
        
        elif choix_client == 3:
            
            target_ports = input("Entrez les ports a scanner (ex: 80, 443, ...) : ")
            target_ports = target_ports.split(",")
            target_int_ports = []

            for iport in target_ports:
                target_int_ports.append(int(iport))

            if len(target_int_ports) > 1:
                print(f"\n\nScanning {client_cli_1.ip_server}...")

                client_cli_1.run_scan(target_int_ports)

            elif len(target_int_ports) == 1:
                print(f"\n\nScanning {client_cli_1.ip_server}...")
                client_cli_1.scan_port(target_int_ports)

            else:
                print("Vous n'avez pas rentrez de ports!")
                    
            
#-----------------------------------------------------
#-----------------------------------------------------
#-----------------------------------------------------


ip_server = input("Veuillez choisir une address IP ou nom de domaine du server cible pour lancer une instance.\n=>")

client_cli_1 = Client(ip_server)
cli_enable(0)