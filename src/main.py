import cv2 as cv
import numpy as np
from collections import defaultdict
import argparse, math


def tst():
    cap = cv.VideoCapture("sugar.mp4")

    if cap.isOpened():
        print("opened")
    else:
        print("Failure")

    width = int(cap.get(cv.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv.CAP_PROP_FRAME_HEIGHT))

    fourcc = cv.VideoWriter_fourcc(*'mp4v')
    output = cv.VideoWriter("output.mp4", fourcc, 24, (width, height), isColor=True)
    history=defaultdict(tuple)
    frame_count=0
    while True:
        ret, frame = cap.read()
        if not ret: break
        frame_count+=1
        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        _, binary = cv.threshold(gray, 127, 255, cv.THRESH_BINARY)
        (all_contours, hierarchy) = cv.findContours(binary, cv.RETR_EXTERNAL,cv.CHAIN_APPROX_SIMPLE)
        if len(all_contours)>0:
            threshold = 100
            contours = [x for x in all_contours if cv.contourArea(x) > threshold]
            srt = sorted(contours, key = cv.contourArea)
            lx,ly,lw,lh = cv.boundingRect(srt[0])
            blobs = 0
            id = 0
            prev = (width // 2, height // 2)   #middle of frame
            #prev = (lx, ly)                   #lines originate from largest blob
            for contour in contours:
                print(contour)
                area = cv.contourArea(contour)
                if area > 1000:
                    cv.drawContours(frame, [contour], 0, (255, 255, 255), 1)    #-1 to fill
                if area < 1500:
                    blobs+=1
                    x,y,w,h = cv.boundingRect(contour)
                    cv.rectangle(frame,(x,y),(x+w,y+h),(255,255,255),1)    #-1 for fill
                    font_size = 1
                    #cv.putText(frame, str(blobs), (x, y+20), cv.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), font_size)
                    distance = math.dist((x, y), prev)
                    print(f"distance: {distance}")
                    #draw_trajectory(frame, history, id)
                    #if (distance  > width / 4 or distance  > height / 4 ):  
                    #    cv.line(frame, prev, (x, y), (255, 255, 255), 1)
                    #draw_trajectory(frame, history, id)
                    #prev = (x, y)
                    if not history[id] or find_closest(history, x, y) == -1:
                        id +=1 
                    else:
                        id = find_closest(history, x, y)
                    print(f'id:{id}')
                    cv.putText(frame, str(id), (x, y+20), cv.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), font_size)
                    
                    history.setdefault(id, (int, []))[0] = id
                    history.setdefault(id, (int, []))[1].append((x, y))
                    
            output.write(frame)
    cv.destroyAllWindows() 
        
    cap.release()
    output.release()

def draw_trajectory(frame, history, id):
    points = history[id]
    if len(points < 2): return
    for i in range(0, len(points)-1):
        cv.line(frame, points[i], points[i+1], (255, 255, 255), 1)

def draw_lines_from_center(frame, contours, width, height): #put in width and height of frame
    centr = (width // 2, height // 2)
    for contour in contours:
        x,y,w,h = cv.boundingRect(contour)
        cv.line(frame, centr, (x, y), (255,255,255), 1)



def find_closest(history, x, y):    
    closest = None
    ret = -1
    if len(history) == 0:
        return -1
    for id in history:
        points = history[id]
        if len(points) == 0: continue
        point = points[-1] #get last point of contour
        dist = math.dist((x, y), point)
        if not closest: 
            closest = dist
            continue        
        if dist < closest: 
            closest = dist
            ret = id
    return ret


if __name__=="__main__":
   parser = argparse.ArgumentParser()
   tst()