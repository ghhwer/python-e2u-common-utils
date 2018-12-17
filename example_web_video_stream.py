import cv2
import time
from common_utils.web_video_stream import mjpg_stream

mjpg = mjpg_stream(ip='127.0.0.1',fileName='stream.mjpg',port=8080,supressDebug=False)

try:
    while True:
        # Read until video is completed
        while True:
            cap = cv2.VideoCapture('footage.mp4')
            if (cap.isOpened()== False):
              print("Error opening video stream or file")
            while(cap.isOpened()):
              # Capture frame-by-frame
              ret, frame = cap.read()
              if ret == True:
                  # Pass frame to web vieo stream
                  mjpg.update_frame(frame)
                  time.sleep(0.001)
              else:
                  break
            cap.release()
except KeyboardInterrupt:
	print ''
	print "Stopping Services..."

# Closes server
mjpg.disconnect()
