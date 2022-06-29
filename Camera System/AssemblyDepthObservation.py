from turtle import shape
import cv2
import numpy as np

import pyk4a
#from helpers import colorize
from pyk4a import Config, PyK4A
from sklearn.preprocessing import Binarizer
import time
import matplotlib.pyplot as plt


def get_colour(hsv): 
    green_lower= np.array([36, 65, 87])
    green_upper= np.array([102, 255, 247])
    red_lower=np.array([108, 165, 18])
    red_upper=np.array([179, 230, 215])
    lblue_lower=np.array([59, 63, 191])
    lblue_upper= np.array([109, 255, 253])
    yellow_lower=np.array([13, 200, 188])
    yellow_upper=np.array([103, 255, 253])
    white_lower=np.array([64, 11, 204])
    white_upper=np.array([156, 142, 253])
    blue_lower=np.array([108, 163, 127])
    blue_upper=np.array([129, 255, 180])
    orange_lower=np.array([0, 147, 1])
    orange_upper=np.array([11, 239, 236])

    if (green_lower[0]<= hsv[0]<= green_upper[0]) and (green_lower[1]<= hsv[1]<= green_upper[1]) and (green_lower[2]<= hsv[2]<= green_upper[2]):
        return 'green'
    elif (red_lower[0]<= hsv[0]<= red_upper[0]) and (red_lower[1]<= hsv[1]<= red_upper[1]) and (red_lower[2]<= hsv[2]<= red_upper[2]):
        return 'red'
    elif (lblue_lower[0]<= hsv[0]<= lblue_upper[0]) and (lblue_lower[1]<= hsv[1]<= lblue_upper[1]) and (lblue_lower[2]<= hsv[2]<=lblue_upper[2]):
        return 'light_blue'
    elif (yellow_lower[0]<= hsv[0]<= yellow_upper[0]) and (yellow_lower[1]<= hsv[1]<= yellow_upper[1]) and (yellow_lower[2]<= hsv[2]<= yellow_upper[2]):
        return 'yellow'
    elif (white_lower[0]<= hsv[0]<= white_upper[0]) and (white_lower[1]<= hsv[1]<= white_upper[1]) and (white_lower[2]<= hsv[2]<= white_upper[2]):
        return 'white'
    elif (blue_lower[0]<= hsv[0]<= blue_upper[0]) and (blue_lower[1]<= hsv[1]<= blue_upper[1]) and (blue_lower[2]<= hsv[2]<= blue_upper[2]):
        return 'blue'
    elif (orange_lower[0]<= hsv[0]<= orange_upper[0]) and (orange_lower[1]<= hsv[1]<= orange_upper[1]) and (orange_lower[2]<= hsv[2]<= orange_upper[2]):
        return 'orange'

def getLegoLabels(area):
    if 400<= area<= 1399:
        return 'Small Lego'
    elif 1400 <= area <= 2300: #changed values here
        return 'Medium Lego'
    elif 2301 <= area <= 3100:
        return 'Large Lego'


#### Main ####
k4a = PyK4A(Config(color_resolution=pyk4a.ColorResolution.RES_720P, depth_mode=pyk4a.DepthMode.NFOV_UNBINNED,))
k4a.start()

# create figure
fig = plt.figure(figsize=(10, 7))
  
# setting values to rows and column variables
rows = 2
columns = 2

capture1 = k4a.get_capture()
#capture1= capture1[339:760,921:1234]  #for detection [335:763,504:1234]

#acquiring depth map
if np.any(capture1.transformed_depth):
    depth_map1= capture1.transformed_depth
    depth_map1=depth_map1[272:(272+284),583:(583+265)]
    
#acquiring colour image
if capture1.color is not None:
    colour_img1= capture1.color[:,:,:3]
    colour_img1=colour_img1[272:(272+284),583:(583+265)]

# roi = cv2.selectROI(colour_img1)
# print(roi)

counter=0
while counter<=30:
    time.sleep(1)
    counter += 1.
    print(counter)

capture2 = k4a.get_capture()

