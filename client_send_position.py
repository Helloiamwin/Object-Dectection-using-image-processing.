
from multiprocessing.connection import wait
from re import M
import socket
import time
import cv2
import numpy as np
import matplotlib.pyplot as plt
import os

HOST = "192.168.125.5" #my IP address 
SERVER_PORT = 65432
FORMAT = "utf8"

def Get_path_img(): #To get the path path of image that contain the last image had captured
    path = 'E:\\Year4_Sec1\\Image_Pro\\final_exam\\official\\test_12_12' #The folder for saving image
    path_img = ''
    for i in os.listdir(path):
        path_img = i
    return path +'\\'+ path_img
  
def Invert_Coor_Left_Top(center): #To tranfer size image from camera to real 
    
    w_real = center[0]
    h_real = center[1]

    h_origin = 78 #mm  278.17; -168.86  --> 356.27; -58.96
    w_origin = 110

    h_pixel = 960 # HD image
    w_pixel = 1280

    w_real = int(np.floor((w_real/w_pixel)*w_origin))
    h_real = int(np.floor((h_real/h_pixel)*h_origin))

    return [h_real, w_real]

def Invert_Coor(center): #To tranfer size image from camera to real 
    
    w_real = center[0]
    h_real = center[1]

    h_origin = 78 #mm  278.17; -168.86  --> 356.27; -58.96
    w_origin = 110

    h_pixel = 960 # HD image
    w_pixel = 1280

    if w_real > (w_pixel/2):
        w_real = int(np.floor(((w_real-(w_pixel/2))/(w_pixel/2))*(w_origin/2)))
    else:
        w_real = -(int(np.floor((((w_pixel/2)-w_real)/(w_pixel/2))*(w_origin/2))))

    if h_real > (h_pixel/2):
        h_real = int(np.floor(((h_real-(h_pixel/2))/(h_pixel/2))*(h_origin/2)))
    else:
        h_real = -(int(np.floor((((h_pixel/2)-h_real)/(h_pixel/2))*(h_origin/2))))

    return [h_real, w_real]

