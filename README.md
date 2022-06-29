# SuprTwin-human-robot-collaboration
Repository containing code for better human-robot collaboration in an industrial assemby line. Implemeted using traditional computer vision, deep learning and RoboExpert for simulation

**Project discription:**
The project pipeline is designed in three stages. 
* First, live detection and tracking of human hands using depth map obtained from Mircrosoft azure kinect-V2 camera.
* Second, Lego block detection and Assembly Observation using HSV thresholding and depth-based background substraction.
* Third, Simulation of the whole assembly environment using Seimens RoboExpert.

**Module description :**

**Human hand detection:**
* Deep-learng based approch
* Implemented using Faster RCNN with a resnet50 backbone. 
* Dataset: Dataset : MSRA Hands - https://jimgmysuen.github.io/txt/cvpr14_MSRAHandTrackingDB_readme.txt 
  MSRA Hands is a dataset for hand tracking. In total 6 subjects' right hands are captured using Intel's Creative Interactive Gesture Camera. Each subject   is asked to make various rapid gestures in a 400-frame video sequence. 
  Each frame contains depth map of size 320 X 240 (only D channel) of a single hand in various poses. And location of 21 key points for each frame.
* Training : The model is trained on a CPU for 37 epochs, which took 40 hrs.Batch-training was used, with batch-size being 10 frames. 
* Input data preprocessing: depth based background subtraction.
* Output: hand detection (boolean) and keypoint localization if the detection result is true.

**Human hand tracking:**
* Custom tracking algorithm, by iteratively observing relative distance between hand and objects (in this case lego blocks) 
* Predics ID of the object which human is trying to grab.

Camera systems composes of the following two unit: 
**Lego Detection **
* Creation of HSV database and contour area database to detect Lego colour and Lego Label
* Setting of Region of Interest to denote the Lego Block detection.
* Create a Custom Mask to identify different Lego Blocks and find contours and center.
* Create a dictionary of Lego blocks information containing Unit ID, Center, Depth, Lego Label, etc and compare with the dictionary after Human intervention to find missing IDs.

**Assembly Area Perception **
* Reusing HSV database and contour area database to detect Lego colour and Lego Label.
* Setting of Region of Interest to denote the Assembly Area detection and collecting Depth maps before and after human intervention at every step.
* Compare depth maps before and after human intervention to create a mask of newly added components and use contour detection.
* Get the characteristics of the newly added blocks and compare to the color and area values of IDs missing after human intervention to confirm objects removed from Lego Blocks Area are placed in Assembly area.

 
