import cv2
from telegram import email_alert

config_file = 'ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt'
frozen_model = 'frozen_inference_graph.pb'
model = cv2.dnn_DetectionModel(frozen_model, config_file)

classLabels = []
file_name = 'Labels.txt'
with open(file_name, 'rt') as ftp:
    classLabels = ftp.read().rstrip('\n').split('\n')

cap = cv2.VideoCapture('cam_video1.mov')

counted_cars = 0
time_delay = 39
email_time_delay = 499

while True:
    ret, frame = cap.read()
    height, width, _ = frame.shape
    roi = frame[400:600, 1100:1450]
    roi2 = frame[350:480, 920:1200]
    roi3 = frame[600:1080, 600:1400]

    model.setInputSize(320, 320)
    model.setInputScale(1.0 / 127.5)
    model.setInputMean((127.5, 127.5, 127.5))
    model.setInputSwapRB(True)

    ClassIndex, confidence, bbox = model.detect(roi, confThreshold=0.5)
    font_scale = 3
    font = cv2.FONT_HERSHEY_PLAIN
    for ClassInd, conf, boxes in zip(ClassIndex, confidence, bbox):

        if ClassInd == 1:
            cv2.rectangle(roi, boxes, (255, 0, 0), 4)
            cv2.putText(roi, 'Person', (boxes[0] + 10, boxes[1] + 40),
                        font, font_scale, color=(0, 255, 0), thickness=3)
            email_time_delay += 1
            if email_time_delay % 500 == 0:
                email_alert('Alpaki', 'Ktoś podszedł do ogrodzenia', 'piotrborsuk266@gmail.com')

    ClassIndex, confidence, bbox = model.detect(roi2, confThreshold=0.5)

    for ClassInd, conf, boxes in zip(ClassIndex, confidence, bbox):

        if ClassInd == 1:
            cv2.rectangle(roi2, boxes, (255, 0, 0), 4)
            cv2.putText(roi2, 'Person', (boxes[0] + 10, boxes[1] + 40),
                        font, font_scale, color=(0, 255, 0), thickness=3)
            email_time_delay += 1
            if email_time_delay % 800 == 0:
                email_alert('Alpaki', 'Ktoś podszedł do ogrodzenia', 'piotrborsuk266@gmail.com')

    ClassIndex, confidence, bbox = model.detect(roi3, confThreshold=0.5)

    for ClassInd, conf, boxes in zip(ClassIndex, confidence, bbox):

        if ClassInd == 3:
            cv2.rectangle(roi3, boxes, (255, 0, 0), 4)
            cv2.putText(roi3, 'Car', (boxes[0] + 10, boxes[1] + 40),
                        font, font_scale, color=(0, 255, 0), thickness=3)
            time_delay += 1
            if time_delay % 40 == 0:
                counted_cars += 1

    cv2.putText(frame, f'Counted cars: {counted_cars}', (600, 600),
                cv2.FONT_HERSHEY_PLAIN, 3, color=(255, 0, 0), thickness=3)
    cv2.imshow('Frame', frame)
    cv2.imshow('Roi', roi)
    cv2.imshow('Roi2', roi2)
    cv2.imshow('Roi3', roi3)

    if cv2.waitKey(1) & 0xFF == ord('q'):
            break
cap.release()
cv2.destroyAllWindows()