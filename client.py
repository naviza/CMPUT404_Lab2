import socket

BYTES_TO_READ = 4096

def get(host, port):
    request = b"GET / HTTP/1.1\nHost:" + host.encode('utf-8') + b"\n\n"# valid http request
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # creating a new internet socket
    s.connect((host, port)) # request comes after you connect to the server
    s.send(request) 
    s.shutdown(socket.SHUT_WR) # only kills the write of the socket. the socket can stll read

    result = s.recv(BYTES_TO_READ)

    while(len(result) > 0):
        print(result)
        result = s.recv(BYTES_TO_READ)
    s.close()

get("localhost", 8081)