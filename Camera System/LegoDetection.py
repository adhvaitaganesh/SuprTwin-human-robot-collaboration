"This code is used to detect lego blocks and their properties using hsv thresholding"
import numpy as np 
import cv2
import pyk4a
import time
#from helpers import colorize
from pyk4a import Config, PyK4A

def get_colour(hsv):
    "Identify ROI based on HSV values"
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
    #elif (dgreen_lower[0]<= hsv[0]<= dgreen_upper[0]) and (dgreen_lower[1]<= hsv[1]<= dgreen_upper[1]) and (dgreen_lower[2]<= hsv[2]<= dgreen_upper[2]):
        #return 'dark green'
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
    "Classify Lego blocks based on Area of contours"
    if 400<= area<= 1399:
        return 'Small Lego'
    elif 1400 <= area <= 2300: #changed values here
        return 'Medium Lego'
    elif 2301 <= area <= 3100:
        return 'Large Lego'

def sort_contours(cnts, method="left-to-right"):  #sorting contours
	# initialize the reverse flag and sort index
	reverse = False
	i = 0
	# handle if we need to sort in reverse
	if method == "right-to-left" or method == "bottom-to-top":
		reverse = True
	# handle if we are sorting against the y-coordinate rather than
	# the x-coordinate of the bounding box
	if method == "top-to-bottom" or method == "bottom-to-top":
		i = 1
	# construct the list of bounding boxes and sort them from top to
	# bottom
	boundingBoxes = [cv2.boundingRect(c) for c in cnts]
	(cnts, boundingBoxes) = zip(*sorted(zip(cnts, boundingBoxes),
		key=lambda b:b[1][i], reverse=reverse))
	# return the list of sorted contours and bounding boxes
	return (cnts, boundingBoxes)


### Main ###
k4a=  PyK4A(Config(color_resolution=pyk4a.ColorResolution.RES_720P, depth_mode=pyk4a.DepthMode.NFOV_UNBINNED,))

k4a.start()


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


keys= ['ID',"Lego_Label","Colour_Label","Area", "Position(x, y coordinates)"]
id=0
oldCenter=[]
oldID=[]
step=1

capture = k4a.get_capture()
# if capture.color is not None:
#     frame=capture.color
# roi = cv2.selectROI(frame)
#print(roi)
while(True):
    
    # Capture the video frame
    capture = k4a.get_capture()
    
    if capture.color is not None:
        frame=capture.color
        frame=frame[230:(230+347),335:(335+214)]

    #create empty dictionary for values for assembly
    data_dict=dict.fromkeys(keys)

    frame_copy= frame[:,:,:3]
    
    hsv = cv2.cvtColor(frame_copy, cv2.COLOR_BGR2HSV)

    mask_green= cv2.inRange(hsv, green_lower, green_upper)
    mask_red= cv2.inRange(hsv, red_lower, red_upper)
    mask_lblue= cv2.inRange(hsv, lblue_lower, lblue_upper)
    mask_yellow= cv2.inRange(hsv, yellow_lower, yellow_upper)
    mask_white= cv2.inRange(hsv, white_lower,white_upper)
    mask_blue= cv2.inRange(hsv,blue_lower, blue_upper)
    mask_orange= cv2.inRange(hsv, orange_lower, orange_upper)

    final_mask= mask_green+mask_red+mask_lblue+mask_yellow+mask_white+mask_blue+mask_orange

    result = cv2.bitwise_and(frame, frame, mask=final_mask)
    cv2.imshow('Masked',final_mask)
    g = result[:,:,1]
    filter = g.copy()

    ret,mask = cv2.threshold(filter,10,255, cv2.THRESH_BINARY)
    mask = cv2.medianBlur(mask,5,0)

    #finding contour data
    contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:7] #getting top 10 contours
    contours,_=sort_contours(contours)
    image = cv2.drawContours(frame, contours, -1, (0, 255, 0), 2)
    
    area_contour=[]
    lego_labels=[]
    center=[]
    colour_hsv=[]
    colour_labels=[]
    depth=[]
    unitID=[] #static IDs to all Lego Identified
    
    for idx, cnt in enumerate(contours):
         
         if cv2.contourArea(cnt) >800: # filter small contours
           
            area=cv2.contourArea(cnt)
            area_contour.append(area)
            lego_labels.append(getLegoLabels(area))
            x,y,w,h = cv2.boundingRect(cnt) # offsets - with this you get 'mask'
            M = cv2.moments(cnt)
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            center_val=(cX,cY)

            if step!=1:
                if center_val in oldCenters:
                    idx= oldCenters.index(center_val)
                    id= oldID[idx]
                else:
                    id+=1
            else:
                id+=1      
            
            center.append(center_val)
            radius = 2
            
            avg_col_bgr=frame_copy[y:y+h,x:x+w]
            hsv_frame = cv2.mean(hsv[cY+2:cY+3,cX+2:cX+3])
            colour_hsv.append(hsv_frame)
            hsv_label= get_colour(hsv_frame)
            colour_labels.append(hsv_label)
            unitID.append(id)

    data_dict["ID"]=unitID
    data_dict["Lego_Label"]=lego_labels
    data_dict["Colour_Label"]=colour_labels
    data_dict["Area"]=area_contour
    data_dict["Position(x, y coordinates)"]=center
    
    oldID=unitID
    oldCenters=center
    id=max(unitID)
    
    print('Step='+str(step))
    print(data_dict)
    cv2.imshow('img',frame_copy) 
    key=cv2.waitKey(5)
    if key != -1:
            cv2.destroyAllWindows()
            break
    
    time.sleep(5)
    step=step+1
k4a.stop()  


    

    



  