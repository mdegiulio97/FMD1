import numpy as np
import cv2

# Open video
cap = cv2.VideoCapture('C:\\Users\\info\\OneDrive\\Desktop\\FMD\\video\\Braq10.mp4')


# read first frame
ret, frame = cap.read()
# show first frame
cv2.imshow('Seleziona una ROI', frame)
# select ROI with mouse
x, y, w, h = cv2.selectROI('Seleziona una ROI', frame, False)
# Save the coordinates of the first ROI as a reference
ref_x, ref_y, ref_w, ref_h = x, y, w, h

#  close select ROI windows
cv2.destroyAllWindows()

roi_images = []

while True:
    # read a video's frame
    ret, frame = cap.read()
    # verifica lettura frame
    if not ret:
        break

    # create a mask for select ROI
    mask = np.zeros_like(frame)
    mask[ref_y:ref_y + ref_h, ref_x:ref_x + ref_w] = 255
    # Extract the part of the frame that is within the ROI
    roi = cv2.bitwise_and(frame, mask)
    #Resizes the extracted ROI initially based on the size of the selected ROI later
    roi = cv2.resize(roi, (ref_w, ref_h))
    # use initial ROI for all frame 
    frame[ref_y:ref_y+ref_h, ref_x:ref_x+ref_w] = roi
    # draw a ROI on current ROI
    cv2.rectangle(frame, (ref_x, ref_y), (ref_x + ref_w, ref_y + ref_h), (0, 255, 0), 2)

    # add image to array
    roi_images.append(roi)

    #show frame
    cv2.imshow('Video with ROI', frame)

    # exit input
    if cv2.waitKey(1) == ord('q'):
        break

cap.release() # relese video

# concatenate the images of the array
output_image = np.concatenate(roi_images, axis=1)

# show final image
cv2.imshow('Output Image', output_image)
cv2.waitKey(0)

cv2.destroyAllWindows() # close all windows
