# python initialSetup.py --shape-predictor /home/rohan/Downloads/shape_predictor_68_face_landmarks.dat



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

## construct the argument parse and parse the arguments
#ap = argparse.ArgumentParser()
#ap.add_argument("-p", "--shape-predictor", required=True,
#    help="path to facial landmark predictor")
#ap.add_argument("-v", "--video", type=str, default="",
#    help="path to input video file")
#args = vars(ap.parse_args())
 
#EYE_AR_THRESH = 0.3

BROW_EAR_THRESH=None 
print("[INFO] loading facial landmark predictor...")
detector = dlib.get_frontal_face_detector()


(lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
(rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]
(lBrowStart,lBrowEnd)=face_utils.FACIAL_LANDMARKS_IDXS['left_eyebrow']
(rBrowStart,rBrowEnd)=face_utils.FACIAL_LANDMARKS_IDXS['right_eyebrow']
(mouthStart,mouthEnd)=face_utils.FACIAL_LANDMARKS_IDXS['mouth']


class setup:
    def __init__(self,shape_predictor_path):
        self.shape_predictor_path = shape_predictor_path
        self.predictor = dlib.shape_predictor(self.shape_predictor_path)
    def browSetup(self):
        print("[INFO] starting video stream thread...")
        vs = VideoStream(src=0).start()
        # vs = VideoStream(usePiCamera=True).start()
        fileStream = False
        time.sleep(1.0)
        '''returns BROW_EAR_THRESH'''
        browThreshs=[]
        BROW_EAR_THRESH=None
        print('\n\n\tMOVE BACK AND FORTH')
        while bool(BROW_EAR_THRESH)==False:
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
                shape = self.predictor(gray, rect)
                shape = face_utils.shape_to_np(shape)
    
    
    
                # values got from face_utils.FACIAL_LANDMARKS_IDXS
                # print(distLeft,distRight)
                rightBrowEye=np.array([shape[i] for i in [17,18,20,21,36,39]])
                leftBrowEye=np.array([shape[i] for i in [22,23,25,26,45,42]])
    
                leftBrowEar=eye_aspect_ratio(leftBrowEye)
                rightBrowEar=eye_aspect_ratio(rightBrowEye)
    
                browEar=(leftBrowEar+rightBrowEar)/2.0
                browThreshs.append(browEar)
    
                leftBrowEyeHull=cv2.convexHull(leftBrowEye)
                rightBrowEyeHull=cv2.convexHull(rightBrowEye)
                
                # cv2.drawContours(frame, [leftEyeHull], -1, (0, 255, 0), 1)
                # cv2.drawContours(frame, [rightEyeHull], -1, (0, 255, 0), 1)
                # cv2.drawContours(frame, [leftBrowHull], -1, (0, 255, 0), 1)
                # cv2.drawContours(frame, [rightBrowHull], -1, (0, 255, 0), 1)
                cv2.drawContours(frame, [leftBrowEyeHull], -1, (14,237,255), 1)
                cv2.drawContours(frame, [rightBrowEyeHull], -1, (14,237,255), 1)
                # cv2.drawContours(frame, [mouthHull], -1, (14,237,255), 1)
    
    
            cv2.imshow("Frame", frame)
            key = cv2.waitKey(1) & 0xFF
    
            if len(browThreshs)==300:
                BROW_EAR_THRESH=avg(browThreshs)
                print('brow raise setup complete!!')
                cv2.destroyAllWindows()
                vs.stop()
                return BROW_EAR_THRESH
    
            # if pattern_list and pattern_list[-1]=='/':
            #     message = "".join(pattern_list)[:-1] # to exclude the backslash
            #     print(message)
            #     if message in morse_code.inverseMorseAlphabet.keys():
            #         message = morse_code.decrypt(message)
            #         print(message)
            #     pattern_list=[] # clear pattern memory if mouth is opened and morse decrypted
            
            # cv2.putText(frame, message, (50, 150), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255), 2)
            # if the `q` key was pressed, break from the loop
            if key == ord("q"):
                break
    
    
    def mouthSetup(self):
        '''returns MOUTH_THRESH'''
        print("[INFO] starting video stream thread...")
        vs = VideoStream(src=0).start()
        # vs = VideoStream(usePiCamera=True).start()
        time.sleep(1.0)
        MOUTH_THRESH=None        
        print('\nMOUTH OPEN SETUP')
        print('OPEN YOUR MOUTH IN ',end ='')
        print('3..',end='');sys.stdout.flush();time.sleep(1)
        print('2..',end='');sys.stdout.flush();time.sleep(1)
        print('1..');sys.stdout.flush();time.sleep(1)
    
        mouthThreshs=[]
        print('\n\nMOVE BACK AND FORTH WITH YOUR MOUTH OPEN')
        while bool(MOUTH_THRESH)==False:
            # if this is a file video stream, then we need to check if
            # there any more frames left in the buffer to process
#            if not vs.more():
#                break
    
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
                shape = self.predictor(gray, rect)
                shape = face_utils.shape_to_np(shape)
                mouth=np.array([shape[i] for i in [48,50,52,54,56,58]])
                mouthEar=eye_aspect_ratio(mouth)
                mouthThreshs.append(mouthEar)
                mouthHull=cv2.convexHull(mouth)
                cv2.drawContours(frame, [mouthHull], -1, (14,237,255), 1)
    
    
            cv2.imshow("Frame", frame)
            key = cv2.waitKey(1) & 0xFF
    
            if len(mouthThreshs)==200:
                MOUTH_THRESH=avg(mouthThreshs)
                print('mouth raise setup complete!!')
                cv2.destroyAllWindows()
                vs.stop()
                return MOUTH_THRESH
            # if the `q` key was pressed, break from the loop
            if key == ord("q"):
                break

# setup1=setup(r'/home/rohan/Downloads/shape_predictor_68_face_landmarks.dat')
# print(setup1.browSetup())
# time.sleep(1)
# print(setup1.mouthSetup())