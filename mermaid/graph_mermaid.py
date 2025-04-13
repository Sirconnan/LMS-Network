from scapy.all import rdpcap, IP, TCP, UDP

def extract_tcp_flags(tcp_pkt):
    flags = []
    flag_str = str(tcp_pkt.flags)
    if tcp_pkt.flags & 0x02:
        flags.append("SYN")
    if tcp_pkt.flags & 0x10:
        flags.append("ACK")
    if tcp_pkt.flags & 0x01:
        flags.append("FIN")
    if tcp_pkt.flags & 0x04:
        flags.append("RST")
    if tcp_pkt.flags & 0x08:
        flags.append("PSH")
    if tcp_pkt.flags & 0x20:
        flags.append("URG")
    return ",".join(flags) if flags else "NONE"

def pcap_to_full_sequence(pcap_file, output_file="sequence.mmd"):
    packets = rdpcap(pcap_file)
    participants = set()
    sequence_lines = ["sequenceDiagram"]

    for pkt in packets:
        if IP in pkt:
            proto = None
            sport = dport = "?"
            flags = ""

            if TCP in pkt:
                proto = "TCP"
                sport = pkt[TCP].sport
                dport = pkt[TCP].dport
                flags = extract_tcp_flags(pkt[TCP])
            elif UDP in pkt:
                proto = "UDP"
                sport = pkt[UDP].sport
                dport = pkt[UDP].dport
                flags = ""

            if proto:
                src = pkt[IP].src
                dst = pkt[IP].dst
                participants.add(src)
                participants.add(dst)

                label = f"{proto} : {sport} => {dport}"
                if flags:
                    label += f" [{flags}]"

                sequence_lines.append(f"    {src} ->> {dst}: {label}")

    # Ajouter les participants en haut (une seule fois chacun)
    participant_lines = [f"    participant {ip}" for ip in sorted(participants)]
    sequence_lines = ["sequenceDiagram"] + participant_lines + sequence_lines[1:]

    with open(output_file, "w") as f:
        f.write("\n".join(sequence_lines))

    print(f"Diagramme Mermaid généré avec chaque paquet dans '{output_file}'.")

# Exemple d'utilisation
pcap_to_full_sequence("fichier.pcapng")
