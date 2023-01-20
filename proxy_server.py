import socket
from threading import Thread

BYTES_TO_READ = 4096
PROXY_SERVER_HOST = "localhost"
PROXY_SERVER_PORT = 8080 # 8080 because of convention

# proxy server accept requests and then relays them to a target
# when the p.server gets a response, 

def send_request(host, port, request_data):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        # sending data to google
        client_socket.connect((host, port))
        client_socket.send(request_data)
        client_socket.shutdown(socket.SHUT_WR) # let the server know that we're done sending data
        # getting response from google
        data = client_socket.recv(BYTES_TO_READ)
        result = b'' + data
        while len(data) > 0:
            # keep consuming data and accumulate it
            data = client_socket.recv(BYTES_TO_READ)
            result += data
        return result
    return

def handle_connection(conn, addr):
    with conn:
        print(f"connected to {addr}")
        request = b''
        while True:
            data = conn.recv(BYTES_TO_READ)
            if not data:
                break
            print(data)
            request += data
        response = send_request("www.google.com", 80, request)
        conn.sendall(response)
    return


def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((PROXY_SERVER_HOST, PROXY_SERVER_PORT))
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.listen(2) # 2 = size of queue allowed

        conn, addr = server_socket.accept() # Double check this part
        handle_connection(conn, addr) # double check this part
    return

def start_threaded_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((PROXY_SERVER_HOST, PROXY_SERVER_PORT))
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.listen(2) # 2 = size of queue allowed

        while True:
            conn, addr = server_socket.accept() # stops working at this point
            # the moment you get a connection from another client, we pass off the connection to another thread for processing
            thread = Thread(target=handle_connection, args=(conn, addr))
            thread.run()
    pass

start_threaded_server()