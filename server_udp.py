import socket, random

SERVER_IP = "0.0.0.0"
PORT = 8821
MAX_MSG_SIZE = 1024

def special_sendto(socket_object, response, client_address):
    fail = random.randint(1, 3)
    if not (fail == 1):
        socket_object.sendto(response.encode(), client_address)
    else:
        print("Oops")
        socket_object.sendto("".encode(), client_address)


server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind((SERVER_IP, PORT))
while True:
    client_message, client_address = server_socket.recvfrom(MAX_MSG_SIZE)
    data = client_message.decode()
    print("Client sent:", data)
    if(data == "Exit"):
        response = "Bye"
        special_sendto(server_socket, response, client_address)
        break
    response = "Super " + data
    special_sendto(server_socket, response, client_address)

server_socket.close()
