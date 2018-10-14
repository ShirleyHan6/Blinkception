import cv2
import os
import pickle
import face_recognition
# get the user name from the user input 
def register():
    try:
        email_wechat_dict = pickle.load(open("records/email.txt", "rb"))
    except EOFError:
        email_wechat_dict = {}

    try:
        userNamesRecognized = pickle.load(open("records/userNamesRecognized.txt", "rb"))
    except EOFError:
        userNamesRecognized = {}

    userName = input("Enter a user name: ")
    print(email_wechat_dict.keys())
    if userName not in list(email_wechat_dict.keys()):
        email_wechat_dict[userName]=['','','','']
        email_wechat_dict[userName][0] = input("Enter the gmail account of the user: ")
        email_wechat_dict[userName][1] = input("Enter the password of the user: ")
        email_wechat_dict[userName][2] = input("Enter the emergency contact email: ")
        email_wechat_dict[userName][3] = input("Enter the emergency contact wechat friend name: ")

        cam = cv2.VideoCapture(0)

        cv2.namedWindow("test")

        img_counter = 0

        while True:
            ret, frame = cam.read()
            cv2.imshow("test", frame)
            if not ret:
                break
            k = cv2.waitKey(1)

            if k%256 == 27:
                # ESC pressed
                print("Escape hit, closing...")
                break
            elif k%256 == 32:
                # SPACE pressed
                img_name = userName + ".jpg"
                cv2.imwrite(img_name, frame)
                print("{} written!".format(img_name))
                img_counter += 1
            elif k%256 == 127:
                # delete pressed
                try: 
                    os.remove(userName + ".jpg")
                except: 
                    pass
            if k == ord('q'):
                break

        cam.release()

        cv2.destroyAllWindows()
        user_image = face_recognition.load_image_file(userName + ".jpg")
        user_face_encoding = face_recognition.face_encodings(user_image)[0]

        userNamesRecognized[userName] = user_face_encoding
        print(email_wechat_dict.keys())
        pickle.dump(email_wechat_dict, open("records/email.txt", "wb"))
        pickle.dump(userNamesRecognized, open("records/userNamesRecognized.txt", "wb"))
        print('Registration Successful!')
        return True
    else:
        return False # if user already exists