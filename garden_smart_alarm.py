# import necessary packages
import sys
from pushbullet import PushBullet
from playsound import playsound
import cvlib as cv
from cvlib.object_detection import draw_bbox
import threading
import cv2


class mythread(threading.Thread):
    def __init__(self, thread_name, thread_ID):
        threading.Thread.__init__(self, target=alarm_sound)
        self.thread_name = thread_name
        self.thread_ID = thread_ID
        self.daemon = True

    def start(self):
        super().start()

    def is_alive(self) -> bool:
        return super().is_alive()



def alarm_sound():
    playsound('./audio/alarmhome.mp3')
    print('ALERT!!')


def run():
    # open webcam
    webcam = cv2.VideoCapture(0)

    if not webcam.isOpened():
        print("Could not open webcam")
        exit()

    access_token = 'o.CHzTHRGTyTxuQyIJz9IDOTOagjkOebGE'
    pb = PushBullet(access_token)
    alarm_id = 1 # index of alarm ID
    alarm = mythread('alarm', alarm_id)
    # loop through frames
    while webcam.isOpened():

        # read frame from webcam
        status, frame = webcam.read()

        if not status:
            break

        # apply object detection
        bbox, label, conf = cv.detect_common_objects(frame, confidence=0.25, model='yolov3-tiny')
        if 'person' in label and not alarm.is_alive():
            alarm = mythread('alarm', ++alarm_id)
            pb.push_note("ALARM!!!", "someone was seen in your house.")
            alarm.start()

        print(bbox, label, conf)

        # draw bounding box over detected objects
        out = draw_bbox(frame, bbox, label, conf, write_conf=True)

        # display output
        cv2.imshow("Real-time object detection", out)

        # press "Q" to stop
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # release resources
    webcam.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    print("started")
    run()
