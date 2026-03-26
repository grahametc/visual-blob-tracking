import cv2 as cv
import numpy as np


def tst():
    cap = cv.VideoCapture("astro.mp4")

    if cap.isOpened():
        print("cont")
    else:
        print("Failure")

    width = int(cap.get(cv.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv.CAP_PROP_FRAME_HEIGHT))

    fourcc = cv.VideoWriter_fourcc(*'mp4v')
    output = cv.VideoWriter("output.mp4", fourcc, 24, (width, height), isColor=True)
    while True:
        ret, frame = cap.read()
    
        if not ret: break
        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        _, binary = cv.threshold(gray, 127, 255, cv.THRESH_BINARY)
        (contours, hierarchy) = cv.findContours(binary, cv.RETR_EXTERNAL,cv.CHAIN_APPROX_SIMPLE)
        if len(contours)>0:
            blobs = 0
            for contour in contours:
                print(contour)
                area = cv.contourArea(contour)
                if area>100:
                    blobs+=1
                    x,y,w,h = cv.boundingRect(contour)
                    cv.rectangle(frame,(x,y),(x+w,y+h),(255,255,255),1)
                    cv.putText(frame, str(blobs), (x, y+20), cv.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 1)
            output.write(frame)
       
    cv.destroyAllWindows() 
        
    cap.release()
    output.release()

if __name__=="__main__":
   tst()