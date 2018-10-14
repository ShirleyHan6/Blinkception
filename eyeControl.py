# python eyeControl.py --shape-predictor /home/rohan/Downloads/shape_predictor_68_face_landmarks.dat
'''CHANGE THIS PATH TO YOUR LOCATION FOR THE PREDICTOR'''
SHAPE_PREDICTOR_PATH = r'/Users/shirley/Desktop/blinkception/shape_predictor_68_face_landmarks.dat'

# import the necessary packages
from scipy.spatial import distance as dist
from imutils.video import FileVideoStream
from imutils.video import VideoStream
from imutils import face_utils
import numpy as np
import argparse
import imutils
import time
import dlib
import cv2
import sys
import pickle
#from itertools import groupby
#import playground
import morse_code 
import initialSetup
import faceRecognize    
import playground
import sendEmail
from sendEmail import sendEmail
from sendEmail import sendWechatMessage
from playground import *

user=faceRecognize.is_recognized()
f=open(r'records/userThresholds.txt','rb')
try:
	userThresholds=pickle.load(f)
except:
	userThresholds={}
f.close()
USER_EXISTS=False
CARRY_ON_SETUP=True
if bool(user)==True:
	USER_EXISTS=True
if user in list(userThresholds.keys()):
	CARRY_ON_SETUP=False

setup1=initialSetup.setup(SHAPE_PREDICTOR_PATH)

if CARRY_ON_SETUP and USER_EXISTS:	
	BROW_EAR_THRESH=setup1.browSetup();time.sleep(1) 
	MOUTH_THRESH=setup1.mouthSetup();time.sleep(1)
	userThresholds[user]=[BROW_EAR_THRESH,MOUTH_THRESH]
	pickle.dump(userThresholds,open('userThresholds.txt','wb'))

elif USER_EXISTS==False:
	print('Please Register!!!!!')
	sys.exit()
else:
	BROW_EAR_THRESH,MOUTH_THRESH=userThresholds[user]

def interactWebsite(message):
	if message in morse_code.inverseMorseAlphabet.keys():
		message = morse_code.decrypt(message)
		# print(message)
		if message=='@':
			return 'quit'
		interactElement(getCurrentElement(), word = message)

def eye_aspect_ratio(eye):
	A = dist.euclidean(eye[1], eye[5])
	B = dist.euclidean(eye[2], eye[4])
	C = dist.euclidean(eye[0], eye[3])
	ear = (A + B) / (2.0 * C)
	return ear


def distance(x,y):
	a,b=x
	c,d=y
	return round(((a-c)**2 + (b-d)**2)**0.5,3)
def avg(L):
	return sum(L)/len(L)
def std_dev(L): # to find standard deviation of L
	mean=avg(L)
	variance=sum([(x-mean)**2 for x in L])/len(L)
	return round(variance**0.5,3)
#def patternFunc1():
#	playground.fn1()


# construct the argument parse and parse the arguments
#ap = argparse.ArgumentParser()
#ap.add_argument("-p", "--shape-predictor", required=True,
#	help="path to facial landmark predictor")
#ap.add_argument("-v", "--video", type=str, default="",
#	help="path to input video file")
#args = vars(ap.parse_args())
 
# define two constants, one for the eye aspect ratio to indicate
# blink and then a second constant for the number of consecutive
# frames the eye must be below the threshold
EYE_AR_THRESH = 0.3
EYE_AR_CONSEC_FRAMES = 3

# BROW_EAR_THRESH=setup1.browSetup();time.sleep(1) 
# BROW_EAR_THRESH=0.6261359380652183
RAISE_AR_CONSEC_FRAMES = 3
# initialize the frame BLINK_COUNTERs and the total number of blinks
BLINK_COUNTER = 0
BLINK_TOTAL = 0

RAISE_COUNTER=0
RAISE_TOTAL=0
# MOUTH_THRESH=setup1.mouthSetup();time.sleep(1) #0.6553960565298503
# MOUTH_THRESH=0.6553960565298503
MOUTH_COUNTER=0
MOUTH_TOTAL=0
MOUTH_AR_CONSEC_FRAMES=3
# BROW_RAISE_THRESHOLD=1

TIME=0
beg,end=0,0

''' 
'r':  eyebrow raise,
'b':  blink
'/':  mouth open
'''
count = 3
pattern_list=[]
currentWord=[]
#pattern_dict={'brb':patternFunc1}

# initialize dlib's face detector (HOG-based) and then create
# the facial landmark predictor

