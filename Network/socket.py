import socket

_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
_socket.connect(('data.pr4e.org', 80))

print("Own address : ", _socket.getsockname())
print("Remote address : ", _socket.getpeername())
print()

cmd = "GET http://data.pr4e.org/romeo.txt HTTP/1.0\r\n\r\n".encode()    # \r\n\r\n 꼭 있어야 한다.
_socket.send(cmd)

while True :
    data = _socket.recv(512)

    #print("==>", data.decode())
    
    #if len(data) < 1 : <- 이렇게 해도된다. but data is None 은 안된다. 마지막 문자는 공백('')이다.
    if not data :
        break
    print(data.decode(), end="")

_socket.close()
