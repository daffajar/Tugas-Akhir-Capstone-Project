from ultralytics import YOLO
import cv2
import math
import os
import json
import datetime
from flask import redirect,url_for,session

global start,web_count
start = None
web_count = [0,0,0,0,0,0,0,0,0]

def update_webcam_db(new_data):
    with open("webcam_db.json",'r+') as file:
        
        file_data = json.load(file)
       
        file_data["detections"][-1] = new_data
        
        file.seek(0)    
   
        json.dump(file_data, file, indent = 4)

        file.close()

def update_db(new_data):
    with open("db.json",'r+') as file:
        
        file_data = json.load(file)
       
        file_data["detections"].append(new_data)
        
        file.seek(0)
   
        json.dump(file_data, file, indent = 4)

        file.close()

def video_detection(path_x):
    model = YOLO('bestrasio1.pt')
    
    # Open the video file
    
    cap = cv2.VideoCapture(path_x)
    unique_id=set()
    classnames = ['Bird', 'Cats', 'Cow', 'Deer', 'Dog', 'Elephant', 'Giraffe','Person', 'Pig', 'Sheep']
    count = [0,0,0,0,0,0,0,0,0,0]
    while cap.isOpened():
        # Read a frame from the video
        success, frame = cap.read()
        
        
        if success:
            # Run YOLOv8 inference on the frame
            results = model.track(frame,conf=0.25,iou=0.5,classes=[2,3,9],tracker="botsort.yaml",persist=True,device=0) 
            img = results[0].plot()
            height, width, _ = img.shape
            # print(results)
            if  results[0].boxes.id !=  None:
                boxes = results[0].boxes.xyxy.cpu().numpy().astype(int)
                classes = results[0].boxes.cls.cpu().numpy().astype(int)
             

                ids = results[0].boxes.id.cpu().numpy().astype(int)
                for box, id,cls in zip(boxes, ids,classes):
                    # Check if the id is unique
                    int_id =int(id)
                    if  int_id  not  in  unique_id:
                        count[cls] = count[cls] + 1
                        unique_id.add(int_id)               
                    if cv2.waitKey(1) & 0xFF == ord("q"):
                        break
                
                cv2.line(img, (width - 500,25), (width,25), [85,45,255], 40)
                cv2.line(img, (width - 500,60), (width,60), [85,45,255], 40)
                cv2.line(img, (width - 500,95), (width,95), [85,45,255], 40)
                cv2.line(img, (width - 500,130), (width,130), [85,45,255], 40)
                cv2.putText(img, f'Number of Cow: {count[2]}', (width - 500, 35), 0, 1, [225, 255, 255], thickness=2, lineType=cv2.LINE_AA)
                cv2.putText(img, f'Number of Deer: {count[3]}', (width - 500, 70), 0, 1, [225, 255, 255], thickness=2, lineType=cv2.LINE_AA)
                cv2.putText(img, f'Number of Sheep: {count[9]}', (width - 500, 105), 0, 1, [225, 255, 255], thickness=2, lineType=cv2.LINE_AA)
                cv2.putText(img, f'Total Animals: {(count[2] + count[3] + count[9])}', (width - 500, 140), 0, 1, [225, 255, 255], thickness=2, lineType=cv2.LINE_AA)
                print(len(unique_id))
            yield img
            cv2.destroyAllWindows()

            
                        # Break the loop if 'q' is pressed
            
        else:
            # Break the loop if the end of the video is reached
            break
        

    # Release the video capture object and close the display window
    print("work2")
    cap.release()
    new_data = {
        "filename" : path_x,
        "timestamp" : datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),
        "sheep_count" : count[9],
        "cow_count" : count[2],
        "deer_count" : count[3],
        "total_count" : count[2] + count[3] + count[9]
    }
    
    if new_data['filename'] != None:
        update_db(new_data=new_data)

    
def web_detection(path_x):
    model = YOLO('100.pt')
    
    # Open the video file
    
    cap = cv2.VideoCapture(path_x)
    unique_id=set()
    classnames = ['Bird', 'Cat', 'Cow', 'Deer', 'Dog', 'Elephant', 'Giraffle','Person', 'Pig', 'Sheep']
    start = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
    with open("webcam_db.json",'r+') as file:
        
        file_data = json.load(file)
       
        file_data["detections"].append({
            "start" : start,
            "end" : None,
            "sheep_count" : 0,
            "cow_count" : 0,
            "deer_count" : 0,
            "total_count" : 0
        })
        
        file.seek(0)
   
        json.dump(file_data, file, indent = 4)

        file.close()

    web_count = [0,0,0,0,0,0,0,0,0,0]
    while cap.isOpened():
        # Read a frame from the video
        success, frame = cap.read()
        
        
        if success:
            # Run YOLOv8 inference on the frame
            results = model.track(frame,conf=0.25,iou=0.5,classes=[2,3,9],tracker="botsort.yaml",persist=True,device=0) 
            img = results[0].plot()
            height, width, _ = img.shape
            # print(results)
            if  results[0].boxes.id !=  None:
                boxes = results[0].boxes.xyxy.cpu().numpy().astype(int)
                classes = results[0].boxes.cls.cpu().numpy().astype(int)
             
                ids = results[0].boxes.id.cpu().numpy().astype(int)
                for box, id,cls in zip(boxes, ids,classes):
                    # Check if the id is unique
                    int_id =int(id)
                    if  int_id  not  in  unique_id:
                        web_count[cls] = web_count[cls] + 1
                        new_data = {
                            "start" : start,
                            "end" : datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),
                            "sheep_count" : web_count[9],
                            "cow_count" : web_count[2],
                            "deer_count" : web_count[3],
                            "total_count" : web_count[2] + web_count[3] + web_count[9]
                        }

                        update_webcam_db(new_data)
                        unique_id.add(int_id)               
                    if cv2.waitKey(1) & 0xFF == ord("q"):
                        break
                cv2.line(img, (width - 230,25), (width,25), [85,45,255], 40)
                cv2.line(img, (width - 230,60), (width,60), [85,45,255], 40)
                cv2.line(img, (width - 230,95), (width,95), [85,45,255], 40)
                cv2.line(img, (width - 230,130), (width,130), [85,45,255], 40)
                cv2.putText(img, f'Total Animal: {web_count[2] + web_count[3] + web_count[9]}', (width - 230, 140), 0, 0.60, [225, 255, 255], thickness=2, lineType=cv2.LINE_AA)
                cv2.putText(img, f'Number of Cow: {web_count[2]}', (width - 230, 35), 0, 0.60, [225, 255, 255], thickness=2, lineType=cv2.LINE_AA)
                cv2.putText(img, f'Number of Deer: {web_count[3]}', (width - 230, 70), 0, 0.60, [225, 255, 255], thickness=2, lineType=cv2.LINE_AA)
                cv2.putText(img, f'Number of Sheep: {web_count[9]}', (width - 230, 105), 0, 0.60, [225, 255, 255], thickness=2, lineType=cv2.LINE_AA)
                print(len(unique_id))
            yield img
            cv2.destroyAllWindows()

            
                        # Break the loop if 'q' is pressed
            
        else:
            # Break the loop if the end of the video is reached
            break
        

    # Release the video capture object and close the display window
    



