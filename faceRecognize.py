import face_recognition
import cv2
import pickle
def is_recognized():
    # Get a reference to webcam #0 (the default one)
    video_capture = cv2.VideoCapture(0)

    # user_image = face_recognition.load_image_file("Shirley.jpg")

    # user_face_encoding = face_recognition.face_encodings(biden_image)[0]

    # Create arrays of known face encodings and their names
    f=open(r'records/userNamesRecognized.txt','rb')
    userNamesRecognizedDict=pickle.load(f)
    f.close()
    known_face_encodings =list(userNamesRecognizedDict.values())
    known_face_names =list(userNamesRecognizedDict.keys())

    # Initialize some variables
    face_locations = []
    face_encodings = []
    face_names = []
    process_this_frame = True
    frameCounter=0
    breakOuter=False
    while True:
        # Grab a single frame of video
        ret, frame = video_capture.read()

        # Resize frame of video to 1/4 size for faster face recognition processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = small_frame[:, :, ::-1]

        # Only process every other frame of video to save time
        if process_this_frame:
            # Find all the faces and face encodings in the current frame of video
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

            face_names = []
            for face_encoding in face_encodings:
                # See if the face is a match for the known face(s)
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                name = "Unknown"

                # If a match was found in known_face_encodings, just use the first one.
                if True in matches:
                    first_match_index = matches.index(True)
                    name = known_face_names[first_match_index]
                if name != "Unknown":
                    # print('User {} recognized!'.format(name))
                    return name
                    
                else:
                    if frameCounter>10:
                        print('User not recognized. Please register first. ')
                        return False
                face_names.append(name)

        process_this_frame = not process_this_frame
        frameCounter+=1


    video_capture.release()
    cv2.destroyAllWindows()
#print(is_recognized())