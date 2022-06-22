# SuprTwin-human-robot-collaboration
Repository containing code for better human-robot collaboration in an industrial assemby line. Implemeted using traditional computer vision, deep learning and RoboExpert for simulation

**Project discription:**
The project pipeline is designed in three stages. 
* First, live detection and tracking of human hands using depth map obtained from Mircrosoft azure kinect-V2 camera.
* Second, Lego block detection and localization using HSV thresholding.
* Third, Simulation of the whole assembly environment using Seimens RoboExpert.

Module description : 

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


**Results:**
 
