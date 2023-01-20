import socket
from threading import Thread

BYTES_TO_READ = 4096
HOST = "localhost"
PORT = 8081 # 8080 because of convention

def handle_connection(conn, addr):
    with conn:
        print("Connected to {addr} at port {port}")
        while True:
            data = conn.recv(BYTES_TO_READ)
            if not data:
                break
            print(data) # print to console
            conn.sendall(data) # send it right back
            # send does not guarantee that all of your data that you sent. it will return how many bytes was sent
            # sendall will return an error if it can't send properly
        # conn is closed when leaving the with-block
    return

def start_server():
    # use a with lock: autocloses resources.
    # create the socket as "s". when the program leaves the s-block, it autocloses the s-socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        # s.setsockopt(level, option, value)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # 1 is truthy
        # --> this allows a socket to rebind to the same address under certain conditions
        # usually, when you close the socket, theres a period of time that the socket connection will remain open.
        # setting this will allows you to rebind to the same socket
        s.listen()

        conn, addr = s.accept() # accept returns the conneciton that was just made
        # as long as the address from the source of the incoming packet
        # handle_connection(conn, addr)

        while True:
            conn, addr = s.accept() # stops working at this point
            # the moment you get a connection from another client, we pass off the connection to another thread for processing
            thread = Thread(target=handle_connection, args=(conn, addr))
            thread.run()


start_server()