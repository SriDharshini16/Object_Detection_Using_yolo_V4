# -*- coding: utf-8 -*-
"""YOLO.ipynb
Automatically generated by Colaboratory.
Original file is located at
    https://colab.research.google.com/drive/1WBwpIKNiaUFJrVQv-joCOfv7mr9xW0GZ
"""

!pip install opencv-python==4.4.0.46

import urllib.request

url = 'https://pjreddie.com/media/files/yolov3-tiny.weights'
filename = 'yolov3-tiny.weights'

urllib.request.urlretrieve(url, filename)

url1 = 'https://raw.githubusercontent.com/pjreddie/darknet/master/cfg/yolov3-tiny.cfg'
filename1 = 'yolov3-tiny.cfg'

urllib.request.urlretrieve(url1, filename1)

url2 = 'https://raw.githubusercontent.com/pjreddie/darknet/master/data/coco.names'
filename2 = 'coco.names'

urllib.request.urlretrieve(url2, filename2)

import cv2
import numpy as np

net=cv2.dnn.readNet("./yolov3-tiny.weights","./yolov3-tiny.cfg")

classes=[]
with open("./coco.names") as f:
  classes=f.read().splitlines()

classes = []
with open("coco.names", "r") as f:
    classes = [line.strip() for line in f.readlines()]

conf_threshold = 0.3

# Set the non-maximum suppression threshold
nms_threshold = 0.4

# Load the image
img = cv2.imread("./yolov3.jpg")

img.shape

height, width, channels = img.shape

# Create a blob from the image
blob = cv2.dnn.blobFromImage(img, 1/255, (416, 416), (0, 0, 0), swapRB=True, crop=False)

net.setInput(blob)

# Get the output layer names
output_layers = net.getUnconnectedOutLayersNames()

# Run the forward pass and get the network output
outputs = net.forward(output_layers)

# Initialize the lists of detected boxes, confidences, and class IDs
boxes = []
confidences = []
class_ids = []

# Loop over each output from the network
for output in outputs:
    # Loop over each detection in the output
    for detection in output:
        # Get the class ID and confidence for the detection
        scores = detection[5:]
        class_id = np.argmax(scores)
        confidence = scores[class_id]

        # Filter out weak detections
        if confidence > conf_threshold:
            # Scale the bounding box coordinates to the image size
            center_x = int(detection[0] * width)
            center_y = int(detection[1] * height)
            w = int(detection[2] * width)
            h = int(detection[3] * height)

            # Calculate the top-left corner of the bounding box
            x = int(center_x - w/2)
            y = int(center_y - h/2)

            # Add the bounding box, confidence, and class ID to the lists
            boxes.append([x, y, w, h])
            confidences.append(float(confidence))
            class_ids.append(class_id)

# Apply non-maximum suppression to eliminate overlapping boxes
indices = cv2.dnn.NMSBoxes(boxes, confidences, conf_threshold, nms_threshold)

colors = np.random.uniform(0, 255, size=(len(classes), 3))
for i in indices:
    i = i[0]
    box = boxes[i]
    x, y, w, h = box
    label = classes[class_ids[i]]
    color = colors[class_ids[i]]
    cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)
    cv2.putText(img, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color,thickness=2)

from google.colab.patches import cv2_imshow

cv2_imshow(img)
