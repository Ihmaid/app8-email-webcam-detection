import cv2
import time
from emailing import send_email

# Create a camera object
video = cv2.VideoCapture(0)
# Let the camera starts sleeping for 1 second
time.sleep(1)

first_frame = None

while True:
    check, frame = video.read()
    # Take the actual frame and transform into grayscale to reduce the matrices
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # Take the gray frame and blurs it to reduce the noise and the precision
    gray_frame_gau = cv2.GaussianBlur(gray_frame, (21, 21), 0)

    if first_frame is None:
        first_frame = gray_frame_gau

    delta_frame = cv2.absdiff(first_frame, gray_frame_gau)
    # If a pixel from delta_frame has more than 30 of value it will be
    # reassigned to 255, which is white color. The threshold function returns
    # a list, then we get the 2 item of this list
    thresh_frame = cv2.threshold(delta_frame, 100, 255, cv2.THRESH_BINARY)[1]
    dil_frame = cv2.dilate(thresh_frame, None, iterations=2)

    contours, check = cv2.findContours(dil_frame, cv2.RETR_EXTERNAL,
                                       cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        if cv2.contourArea(contour) < 12500:
            continue
        x, y, w, h = cv2.boundingRect(contour)
        rectangle = cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 3)
        if rectangle:
            send_email()
    cv2.imshow("Video", frame)


    key = cv2.waitKey(1)

    if key == ord("q"):
        break

video.release()