#acquiring depth map
if np.any(capture2.transformed_depth):
    depth_map2= capture2.transformed_depth
    depth_map2=depth_map2[272:(272+284),583:(583+265)]
    
#acquiring colour image
if capture2.color is not None:
    colour_img2= capture2.color
    colour_img2=colour_img2[272:(272+284),583:(583+265)]

#depth based computation to create mask
depth_diff=abs(depth_map2-depth_map1)
length_diff= depth_diff.shape
r=length_diff[0]
c=length_diff[1]
median_diff=np.median(depth_diff[depth_diff>0])
min_diff=np.min(depth_diff[depth_diff>0])
max_diff=np.max(depth_diff[depth_diff>0])

mask=np.zeros(depth_diff.shape,dtype="uint8")
for i in range(0,r):
    for j in range(0,c):
        if depth_diff[i,j]>min_diff + 10:
            mask[i,j]=255
            
mask_rgb = cv2.cvtColor(mask, cv2.COLOR_BGR2RGB)
colour_img2_rgb=cv2.cvtColor(colour_img2, cv2.COLOR_BGR2RGB)
colour_img1_rgb=cv2.cvtColor(colour_img1, cv2.COLOR_BGR2RGB)
masked=cv2.bitwise_and(colour_img2, colour_img2, mask=mask)
masked_rgb = cv2.cvtColor(masked, cv2.COLOR_BGR2RGB)
masked_hsv = cv2.cvtColor(masked, cv2.COLOR_RGB2HSV)


masked_gray = cv2.cvtColor(masked, cv2.COLOR_BGR2GRAY)

#matching contours
contours, hierarchy = cv2.findContours(masked_gray, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
contours = sorted(contours, key=cv2.contourArea, reverse=True)[:8] #top 8 contours(can be changed as per requirement)
mask_contours = cv2.drawContours(masked, contours, -1, (0, 255, 0), 2)


assembly_colour=[]
assembly_area=[]
assembly_legolabel=[]
assembly_hsv_val=[]
for idx, cnt in enumerate(contours):
    if cv2.contourArea(cnt) >400: # filter small contours
        area=cv2.contourArea(cnt)
        assembly_area.append(area)
        assembly_legolabel.append(getLegoLabels(area))
        M = cv2.moments(cnt)
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
        center= (cX,cY)
        #cv2.putText(masked, "#{}".format(i + 1), (cX - 20, cY), cv2.FONT_HERSHEY_SIMPLEX,5.0, (255, 255, 255), 2)
        x,y,w,h = cv2.boundingRect(cnt)
        #print('Debug =',masked_hsv[cY+2:cY+3,cX+2:cX+3])
        hsv_frame =cv2.mean(masked_hsv[cY+2:cY+3,cX+2:cX+3])
        assembly_hsv_val.append(hsv_frame)
        hsv_label= get_colour(hsv_frame[:3])
        assembly_colour.append(hsv_label)
        

fig.add_subplot(rows, columns, 1)
  
# showing image
plt.imshow(colour_img1_rgb)
plt.axis('off')
plt.title("Original Frame")
  
# Adds a subplot at the 2nd position
fig.add_subplot(rows, columns, 2)
  
# showing image
plt.imshow(colour_img2_rgb)
plt.axis('off')
plt.title("Updated Frame")
  
# Adds a subplot at the 3rd position
fig.add_subplot(rows, columns, 3)

# showing image
plt.imshow(mask_rgb)
plt.axis('off')
plt.title("Difference Mask")
  
# Adds a subplot at the 4th position
fig.add_subplot(rows, columns, 4)
  
# showing image

plt.imshow(masked_rgb)
plt.axis('off')
plt.title("Applied Mask")

#Output on Terminal
print("assembly color:")
print(assembly_colour)
print("assembly area:")
print(assembly_area)
print("assembly hsv values:")
print(assembly_hsv_val)
print("assembly lego label:")
print(assembly_legolabel)

plt.savefig('image_step2.jpg')
plt.show()

cv2.waitKey()
cv2.destroyAllWindows()
k4a.stop
        

