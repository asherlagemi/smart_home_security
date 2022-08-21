# import necessary packages
import os
import re
import threading

import cv2
import cvlib as cv
from cvlib.object_detection import draw_bbox
from playsound import playsound
from pushbullet import PushBullet


class MyThread(threading.Thread):
    """represents a simple Thread object. contains an ID to allow the thread to be revived"""
    def __init__(self, thread_name, thread_id):
        threading.Thread.__init__(self, target=alarm_sound)
        self.thread_name = thread_name
        self.thread_ID = thread_id
        self.daemon = True

    def start(self):
        super().start()

    def is_alive(self) -> bool:
        return super().is_alive()


def alarm_sound():
    """plays the alarm sound if possible"""
    print('ALERT!!')
    try:
        playsound('./audio/alarmhome.mp3')
    except Exception as e:
        print("NO ALARM SOUND IS SET. make sure a file named audio/alarmhome.mp3 exists")
        print(e)


def run():
    # open webcam
    webcam = cv2.VideoCapture(0)

    if not webcam.isOpened():
        raise Exception("Could not open webcam")

    alarm_id = 1  # index of alarm ID
    alarm = MyThread('alarm', alarm_id)
    # loop through frames
    while webcam.isOpened():

        # read frame from webcam
        status, frame = webcam.read()

        if not status:
            break

        # apply object detection
        bbox, label, conf = cv.detect_common_objects(frame, confidence=0.25, model='yolov3-tiny')
        # if a human is detected in the frame, start the alarm
        if 'person' in label and not alarm.is_alive():
            alarm = MyThread('alarm', ++alarm_id)
            for tok in token_names.keys():  # runs through tokens (the format of token_names is <token:name>)
                try:
                    pb = PushBullet(tok)
                    pb.push_note("ALARM!!!", "someone was seen in your house.")  # send push notification
                except Exception as e:
                    print(e)
                    print("token not valid:: push notification wasn't delivered to- ", token_names[tok])
                    # the value for the key in dict is the name of the token owner
            alarm.start()

        # print(bbox, label, conf)

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


def load_tokens(token_list_filename):
    token_dict = None
    if os.path.isfile(token_list_filename):
        with open(token_list_filename) as token_file:
            # convert "<token>:<name>" format from file to dictionary.
            token_lines = [line.strip() for line in token_file.readlines() if re.match(r'[^#].*:.*', line)]
            token_dict = {elem[0]: elem[1] for elem in [line.split(':') for line in token_lines]}
    if not token_dict:
        raise Exception('Token list file [{0}] is missing or contains no tokens.'.format(token_list_filename))
    return token_dict


if __name__ == '__main__':
    token_names = load_tokens('token_config.txt')
    print("started")
    run()
