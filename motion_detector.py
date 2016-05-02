#!/usr/bin/env python

# Adapted from http://www.pyimagesearch.com/2015/05/25/basic-motion-detection-and-tracking-with-python-and-opencv/
# includes http://www.pyimagesearch.com/2016/02/22/writing-to-video-with-opencv/
# import the necessary packages
import argparse
import datetime
import imutils
import time
import cv2
import numpy as np

video_counter=1
is_video_init=False

def video_name(video_counter):
    video_name='test'+str(video_counter)+'.avi'
    return video_name

def init_video_recorder(h,w,fps):
    fourcc = cv2.cv.FOURCC(*'DIVX')
    zeros = None
    print "Starting video recording: " + video_name(video_counter)
    writer = cv2.VideoWriter(video_name, fourcc, fps, (w, h), True)
    zeros = np.zeros((h, w), dtype="uint8")
    return writer

def deinit_video_recorder(writer):
    print "Stoping video recording"
    writer.release()
    is_video_init=False
    writer = None

def transfer_file(filename):
    #request to connect to storage server
    
if __name__ == "__main__": 
    # construct the argument parser and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-v", "--video", help="path to the video file")
    ap.add_argument("-a", "--min-area", type=int, default=500, help="minimum area size")
    args = vars(ap.parse_args())
    writer = None
     
    # if the video argument is None, then we are reading from webcam
    if args.get("video", None) is None:
        camera = cv2.VideoCapture(0)
        time.sleep(0.25)
     
    # otherwise, we are reading from a video file
    else:
        camera = cv2.VideoCapture(args["video"])
     
    # initialize the first frame in the video stream
    firstFrame = None
    
    #GET FPS
    fps=camera.get(cv2.cv.CV_CAP_PROP_FPS)
    
    # loop over the frames of the video
    while True:
        # grab the current frame and initialize the occupied/unoccupied
        # text
        (grabbed, frame) = camera.read()
        text = "Unoccupied"

        # if the frame could not be grabbed, then we have reached the end
        # of the video
        if not grabbed:
            break
        
        # resize the frame, convert it to grayscale, and blur it
        frame_resized = imutils.resize(frame, width=500)
        gray = cv2.cvtColor(frame_resized, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)

        # if the first frame is None, initialize it
        if firstFrame is None:
            firstFrame = gray
            continue
		
        # compute the absolute difference between the current frame and
        # first frame
        frameDelta = cv2.absdiff(firstFrame, gray)
        thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]
     
        # dilate the thresholded image to fill in holes, then find contours
        # on thresholded image
        thresh = cv2.dilate(thresh, None, iterations=2)
        (cnts, _) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE)

        # loop over the contours
        for c in cnts:
            # if the contour is too small, ignore it
            if cv2.contourArea(c) < args["min_area"]:
                continue
     
            # compute the bounding box for the contour, draw it on the frame,
            # and update the text
            (x, y, w, h) = cv2.boundingRect(c)
            cv2.rectangle(frame_resized, (x, y), (x + w, y + h), (0, 255, 0), 2)
            text = "Occupied"
        
        #Intrusion detected!    
        if text=="Occupied" and is_video_init==False:
            (h, w) = frame.shape[:2]
            writer=init_video_recorder(h,w,fps)
            is_video_init=True
        #During intrusion we record
        if text=="Occupied":
            writer.write(frame)
        #No longer intrusion - We store and transfer
        if text=="Unoccupied" and is_video_init==True:
            deinit_video_recorder(writer)
            transfer_file(video_name(video_counter))
            is_video_init=False
            video_counter+=1
            
        # draw the text and timestamp on the frame
        cv2.putText(frame_resized, "Room Status: {}".format(text), (10, 20),
            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        cv2.putText(frame_resized, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),
            (10, frame_resized.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)

	    # show the frame and record if the user presses a key
        cv2.imshow("Security Feed", frame_resized)
        cv2.imshow("Thresh", thresh)
        cv2.imshow("Frame Delta", frameDelta)
        key = cv2.waitKey(1) & 0xFF

        # if the `q` key is pressed, break from the lop
        if key == ord("q"):
            break
     
    # cleanup the camera and close any open windows
    camera.release()
    cv2.destroyAllWindows()