#print("[INFO] loading facial landmark predictor...")
detector = dlib.get_frontal_face_detector()
predictor = setup1.predictor # dlib.shape_predictor(args["shape_predictor"])

# grab the indexes of the facial landmarks for the left and
# right eye, respectively
(lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
(rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]
(lBrowStart,lBrowEnd)=face_utils.FACIAL_LANDMARKS_IDXS['left_eyebrow']
(rBrowStart,rBrowEnd)=face_utils.FACIAL_LANDMARKS_IDXS['right_eyebrow']
(noseStart,noseEnd)=face_utils.FACIAL_LANDMARKS_IDXS['nose']
(mouthStart,mouthEnd)=face_utils.FACIAL_LANDMARKS_IDXS['mouth']


# start the video stream thread
print("[INFO] starting video stream thread...")
# vs = FileVideoStream(args["video"]).start()
# fileStream = True
vs = VideoStream(src=0).start()
# vs = VideoStream(usePiCamera=True).start()
fileStream = False
time.sleep(1.0)

# loop over frames from the video stream
while True:
	# if this is a file video stream, then we need to check if
	# there any more frames left in the buffer to process
	if fileStream and not vs.more():
		break

	# grab the frame from the threaded video file stream, resize
	# it, and convert it to grayscale
	# channels)
	frame = vs.read()
	frame = imutils.resize(frame, width=450)
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

	# detect faces in the grayscale frame
	rects = detector(gray, 0)

	# loop over the face detections
	for rect in rects:
		# determine the facial landmarks 
		shape = predictor(gray, rect)
		shape = face_utils.shape_to_np(shape)

		# extract the left and right eye coordinates, then use it to compute the eye aspect ratio (EAR)
		leftEye = shape[lStart:lEnd]
		rightEye = shape[rStart:rEnd]
		leftEAR = eye_aspect_ratio(leftEye)
		rightEAR = eye_aspect_ratio(rightEye)

		# values got from face_utils.FACIAL_LANDMARKS_IDXS
		leftBrowMid,leftEyeMid=25,47
		rightBrowMid,rightEyeMid=20,42
		distLeft=distance(shape[leftBrowMid],shape[leftEyeMid])
		distRight=distance(shape[rightBrowMid],shape[rightEyeMid])
		# print(distLeft,distRight)

		nose_mouth_dist=distance(shape[52],shape[34])

		leftBrow=shape[lBrowStart:lBrowEnd]
		rightBrow=shape[rBrowStart:rBrowEnd]

		rightBrowEye=np.array([shape[i] for i in [17,18,20,21,36,39]])
		leftBrowEye=np.array([shape[i] for i in [22,23,25,26,45,42]])

		mouth=np.array([shape[i] for i in [48,50,52,54,56,58]])

		leftBrowEar=eye_aspect_ratio(leftBrowEye)
		rightBrowEar=eye_aspect_ratio(rightBrowEye)

		browEar=(leftBrowEar+rightBrowEar)/2.0
		# nose=shape[noseStart:noseEnd]
		# mouth=shape[mouthStart:mouthEnd]
		mouthEar=eye_aspect_ratio(mouth)


		# average the eye aspect ratio together for both eyes
		ear = (leftEAR + rightEAR) / 2.0

		# compute the convex hull for the left and right eye, then
		# visualize each of the eyes
		leftEyeHull = cv2.convexHull(leftEye)
		rightEyeHull = cv2.convexHull(rightEye)
		
		leftBrowHull=cv2.convexHull(leftBrow)
		rightBrowHull=cv2.convexHull(rightBrow)

		leftBrowEyeHull=cv2.convexHull(leftBrowEye)
		rightBrowEyeHull=cv2.convexHull(rightBrowEye)
		mouthHull=cv2.convexHull(mouth)

		# noseHull=cv2.convexHull(nose)
		# mouthHull=cv2.convexHull(mouth)
		
		cv2.drawContours(frame, [leftEyeHull], -1, (0, 255, 0), 1)
		cv2.drawContours(frame, [rightEyeHull], -1, (0, 255, 0), 1)
		cv2.drawContours(frame, [leftBrowHull], -1, (0, 255, 0), 1)
		cv2.drawContours(frame, [rightBrowHull], -1, (0, 255, 0), 1)

		cv2.drawContours(frame, [leftBrowEyeHull], -1, (14,237,255), 1)
		cv2.drawContours(frame, [rightBrowEyeHull], -1, (14,237,255), 1)

		cv2.drawContours(frame, [mouthHull], -1, (14,237,255), 1)
		# cv2.drawContours(frame, [noseHull], -1, (0, 255, 0), 1)
		# cv2.drawContours(frame, [mouthHull], -1, (0, 255, 0), 1)

		'''for the eye'''
		# check to see if the eye aspect ratio is below the blink
		# threshold, and if so, increment the blink frame BLINK_COUNTER
		if ear < EYE_AR_THRESH:
			BLINK_COUNTER += 1

		# otherwise, the eye aspect ratio is not below the blink
		# threshold
		else:
			# if the eyes were closed for a sufficient number of
			# then increment the total number of blinks
			if BLINK_COUNTER >= EYE_AR_CONSEC_FRAMES:
				BLINK_TOTAL += 1
				pattern_list.append('.')
				beg=end
				end=time.time()
			if (RAISE_TOTAL,BLINK_TOTAL) in [(1,0),(0,1)]:TIME=0 # assumed zero because we dont know the time of the previous blink
			else:TIME=end-beg
			
			# reset the eye frame BLINK_COUNTER
			BLINK_COUNTER = 0
		
		
		'''for the brow'''
		# BROW_EAR_THRESH is 0.7, setting a cap at 0.9 to prevent side-view weirdness
		if 0.9 > browEar > BROW_EAR_THRESH+0.1: # greater than the threshold here
			RAISE_COUNTER += 1
		else:

			if RAISE_COUNTER >= RAISE_AR_CONSEC_FRAMES:
				RAISE_TOTAL += 1
				pattern_list.append('-')
				beg=end
				end=time.time()
			if (RAISE_TOTAL,BLINK_TOTAL) in [(1,0),(0,1)]:TIME=0 # assumed zero because we dont know the time of the previous blink
			else:TIME=end-beg			
			# reset the eye frame BLINK_COUNTER
			RAISE_COUNTER = 0
		
		'''for the mouth'''
		if mouthEar > (MOUTH_THRESH-0.2): # greater than the threshold here
			MOUTH_COUNTER += 1
		else:

			if MOUTH_COUNTER >= MOUTH_AR_CONSEC_FRAMES:
				MOUTH_TOTAL += 1
				pattern_list.append('/')

			MOUTH_COUNTER = 0

		# draw the total number of blinks on the frame along with
		# the computed eye aspect ratio for the frame
		cv2.putText(frame, "Blinks: {}".format(BLINK_TOTAL), (10, 30),
			cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
		cv2.putText(frame, "Raises: {}".format(RAISE_TOTAL), (10, 50),
			cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
		cv2.putText(frame, "mouth_opens: {}".format(MOUTH_TOTAL), (10, 90),
			cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
		#time between blinks
		cv2.putText(frame, "Time: {:.2f}".format(TIME), (10, 70),
			cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

		cv2.putText(frame, " EAR: {:.2f}".format(ear), (300, 30), # ear aspect ratio
			cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
		cv2.putText(frame, " m_EAR: {:.2f}".format(mouthEar), (280, 50), # ear aspect ratio
			cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
 
	# show the frame

	cv2.imshow("Frame", frame)
	key = cv2.waitKey(1) & 0xFF

	if (len(pattern_list)>1 and all([bool(x) for x in pattern_list]) and pattern_list[-1]=='/') or len(pattern_list) > 6:
		RAISE_TOTAL,BLINK_TOTAL=0,0
		message = "".join(pattern_list)[:-1] # to exclude the backslash
		print(message)

		current_element = getCurrentElement()
		moveToElement(current_element)
		if(message[-1]=='.'):
			print("right")
			pre_element = getNextElement(count)
			count+=1
			current_element = pre_element
			# moveToElement(current_element)
			interactElement(current_element)
			print(current_element_global.get_attribute("class"))
			sleep(1)

		elif(message[-1]=='-'):
			pre_element = getPreviousElement(count)
			count-=1
			current_element = pre_element
			# moveToElement(current_element)
			interactElement(current_element)
			print(current_element_global.get_attribute("class"))
			sleep(1)
			
		else:
			x=interactWebsite(message)
			if x=='quit':
				interactElement(getNextElement(getCurrentElement()))



		
		pattern_list=[]
"""
	if (TIME > 10):
		# pass
		sendEmail(user)
		sendWechatMessage(user)
"""
	# cv2.putText(frame, message, (50, 150), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255), 2)
	# if the `q` key was pressed, break from the loop
	if key == ord("q"):
		break

# do a bit of cleanup
cv2.destroyAllWindows()
vs.stop()
