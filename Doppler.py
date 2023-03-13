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

# Remove all files that match the pattern
for file in os.scandir(current_directory):
    if file.name.startswith("diff_") and file.name.endswith(".png"):
        os.remove(file.path)

time.sleep(1)

# Wait for the directory to be completely emptied
while any(fname.startswith("frame_") for fname in os.listdir(current_directory)):
    pass
while any(fname.startswith("diff_") for fname in os.listdir(current_directory)):
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

# The rest of your code goes here
dir_path = 'C:\\Users\\info\\PycharmProject\\FMD1\\Doppler.py'

if os.access(dir_path, os.R_OK):
    print("You have permissions to read the directory")
else:
    print("You don’t have permissions to read the directory")

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

    # use initial ROI for all frame
    roi = frame[ref_y:ref_y+ref_h, ref_x:ref_x+ref_w]

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
    img = cv2.imread(filename, cv2.IMREAD_GRAYSCALE)
    images.append(img)

# Calculate differences between adjacent images
diff_images = []
for i in range(len(images) - 1):
    diff = cv2.absdiff(images[i], images[i+1])
    diff_images.append(diff)

# Save the difference images like image
for i, diff in enumerate(diff_images):
    filename = f'diff_{i:04d}.png'
    cv2.imwrite(filename, diff)

# Show the difference images as a "video" and a video of difference
frame_rate = 50
for img, diff_img in zip(images, diff_images):
    cv2.imshow("ROI Video", img)
    cv2.imshow("Difference Image", (diff_img * 25))
    # Wait for a certain amount of time (in milliseconds) depending on the desired frame rate
    cv2.waitKey(int(1000 / frame_rate))

    if cv2.waitKey(1) == ord('q'):
        break

cv2.waitKey(0)

cap.release() # release video

cv2.destroyAllWindows() # close all windows
