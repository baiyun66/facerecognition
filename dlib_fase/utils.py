import dlib
import numpy as np
import math
import os
from student import utils
import cv2
from dlib_fase import settings
from crm import models

RIGHT_EYE_START = 37 - 1
RIGHT_EYE_END = 42 - 1
LEFT_EYE_START = 43 - 1
LEFT_EYE_END = 48 - 1


detector = dlib.get_frontal_face_detector()
win = dlib.image_window()
predictor_path = "%s/%s"% (settings.DLIB_SOURCE,'shape_predictor_68_face_landmarks.dat')
predictor = dlib.shape_predictor(predictor_path)


class Getlen:
    def __init__(self,p1,p2):
        self.x=p1.x-p2.x
        self.y=p1.y-p2.y

        self.len= math.sqrt((self.x**2)+(self.y**2))

    def getlen(self):
        return self.len


def eye_aspect_ratio(eye_array):
    l1 = Getlen(eye_array[0], eye_array[3]).getlen()
    l2 = Getlen(eye_array[1], eye_array[5]).getlen()
    l3 = Getlen(eye_array[2], eye_array[4]).getlen()
    ration1 = abs((l2 + l3) / (2 * l1))
    return ration1


def is_person(file):
    eye_tz = []
    vc = cv2.VideoCapture(file)
    c = 0
    flag =0
    if vc.isOpened():
        print("yes")
        rval, frame = vc.read()
    else:
        rval = False
        print("false")

    timeF = 1000000
    try:
        while rval:
            rval, frame = vc.read()
            if c == 0:
                cv2.imwrite("./signdata/face.jpg", frame)
                fase_file = settings.STU_FACE_DATA
                for filename in os.listdir(fase_file):
                    print(filename[0:-4])
                    is_sim = utils.is_sim_people("%s/%s" % (settings.STU_FACE_DATA, str(filename)), "./signdata/face.jpg")
                    if is_sim:
                        user = models.UserProfile.objects.get(email=filename[0:-4])
                        flag = 1
                        print("OK",user)
                        break
                if flag ==0:
                    return 0,None
            if c % timeF == 0:
                if eye_oc(frame):
                    eye_tz.append(eye_oc(frame))
            c = c + 1000000
        cv2.waitKey(1)
        vc.release()
    except:
        pass
    arr_var = np.var(eye_tz)
    print(arr_var)
    if arr_var > 0.001:
        return 1,user
    else:
        return 0,None


def eye_oc(img):
    dets = detector(img)
    for i, d in enumerate(dets):
        shape = predictor(img, d)
        leftEye = [shape.part(i) for i in range(LEFT_EYE_START, LEFT_EYE_END + 1)]
        rightEye = [shape.part(i) for i in range(RIGHT_EYE_START, RIGHT_EYE_END + 1)]
        leftEAR = eye_aspect_ratio(leftEye)
        rightEAR = eye_aspect_ratio(rightEye)
        return (leftEAR+rightEAR)/2
