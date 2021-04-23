import socket

ClientSocket = socket.socket()
host = '127.0.0.1'
port = 2004

print('Waiting for connection response')
try:
    ClientSocket.connect((host, port))
except socket.error as e:
    print(str(e))

res = ClientSocket.recv(1024)
while True:
    Input = input('Hey there: ')
    ClientSocket.send(str.encode(Input))
    res = ClientSocket.recv(1024)
    if res == 'you are a user':
        print('ok')
    print(res.decode('utf-8'))

ClientMultiSocket.close()