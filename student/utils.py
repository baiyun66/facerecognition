import dlib
from imageio import imread
import numpy as np
from dlib_fase import settings
detector = dlib.get_frontal_face_detector()
predictor_path = "%s/%s"% (settings.DLIB_SOURCE,'shape_predictor_68_face_landmarks.dat')
predictor = dlib.shape_predictor(predictor_path)
face_rec_model_path = "%s/%s"% (settings.DLIB_SOURCE,'dlib_face_recognition_resnet_model_v1.dat')
facerec = dlib.face_recognition_model_v1(face_rec_model_path)


def is_face(path):
	try:
		img = imread(path)
		dets = detector(img)
		print('检测到了 %d 个人脸' % len(dets))
		if len(dets)==1:
			return True
		else:
			return False
	except:
		return False


def get_feature(path):
	img = imread(path)
	dets = detector(img)
	print('检测到了 %d 个人脸' % len(dets))
	shape = predictor(img, dets[0])
	face_vector = facerec.compute_face_descriptor(img, shape)
	return face_vector


def distance(a, b):
	a, b = np.array(a), np.array(b)
	sub = np.sum((a-b)**2)
	add = (np.sum(a**2)+np.sum(b**2))/2.
	return sub/add


def classifier(a, b, t=0.12):
	if distance(a, b) <= t:
		ret = True
	else:
		ret = False
	return ret


def is_sim_people(img1, img2):
	path_lists = [img1, img2]
	try:
		feature_lists = [get_feature(path) for path in path_lists]
	except:
		return False
	if len(feature_lists) != 2:
		return False
	return classifier(feature_lists[0], feature_lists[1])




