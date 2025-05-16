# Secure Communication Client Script

## Description

This script implements a client that establishes secure communication with a server using TLS and Diffie-Hellman key exchange. It also includes DNS resolution, TCP port scanning, a graphical user interface (GUI), and an interactive command-line interface (CLI) menu.

## Features

- Secure server connection via TLS.
- Diffie-Hellman key exchange for encrypted messaging.
- Encrypted message sending and receiving.
- Direct and reverse DNS resolution.
- Retrieval of DNS records (A, AAAA, MX, NS, CNAME, TXT).
- TCP port scanning.
- **Graphical User Interface (GUI)** for intuitive interaction.
- **Interactive CLI menu** for easy access to all features.

## Dependencies

The script requires the following libraries:

- `socket`
- `ssl`
- `dns.resolver`
- `random`
- `json`
- `scapy`
- `tkinter` (for GUI)
- `diffie_helman_client` (external module for Diffie-Hellman management)

## Installation

Before running the script, install the required dependencies with:

```sh
pip install dnspython scapy
```

## Usage

### Graphical User Interface (GUI)

To start the GUI application:

```sh
python client_gui.py
```

The GUI allows you to:

- Create a client connection by specifying the server IP and port.
- Send Echo requests.
- Perform DNS queries.
- Scan ports.

#### GUI Screenshots

_Insert GUI screenshots here._

### Launching the CLI Menu

```sh
python client_cli.py
```

You’ll be prompted to enter the server’s IP address or domain name. Then, an interactive menu will appear, offering various operations.

### CLI Menu Options

1. **Echo Request** – Sends a message to the server and displays the response.
2. **DNS** – Opens a sub-menu for direct, reverse DNS resolution, and retrieving DNS records.
3. **Port Scan** – Scans one or more ports on the target host.
4. **Quit** – Exits the application.

### Running Features Outside the Menu

#### Client Initialization

```python
client = Client("192.168.1.1")
```

#### Running the Client and Sending a Message

```python
client.Run_client(443, "Hello, Server!")
```

#### DNS Resolution

```python
print(client.resolution_dns("example.com"))
```

#### Reverse DNS Resolution

```python
print(client.reverse_resolution_dns())
```

#### Retrieving DNS Records

```python
client.get_dns_records("example.com")
```

#### Port Scanning

```python
client.run_scan([80, 443, 22])
```

## Error Handling

In case of network errors, the script displays an error message and gracefully closes the connection.

## Author

Script developed by lenzzair.
