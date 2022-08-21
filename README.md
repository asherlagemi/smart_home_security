# Smart Home Security
Smart home alarm. Using computer vision to distinguish between humans to other moving object, which makes it usefull for outside enviroment. Once a person is seen, the alarm starts and a push notification is sent to the phone via PushBullet

## Libraries:
```
pip install pushbullet.py==0.9.1
pip install opencv-python tensorflow
pip install cvlib
pip install playsound==1.2.2
```
## Token setup
The *token_cofig.txt* file should contain the list of tokens from pushbullet, in following format:

TOKEN:NAME

To get the token log to PushBullet and [follow this guide](https://www.geeksforgeeks.org/python-web-app-to-send-push-notification-to-your-phone "GFG PushBullet Setup")
