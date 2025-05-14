import socket
import threading

def protocol_header(username_len):
    return int.to_bytes(username_len, 1, "big")

def print_message(bytes_data: bytes):
    # take out first 1 bit which represent user name length convert as int
    user_name_len = int.from_bytes(bytes_data[:1], "big")

    user_name = bytes_data[1:user_name_len + 1].decode()
    message = bytes_data[user_name_len + 1:].decode()
    print(f"{user_name}: {message}")

# send address to input function
def receive_message(sock: socket, user_name: str):
    while True:
        # recvfrom() receive source adress inforation
        # ignore address
        response_data, _ = sock.recvfrom(4096)
        print("\033[2K\r", end="")
        print_message(response_data)
        print(f"{user_name} :> ", end="", flush=True) 


def input_message(sock: socket, user_name: str, server_address):
    while True:
        message = input(f"{user_name} :> ")
        print("\033[1A\033[2K", end="")
        print(f"{user_name} : {message}")
        data = protocol_header(len(user_name)) + (user_name + message).encode()
        #sock.send(data)
        sock.sendto(data, server_address)

def main():
    # AF_INET allow to use IPv4 to communicate with a remote machine
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    server_address = ('0.0.0.0', 8000)

    user_name = input('Enter username: ')
    print(f"{user_name} has joined the chat")




    '''
    try:
        sock.connect((server_address, server_port))
    except socket.error as err:
        print(err)
        sys.exit(1)

    -connect() receicing the sercer is blocked
    '''

    
    init_data = protocol_header(len(user_name)) + (user_name + "").encode()
    sock.sendto(init_data, server_address)

    # daemon thread when main prigram finish thread automatically exit
    input_message_thread =  threading.Thread(target=input_message, args=(sock, user_name, server_address,), daemon=True)
    receive_message_thread =  threading.Thread(target=receive_message, args=(sock, user_name,), daemon=True)

    # prevent to block thread which use input()
    input_message_thread.start()
    receive_message_thread.start()

    # stop threads till finish main function
    input_message_thread.join()
    receive_message_thread.join()
if __name__ == "__main__":
    main()