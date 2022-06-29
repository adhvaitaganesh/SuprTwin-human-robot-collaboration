import cv2
import os

"Another code to save frames from image with custom count"
vidcap = cv2.VideoCapture(r'Path')
success,image = vidcap.read()
#print(success)
path= 'Path to save'
count = 0
iter =  1550 #change first
while success:
  iter+=1
  #print("hello")
  cv2.imwrite(str(path)+str(iter)+".jpg", image)    #save frame as JPEG file      
  count += 40 # i.e. at 30 fps, this advances one second
  vidcap.set(cv2.CAP_PROP_POS_FRAMES, count)
  success,image = vidcap.read()
  print('Read a new frame'+str(iter)+':', success)
  #count += 1