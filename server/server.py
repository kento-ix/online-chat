import socket
import time
from datetime import datetime, timedelta
import threading

def cleanup_client(client_list):
    while True:
        print(f"The clients currently present in the relay system are {len(client_list)}")
        print(client_list)
        print("/-----------------/")

        now = datetime.now()
        expired_second = 120
        expired_at = timedelta(seconds=expired_second)

        to_remove = []

        for client in client_list:
            diff = now - client["last_sent"]
            if diff > expired_at:
                to_remove.append(client)

        for client in to_remove:
            print("<<<")
            print("deleted client", client)
            print("<<<")
            client_list.remove(client)

        time.sleep(5)

def main():

    # AF_INET allow to use IPv4 to communicate with a remote machine
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # address listen all available network
    server_address = '0.0.0.0'
    server_port = 8000
    print(f"Starting up on port {server_port}\n")
    sock.bind((server_address, server_port))

    client_list = []

    thread = threading.Thread(target=cleanup_client, args=(client_list,), daemon=True)
    thread.start()

    while True:
        try:
            data, address = sock.recvfrom(4096)
            if not data:
                continue

            found_index = -1
            for i in range(len(client_list)):
                if client_list[i]["address"] == address:
                    found_index = i
                    break
            # add client if not exist
            if found_index == -1: 
                client_list.append({"address": address, "last_sent": datetime.now()})
            # update time if exist
            else: 
                client_list[found_index]["last_sent"] = datetime.now()
            
            # take out user name from first byte
            user_name_len = int.from_bytes(data[:1], "big")
            # ignore first 1 byte take out latter name data
            user_name = data[1: user_name_len + 1].decode()
            # ignore first usernmae length and take out latter massge data
            message = data[user_name_len + 1:].decode()

            if message.strip() == "":
                continue

            print("Username: ", user_name)
            print("Message: ", message)
            print(f"Current on relay system: {len(client_list)}")
            print("/-----------------/")

            # broad cast message 
            for client in client_list:
                client_addr = client["address"]
                # check both address and port 
                if client_addr[0] == address[0] and client_addr[1] == address[1]:
                    continue
                print("send to", client_addr[1])
                sock.sendto(data, client_addr)

        except KeyboardInterrupt:
            print("\nServer stopped.")
            break

if __name__ == "__main__":
    main()