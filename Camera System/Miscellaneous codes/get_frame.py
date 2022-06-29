import cv2
import os

" This code is used to extract frames from a video"
vidcap = cv2.VideoCapture('path')
#success,image = vidcap.read()
print('hello1')
path= 'Path to save'
count = 0
iter=0
print('hello2')

while vidcap.isOpened():
    print('hello')
    ret, frame = vidcap.read()

    if ret:
        iter+=1
        cv2.imwrite(os.path.join(path+str(iter)+".jpg"), frame)
        count += 10 # i.e. at 30 fps, this advances one second
        print('Read a new frame_'+str(iter)+':', ret)
        vidcap.set(cv2.CAP_PROP_POS_FRAMES, count)
    else:
        vidcap.release()
        break