def Processing():
    path = Get_path_img()
    image = cv2.imread(path)
    img = cv2.fastNlMeansDenoisingColored(image,None,10,10,7,21) #lọc nhiễu ảnh
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)	#chuyển sang ảnh xám
    img = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV,27,4) 
    #to detect coutour of image using gaussian filter. Adjust 2 last params to match your image

    # Apply HoughLinesP method to
    # to directly obtain line end points
    lines = cv2.HoughLinesP(
                img, # Input edge image
                1, # Distance resolution in pixels
                np.pi/180, # Angle resolution in radians
                threshold=100, # Min number of votes for valid line
                minLineLength=200, # Min allowed length of line
                maxLineGap=2 # Max allowed gap between line for joining them
                )
    rows = img.shape[0]
    # Apply HoughCircles method to
    # to directly obtain line end points
    circles = cv2.HoughCircles(img, cv2.HOUGH_GRADIENT, 1, rows / 8,
                                param1=200, param2=30,
                                minRadius=100, maxRadius=1000)

    center_shape=[] #mảng lưu tâm tất cả shape 
    #----------------CIRCLE------------------------
    if circles is not None:
        circles = np.uint16(np.around(circles))
        for i in circles[0, :]:
            center = (i[0], i[1])
            # circle center
            cv2.circle(image, center, 5, (0, 100, 100), 3)
            # circle outline
            radius = i[2]
            #print(radius)
            cv2.circle(image, center, radius, (255, 0, 255), 3)
            print("The Circle Dectected: Center = (%2.2f, %2.2f), Radius = %2.2f"%(i[0], i[1], i[2]))

            center = Invert_Coor(center)
            center_shape.append(center)
    else:
        print("Do not dectect the Circle")
        center_shape.append([None, None])
  
    #---------------------RECTANGLE------------------------
    if lines is not None:
        d=[] # mảng chứa độ dài các cạnh được dectect
        d_ = []

        for i, points  in enumerate(lines):
            x1,y1,x2,y2=points[0]
            d.append([i,np.sqrt(pow((x2-x1),2)+pow((y2-y1),2))])
        d = np.array(d)

        d_=np.argsort(d[:,1],kind='quicksort') #sort từ lớn đến bé
   
        d_[:] = d_[::-1] #flip array

        lines_list =[] #mảng lưu tọa độ đoạn thẳng
        cent_list = [] #mảng lưu trung điểm đoạn thẳng

        for stt, i in enumerate(d_): #Lọc 2 cạnh đối nhau của hình vuông
            x1,y1,x2,y2=lines[i][0] #lấy tọa độ cạnh
            #tìm trung điểm cạnh
            x_av = int(np.floor(abs(abs(x1+x2))/2))
            y_av = int(np.floor(abs(abs(y1+y2))/2))
            if stt == 0: #lưu cạnh độ dài lớn nhất 
                d_1_x = x_av
                d_1_y = y_av
                cv2.line(image,(x1,y1),(x2,y2),(0,255,0),3)
                cv2.drawMarker(image, (x_av, y_av),(0,0,255), markerType=cv2.MARKER_STAR, markerSize=40, thickness=1, line_type=cv2.LINE_AA)
                # Maintain a simples lookup list for points
                lines_list.append([(x1,y1),(x2,y2)])
                cent_list.append([d_1_x,d_1_y])
            d_break = np.sqrt(pow((d_1_x-x_av),2)+pow((d_1_y-y_av),2))
            
            if d_break > 250 and d_break < 350:	#tìm cạnh đối
                cv2.line(image,(x1,y1),(x2,y2),(255,255,0),3)
                cv2.drawMarker(image, (x_av, y_av),(0,0,255), markerType=cv2.MARKER_STAR, markerSize=40, thickness=1, line_type=cv2.LINE_AA)
                # Maintain a simples lookup list for points
                lines_list.append([(x1,y1),(x2,y2)])
                cent_list.append([x_av,y_av])
                break
        #print(len(lines_list),d)
        x_cen = int(np.floor(abs(abs(cent_list[0][0]+cent_list[1][0]))/2))
        y_cen = int(np.floor(abs(abs(cent_list[0][1]+cent_list[1][1]))/2))
        cv2.drawMarker(image, (x_cen, y_cen),(255,0,255), markerType=cv2.MARKER_STAR, markerSize=40, thickness=1, line_type=cv2.LINE_AA)
        print("The rectangle dectected: Center = (%2.2f, %2.2f), Side length= %2.2f"%(x_cen, y_cen, d_break))
        Invert_Coor([x_cen,y_cen])
        center_shape.append(Invert_Coor([x_cen,y_cen]))
    else:
        print("Do not dectect the Rectangle")
        center_shape.append([None, None])

    #trả về tọa độ tâm 2 hình cách nhau bở dấu ;
    center_tmp = str(center_shape[0][0])+";"+str(center_shape[0][1])+";"+str(center_shape[1][0])+";"+str(center_shape[1][1])
    return center_tmp

#----------------------main---------------------
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("CLIENT SIDE")

try:
    client.connect( (HOST, SERVER_PORT) )
    print("client address:",client.getsockname())

    start_sig = ' '
    flag_routine = 0 
    #flag_process_img = None
    while (flag_routine==0 and start_sig != "x"):
        start_sig = input("Do you want to start the routine: \nPlease type 'Start' or 'x'")

        if start_sig == "Start": #Nếu nhận "Start"
            flag_routine = 1
            client.sendall(start_sig.encode(FORMAT)) #gui tin hieu "Start"
            print("Client has send the signal 'Start' \n --------------------")
            center_shape_ = []
            flag_process_img = ' '
            while flag_process_img != 'x' and flag_process_img != "End":
                print("wait responsible signal...")
                flag_process_img = client.recv(1024).decode(FORMAT) #Doi ABB tra ve "Done_Capture"
                if flag_process_img == "Done_Capture":
                    time.sleep(2)
                    print("Processing . . . . .")
                    center_shape_ = Processing()
                    time.sleep(0.5)
                    print("Done_pro")
                    client.sendall(center_shape_.encode(FORMAT))
                    Done_r = client.recv(1024).decode(FORMAT) #Doi ABB tra ve "Done_Routine"
                    print("Done Routine")
                    flag_process_img = "End"
                flag_routine = 0 
except:
    print("Error")

client.close();