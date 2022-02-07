#Tutorial URL : https://youtu.be/Exic9E5rNok
#Original owner : Tech With Tim
#Done by : Deshan Wickramaarachchi
#start Date : 2021/10/01

import cv2
import time
import datetime


cap = cv2.VideoCapture(0)
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
body_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_fullbody.xml")
detection = False
detection_stopped_time = None
timer_sterted = False
second_to_record_Ater_detection = 5

framesize = (int(cap.get(3)), int(cap.get(4)))
fourcc = cv2.VideoWriter_fourcc(*"mp4v")


while True:
    _, frame = cap.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 9)
    bodies = face_cascade.detectMultiScale(gray, 1.3, 9)

    if len(faces) + len(bodies) > 0:
        if detection:
            timer_sterted = False
        else:
            detection = True
            currunt_time = datetime.datetime.now().strftime("%d-%m-%Y-%H-%M-%S")
            out = cv2.VideoWriter(f"{currunt_time}.mp4", fourcc, 20, framesize)
            print("Stared recordng!")
    elif detection:
        if timer_sterted:
            if time.time() - detection_stopped_time >= second_to_record_Ater_detection:
                detection = False
                timer_sterted = False
                out.release()
                print('Stop Recording ! ')
        else:
            timer_sterted = True
            detection_stopped_time = time.time()

    if detection:
        out.write(frame)

    for(x,y, width, height) in faces:
        cv2.rectangle(frame,(x,y), (x + width, y + height), (255, 0,0), 3)

    # for (x, y, width, height) in bodies:
    #     cv2.rectangle(frame, (x, y), (x + width, y + height), (255, 0, 0), 3)

    cv2.imshow("Camera", frame)

    if cv2.waitKey(1) == ord('q'):
        break

out.release()
cap.release()
cv2.destroyAllWindows()