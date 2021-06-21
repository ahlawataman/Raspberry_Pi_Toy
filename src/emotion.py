from __future__ import unicode_literals

import cv2
import tensorflow as tf
import numpy as np
from skimage.transform import resize
from luma.core.interface.serial import i2c
from luma.core.render import canvas
from PIL import Image, ImageSequence
from luma.oled.device import sh1106
from pathlib import Path
from luma.core.sprite_system import framerate_regulator
import sys
import os
import time

cv2.destroyAllWindows()
tf.compat.v1.enable_eager_execution()


def crop_center(img, x, y, w, h):    
    return img[y:y+h,x:x+w]

def preprocess_img(raw):
    img = resize(raw,(200,200, 3))
    img = np.expand_dims(img,axis=0)
    if(np.max(img)>1):
        img = img/255.0
    return img

def brain(raw, x, y, w, h, f, i, o):
    ano = ''
    img = crop_center(raw, x, y , w , h)
    img = preprocess_img(img)
    f.set_tensor(i['index'], img.astype(np.float32))
    f.invoke()
    res = f.get_tensor(o['index'])
    classes = np.argmax(res,axis=1)
    if classes == 0:
        ano = 'anger'
    elif classes == 1:
        ano = 'disgust'
    elif classes == 2:
        ano = 'fear'
    elif classes == 3:
        ano = "happy"
    elif classes == 4:
        ano = "neutral"
    elif classes == 5:
        ano = 'sadness'
    else :
        ano = 'surprised'
    return ano

def check(answer):

    temp_dict = dict(sorted(answer.items(),key = lambda x:x[1], reverse = True))
    max_key = max(temp_dict,key = temp_dict.get)
    if(temp_dict[max_key]==0):
        return 'No face Detected'
    return max_key

def checkEmotion():

    print('Loading ..')

    f = tf.lite.Interpreter("models/model_optimized.tflite")
    f.allocate_tensors()
    i = f.get_input_details()[0]
    o = f.get_output_details()[0]

    print('Load Success')


    cascPath = "haarcascade_frontalface_default.xml"

    faceCascade = cv2.CascadeClassifier(cascPath)


    cap = cv2.VideoCapture(0)
    ai = 'anger'
    img = np.zeros((200, 200, 3))
    ct = 0
    iterator = 0

    answer = {
        'sadness':0,
        'anger':0,
        'happy':0,
        'neutral':0,
        'disgust':0,
        'fear':0,
        'surprised':0
    }

    while(True):
        # Capture frame-by-frame
        ret, frame = cap.read()
        ct+=1
        # Our operations on the frame come here
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect faces in the image
        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(150, 150)
            #flags = cv2.CV_HAAR_SCALE_IMAGE
        )
        
        ano = ''    
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.putText(frame, ai, (x, y-5), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255), 2, cv2.LINE_AA)
            answer[ai] += 1
            if ct > 3:
                ai = brain(gray, x, y, w, h, f, i, o)
                ct = 0

        iterator+=1


        # Display the resulting frame
        cv2.imshow('frame',frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        if iterator==75:
            break

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()

    emotion = check(answer)
    print(emotion)

    serial = i2c(port=1, address=0x3C)
    device = sh1106(serial)

    #print face function :-
    if emotion == "No face Detected":
        #No Face Detected
        with canvas(device) as draw:
            draw.rectangle(device.bounding_box, outline="white", fill="black")
            draw.text((18, 23), "NO FACE DETECTED", fill="white")
            draw.text((38, 35), "try again!", fill="white")
            time.sleep(7)
            return
    else:
        regulator = framerate_regulator(fps=10)
        img_path = f'images/{emotion}.gif'
        face = Image.open(img_path)
        device.size = (128, 128)
        size = [min(*device.size)] * 2
        posn = ((device.width - size[0]) // 2, device.height - size[1] + 30)
        t_end = time.time() + 7
        os.system(f"mpg123 audio/{emotion}.mp3")
        while time.time() < t_end:
            for frame in ImageSequence.Iterator(face):
                with regulator:
                    background = Image.new("RGB", device.size, "white")
                    background.paste(frame.resize(size, resample=Image.LANCZOS), posn)
                    device.display(background.convert(device.mode))
            time.sleep(3)