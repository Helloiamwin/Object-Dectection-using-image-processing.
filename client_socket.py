from re import M
import socket

HOST = "192.168.125.5"
SERVER_PORT = 65432
FORMAT = "utf8"

def sendList(client, list):

    for item in list:
        client.sendall(item.encode(FORMAT))
        #wait response
        client.recv(1024)

    msg = "end"
    client.send(msg.encode(FORMAT))

   
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("CLIENT SIDE")

try:
    client.connect( (HOST, SERVER_PORT) )
    print("client address:",client.getsockname())

    list = ["duchieuvn","15","nam"]

    msg = None
    msg_recv = None
    while (msg != "x"):
        
        msg = input("talk: ")
        client.sendall(msg.encode(FORMAT))
        if (msg == "thang"):
            msg_recv = client.recv(1024).decode(FORMAT)
            print("server has responded",msg_recv)
        if (msg == "list"):
            # wait response
            client.recv(1024)
            sendList(client, list)
except:
    print("Error")

client.close()