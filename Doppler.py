import numpy as np
import cv2
import glob2 as glob
import os
import time

# Set the current directory
current_directory = os.getcwd()

# Define the pattern to match
pattern = "frame_*.png"

# Remove all files that match the pattern
for file in os.scandir(current_directory):
    if file.name.startswith("frame_") and file.name.endswith(".png"):
        os.remove(file.path)

# Wait for the directory to be completely emptied
while any(fname.startswith("frame_") for fname in os.listdir(current_directory)):
    pass

# Wait for the directory to be completely emptied
while True:
    # Check if there are any files that match the pattern
    if any(fname.startswith("frame_") for fname in os.listdir(current_directory)):
        print("the directory doesn't empty.")
        # Wait for one second and check again
        time.sleep(1)
    else:
        print("the directory is empty")
        # No more files matching the pattern, break out of the loop
        break

# At this point, the directory should be empty

time.sleep(1)

# The rest of your code goes here

# Open video
cap = cv2.VideoCapture('C:\\Users\\info\\OneDrive\\Desktop\\FMD\\video\\Braq10.mp4')

# read first frame
ret, frame = cap.read()
# show first frame
cv2.imshow('Select ROI', frame)
# select ROI with mouse
x, y, w, h = cv2.selectROI('Select ROI', frame, False)
# Save the coordinates of the first ROI as a reference
ref_x, ref_y, ref_w, ref_h = x, y, w, h

#  close select ROI windows
cv2.destroyAllWindows()

counter = 0
while True:
    # read a video's frame
    ret, frame = cap.read()
    # verify read frame
    if not ret:
        break

    # create a mask for select ROI
    mask = np.zeros_like(frame)
    mask[ref_y:ref_y + ref_h, ref_x:ref_x + ref_w] = 255
    # Extract the part of the frame that is within the ROI
    roi = cv2.bitwise_and(frame, mask)
    # Resizes the extracted ROI initially based on the size of the selected ROI later
    roi = cv2.resize(roi, (ref_w, ref_h))
    # use initial ROI for all frame 
    frame[ref_y:ref_y+ref_h, ref_x:ref_x+ref_w] = roi

    # Save the ROI like image
    filename = f'frame_{counter:04d}.png'
    cv2.imwrite(filename, roi)
    counter += 1

    # draw a ROI on current ROI
    cv2.rectangle(frame, (ref_x, ref_y), (ref_x + ref_w, ref_y + ref_h), (0, 255, 0), 2)

    # show frame
    cv2.imshow('Video with ROI', frame)

    # exit input
    if cv2.waitKey(1) == ord('q'):
        break

# Recovers image file names starting with "frame_" and ending with ". png"
image_files = sorted(glob.glob("frame_*.png"))

# Load images from file name list
images = []
for filename in image_files:
    images.append(cv2.imread(filename))

# Concatenate images horizontally
result = cv2.hconcat(images)

# Show the resulting image
cv2.imshow('Concatenated Image', result)

cv2.waitKey(0)

cap.release() # release video

cv2.destroyAllWindows() # close all windows
