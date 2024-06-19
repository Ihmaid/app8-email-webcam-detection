import cv2
import time
from emailing import send_email
import glob

# Create a camera object
video = cv2.VideoCapture(0)
# Let the camera starts sleeping for 1 second
time.sleep(1)

# Initialize a None variable to get the first frame at the loop
first_frame = None
# This list is used to find the moment when the object gets out from the camera
# to use this moment to send the email
status_list = []
count = 1

while True:
    # While there is no object at the video, the status is 0
    status = 0
    # The read method returns the state of the video (True or False) and the
    # frame, which is a NumPy matrix
    check, frame = video.read()

    # Take the actual frame and transform into grayscale to reduce the matrices
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # Take the gray frame and blurs it to reduce the noise and the precision
    gray_frame_gau = cv2.GaussianBlur(gray_frame, (21, 21), 0)

    # Guards the first frame of the video at first_frame
    if first_frame is None:
        first_frame = gray_frame_gau

    # Do the difference of the first frame, which is the base scenario with
    # no objects , and the subsequents frames, trying to find some change
    delta_frame = cv2.absdiff(first_frame, gray_frame_gau)

    # If a pixel from delta_frame has more than 30 of value it will be
    # reassigned to 255, which is white color, that means that what is black
    # isn`t an object. The threshold function returns a list, then we get the
    # 2 item of this list
    thresh_frame = cv2.threshold(delta_frame, 100, 255, cv2.THRESH_BINARY)[1]
    # Intensify the effect of blur and grayscale
    dil_frame = cv2.dilate(thresh_frame, None, iterations=2)

    # Extract the contour of the white pieces at the frame, and these pieces
    # are meant to be the possible objects. Returns a list of contour
    contours, check = cv2.findContours(dil_frame, cv2.RETR_EXTERNAL,
                                       cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours:
        # If the contour area is less than 12500, it is too small to be
        # considered as object. That removes the light spots
        if cv2.contourArea(contour) < 13500:
            continue

        # The function returns the measures of a rectangle that covers the
        # contour
        x, y, w, h = cv2.boundingRect(contour)
        rectangle = cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 3)
        if rectangle.any():
            status = 1
            cv2.imwrite(f"images/{count}.png", frame)
            count += 1
            all_images = glob.glob("images/*.png")
            index = int(len(all_images) / 2)
            image_with_object = all_images[index]

    # Creates a list of 2 items to identify when the status change from 1 to 0,
    # and this moment the object got out of the camera
    status_list.append(status)
    status_list = status_list[-2:]
    if status_list[0] == 1 and status_list[1] == 0:
        send_email(image_with_object)

    cv2.imshow("Video", frame)

    # Defines a keycap to exit the video tab
    key = cv2.waitKey(1)
    if key == ord("q"):
        break

video.release()
