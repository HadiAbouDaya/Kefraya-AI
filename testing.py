import cv2
import numpy as np
import glob
import random
import os
def crop_one_picture(path,filename):
    img=cv2.imread(os.path.join(path,filename),-1)##Read the color image, the transparency of the image (alpha channel) is ignored, the default parameter; grayscale image; read the original image, including the alpha channel; can be expressed as 1, 0, -1
    width, height, channel = img.shape
    rows=int(width/4)
    cols=int(height/4)
    sum_rows=img.shape[0]   #height
    sum_cols=img.shape[1]    #width
    save_path=path+"\\crop_{0}\\".format(filename)  #Saved path
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    print("Cropped {0} column pictures, {1} row pictures.".format(int(sum_cols/cols),int(sum_rows/rows))) 

    for i in range(int(sum_cols/cols)):
        print((int(sum_cols/cols)))
        for j in range(int(sum_rows/rows)):
            print(int(sum_cols/cols))
            cv2.imwrite(save_path+os.path.splitext(filename)[0]+'_'+str(j)+'_'+str(i)+os.path.splitext(filename)[1],img[j*rows:(j+1)*rows,i*cols:(i+1)*cols,:])
            #print(path+"\crop\\"+os.path.splitext(filename)[0]+'_'+str(j)+'_'+str(i)+os.path.splitext(filename)[1])
    print("Cropping completed, get {0} pictures.".format(int(sum_cols/cols)*int(sum_rows/rows)))
    print("File saved in {0}".format(save_path))
def file_name(root_path,picturetype):
    filename=[]
    for root,dirs,files in os.walk(root_path):
        for file in files:
            if os.path.splitext(file)[1]==picturetype:
                filename.append(os.path.join(root,file))
    return filename
def merge_picture(num_of_cols,num_of_rows):
    global path
    global new
    global filename
    namee=file_name(new,".tif")
    shape=cv2.imread(namee[0]).shape  
    cols=shape[1]
    rows=shape[0]
    channels=shape[2]
    dst=np.zeros((rows*num_of_rows,cols*num_of_cols,channels),np.uint8)
    for i in range(len(namee)):
        img=cv2.imread(namee[i],-1)
        cols_th=int(namee[i].split("_")[-1].split('.')[0])
        rows_th=int(namee[i].split("_")[-2])
        roi=img[0:rows,0:cols,:]
        dst[rows_th*rows:(rows_th+1)*rows,cols_th*cols:(cols_th+1)*cols,:]=roi
    cv2.imwrite(os.path.join(path,"result_"+filename),dst)
def label(net,classes,images_path,choice,row,col,x,y):
                global new
                global filename
                global path
                global numb
                layer_names = net.getLayerNames()
                output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]
                colors =np.array([[ 43.83397456,  87.67468706, 0],[164.95796038,  57.24219913, 0]])
                # Insert here the path of your images
                random.shuffle(images_path)
                # loop through all the images
                for img_path in images_path:
                    
                    # Loading image
                    img = cv2.imread(img_path)
                    img = cv2.resize(img, None, fx=x, fy=y)
                    height, width, channels = img.shape
                    
                    # Detecting objects
                    blob = cv2.dnn.blobFromImage(img, 0.00392, (416, 416), (0, 0, 0), True, crop=False)

                    net.setInput(blob)
                    outs = net.forward(output_layers)

                    # Showing informations on the screen
                    class_ids = []
                    confidences = []
                    boxes = []
                    for out in outs:
                        for detection in out:
                            scores = detection[5:]
                            class_id = np.argmax(scores)
                            confidence = scores[class_id]
                            if confidence > 0.3:
                                # Object detected
                                #print(class_id)
                                center_x = int(detection[0] * width)
                                center_y = int(detection[1] * height)
                                w = int(detection[2] * width)
                                h = int(detection[3] * height)

                                # Rectangle coordinates
                                x = int(center_x - w / 2)
                                y = int(center_y - h / 2)

                                boxes.append([x, y, w, h])
                                confidences.append(float(confidence))
                                class_ids.append(class_id)

                    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
                    font = cv2.FONT_HERSHEY_PLAIN
                    
                    for i in range(len(boxes)):
                        if i in indexes:
                            x, y, w, h = boxes[i]
                            label = str(classes[class_ids[i]])
                            print(class_ids[i])
                            color = colors[class_ids[i]]
                            numb=numb+1
                            cv2.rectangle(img, (x, y), (x + w, y + h),color, 1)
                            cv2.putText(img, label, (x, y + 30), font, 1, color, 1)
                    print(numb)
                    if choice==1:
                        cv2.imwrite(os.path.join(path,"result_"+filename),img)
                    else:
                        cv2.imwrite(os.path.join(new,"vertical"+"_"+str(row)+"_"+str(col)+".tif"),img)
                        key = cv2.waitKey(0)
            
def test(choice,path,filename):

    net = cv2.dnn.readNet(os.path.join(path,"yolov3_training_last.weights"), os.path.join(path,"yolov3_testing.cfg"))

    # Name custom object
    classes = ["plant","no_plant"]
    if choice==1:
       images_path = glob.glob(os.path.join(path,filename))
       label(net,classes,images_path,choice,0,0,4,4) 
    if choice==2:
        for row in range(4):
                for col in range (4):        
                # Images path
                    images_path = glob.glob(os.path.join(path,"crop_"+filename+"/vertical"+"_"+str(row)+"_"+str(col)+".tif"))
                    label(net,classes,images_path,choice,row,col,1,1)
                    
                    
def menu():
    choice=int(input("If you consider that the size of your plants small press 1:/nIf you consider the size of your plants big press 2:/n"))
    return choice
path=r"C:\Users\LENOVO\Desktop\stage\the code"
filename=input("insert filename: ")
img=cv2.imread(os.path.join(path,filename),-1)
width, height, channel = img.shape
choice=menu()
new=os.path.join(path,"new_"+filename)
numb=0
if (width>430 and height>430) and choice==2:
    try:
        os.makedirs(new)
    except FileExistsError:
        pass
    crop_one_picture(path,filename)
    test(2,path,filename)
    merge_picture(4,4)
elif (width<=430 and height<=430) and choice==1:
    test(1,path,filename)
elif choice!=1 and choice!=2:
    print("you didn't select one of the 2 choices")
else:
    print("the selected choice doesn't match the size of the image")
