import socket

BYTES_TO_READ = 4096

# def get1(host, port):
#     request = b"GET / HTTP/1.1\nHost:" + host.encode('utf-8') + b"\n\n"# valid http request

#     request = b"GET / HTTP/1.1\nwww.google.com\n\n" # this should be directed to google
#     s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # creating a new internet socket
#     s.connect((host, port)) # request comes after you connect to the server
#     s.send(request) 
#     s.shutdown(socket.SHUT_WR) # only kills the write of the socket. the socket can stll read

#     result = s.recv(BYTES_TO_READ)

#     while(len(result) > 0):
#         print(result)
#         result = s.recv(BYTES_TO_READ)
#     s.close()

def get(host, port):
    request = b"GET / HTTP/1.1\nHost: www.google.com\n\n" # this should be directed to google
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port)) # request comes after you connect to the server
        s.send(request) 
        s.shutdown(socket.SHUT_WR) # only kills the write of the socket. the socket can stll read
        print("waiting for response!")

        chunk = s.recv(BYTES_TO_READ)
        result = b'' + chunk
        while(len(chunk) > 0):
            # print(result)
            chunk = s.recv(BYTES_TO_READ)
            result += chunk
        s.close()
        return result

print(get("localhost", 8080))