import socket


def main():

    # AF_INET allow to use IPv4 to communicate with a remote machine
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # address listen all available network
    server_address = '0.0.0.0'
    server_port = 8000
    print(f"Starting up on port {server_port}\n")
    sock.bind((server_address, server_port))

    clients = []

    while True:
        try:
            data, address = sock.recvfrom(4096)
            if not data:
                continue

            # add client if not exit
            if address not in clients:
                clients.append(address)
            
            # take out user name from first byte
            user_name_len = int.from_bytes(data[:1], "big")
            # ignore first 1 byte take out latter name data
            user_name = data[1: user_name_len + 1].decode()
            # ignore first usernmae length and take out latter massge data
            message = data[user_name_len + 1:].decode()
            print("Username: ", user_name)
            print("Message: ", message)
            print("/-----------------/")

            # broad cast message 
            for client in clients:
                if client != address:
                    sock.sendto(data, client)

        except KeyboardInterrupt:
            print("\nServer stopped.")
            break

if __name__ == "__main__":
    main()