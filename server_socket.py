import socket 
import threading #thư viện đa luồng

HOST = "192.168.125.5" 
SERVER_PORT = 65432 
FORMAT = "utf8"


def handleClient(conns, conn: socket, addr): #xử lý client
    
    print("conn:",conn.getsockname(), "connected") #in ra tên socket
    
    msg = None
    while (msg != "x"):
        msg = conn.recv(1024).decode(FORMAT)
        print("client ",addr, "says", msg)   
        if msg == "x":
            conns.remove(conn)
        for i in conns:
            i.send(msg.encode(FORMAT))
            print("send to all client")
        
    print("client" , addr, "finished")
   # conns.remove(conn)
    print("There are {} clients".format(len(conns)))
    print(conn.getsockname(), "closed")
    conn.close()

#-----------------------main-------------------------
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

s.bind((HOST, SERVER_PORT))
s.listen()

print("SERVER SIDE")
print("server:", HOST, SERVER_PORT)
print("Waiting for Client")

nClient = 0

my_clients = [] 
while (nClient < 6): #nhận tối đa 6 lần client kết nối
    try:
        conn, addr = s.accept()
        my_clients += [conn]
        print("There are {} clients".format(len(my_clients)))

        print(conn.getsockname())
        thr = threading.Thread(target=handleClient, args=(my_clients, conn, addr))
        thr.daemon = False #chỉ khi tất cả client kết thúc thì server mới được kết thúc
        thr.start()

    except:
        print("Error")
    nClient += 1

print("End")
#input()
s.close();


