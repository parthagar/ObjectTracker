# ObjectTracker
Track objects in your webcam feed. 

### Requirements
You can install Conda for python which resolves all the dependencies for this project
or run 
`pip install requirements.txt`

### Description
Run with object_colour which finds the hsv colour of the object you want to track or if you know the hsv colour feed it directly into the program.

### Execution
After reproducing the repo in your device, to run the code,
Type `python track.py` for tracking by finding the hsv colour value of the object you want to track.

### Functionalities
1) Search for hsv value by selecting object region

### To-do
- [x] Threaded video for faster processing
- [x] Show FPS in feed
- [ ] Stabilization/improve hsv value thresholding

### References
1) https://www.pyimagesearch.com/2015/09/14/ball-tracking-with-opencv/

Thanks to Adrian Rosebrock for inspiring me!
