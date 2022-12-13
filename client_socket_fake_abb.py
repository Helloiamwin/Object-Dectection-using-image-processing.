from re import M
import socket
import time

HOST = "192.168.125.5"
SERVER_PORT = 65432
FORMAT = "utf8"

   
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("CLIENT SIDE")

try:
    client.connect( (HOST, SERVER_PORT) )
    print("client address:",client.getsockname())

    start_sig = ' '
    center_shape_sig = ' '

    while start_sig != "x":
        print("Start wait _____")
        start_sig = client.recv(1024).decode(FORMAT) #Doi tin hieu "Start"
        print(start_sig)
        if start_sig == "Start":
            print("has recived Start")
            time.sleep(5)
            flag_process_img = "Done_Capture"
            client.sendall(flag_process_img.encode(FORMAT)) #gui tin hieu "Done_Capture"
            print("has send 'Done_Capture'\nWait center_sig")

            center_shape_sig = ' '
            while center_shape_sig != "x" and center_shape_sig != "end":
                center_shape_sig = client.recv(1024).decode(FORMAT) #Doi tin hieu vi tri center_shape
                check_sig = str(center_shape_sig)
                time.sleep(0.5)
                if check_sig[-1] == "o":
                    #-----routine-----#
                    time.sleep(0.5)
                    print("center_shape",center_shape_sig)
                    center_shape_sig = "end"

            Done_routine = "Done_Routine"
            client.sendall(Done_routine.encode(FORMAT))
            start_sig = ' '

except:
    print("Error")

client.close()