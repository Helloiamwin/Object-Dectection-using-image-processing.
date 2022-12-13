from re import M
import socket

HOST = "127.0.0.1"
SERVER_PORT = 65432
FORMAT = "utf8"


   
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("CLIENT SIDE")

try:
    client.connect( (HOST, SERVER_PORT) )
    print("client address:",client.getsockname())


    msg = None

    while (msg != "x"):
        msg = client.recv(1024).decode(FORMAT)
        print(msg)
except:
    print("Error")

client.close()