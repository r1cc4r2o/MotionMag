import os
import cv2
import glob

import numpy as np
import PIL.Image as Image


# magnify the motion
def grad_shift_mag(frame, alpha=200, low=0.1, high=0.2):
    # convert to gray scale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # compute the gradient
    grad = cv2.Laplacian(gray, cv2.CV_64F)
    
    # compute the motion
    motion = np.zeros_like(grad)
    motion[grad >= low] = 1
    motion[grad >= high] = 2
    
    # magnify the motion
    result = frame.copy()
    result[motion == 1] *= alpha
    result[motion == 2] *= (alpha + 100)
    result[result > 255] = 255
    
    return result


# Read the video
cap = cv2.VideoCapture('data/baby.mp4')
    
# loop over the frames and save frames by frames in a new folder
new_folder = 'data/baby_motion/'

# check if the folder exists
if not os.path.exists(new_folder):
    os.makedirs(new_folder)
    
# loop over the frames
i = 0
while cap.isOpened():
    ret, frame = cap.read()
    if ret:
        # magnify the motion
        result = grad_shift_mag(frame)
        
        if i < 10:
            # save the result
            cv2.imwrite(new_folder + 'frame_000' + str(i) + '.jpg', result)
        elif i < 100:
            # save the result
            cv2.imwrite(new_folder + 'frame_00' + str(i) + '.jpg', result)
        elif i < 1000:
            # save the result
            cv2.imwrite(new_folder + 'frame_0' + str(i) + '.jpg', result)
        
    else:
        break
    i += 1
    

path = sorted(glob.glob('data/baby_motion/*.jpg'))

# pick a frames and save it as a video with pillow
frames = []
for p in path:
    frame = Image.open(p)
    frames.append(frame)


frames[0].save('data/baby_motion_frame_dif.gif', format='GIF', append_images=frames[1:], save_all=True, duration=100, loop=0)