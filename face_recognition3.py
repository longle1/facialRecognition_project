import os
import cv2
import face_recognition
import pickle
encodings = []
names = []

with open('train.pkl', 'rb') as f:
    names = pickle.load(f)
    encodings = pickle.load(f)

cam = cv2.VideoCapture(1)
while True:
    _, frame = cam.read()
    frameSize = cv2.resize(frame, (0, 0), fx=.33, fy=.33)
    frame = cv2.cvtColor(frameSize, cv2.COLOR_RGB2BGR)
    face_locations = face_recognition.face_locations(frame, model='cnn')
    allEncodings = face_recognition.face_encodings(frame, face_locations)
    for (top, right, bottom, left), face_encoding in zip(face_locations,  allEncodings):
        name="unKnown"
        matches = face_recognition.compare_faces(encodings, face_encoding)
        if True in matches:
            first_match_index = matches.index(True)
            name=name_faces[first_match_index]
        top = top * 3
        right = right * 3
        bottom = bottom * 3
        left = left * 3
        cv2.rectangle(test_image, name, (left, top), (right, bottom), (0,0,255), 2)
        cv2.putText(test_image, (left, top - 6), font, .75, (0, 255, 255), 1)
    cv2.imshow("myWindow", test_image)
    cv2.moveWindow("myWindow", 0, 0)
    if cv2.waitKey(0) == ord('q'):
        break
cam.release()
cv2.destroyAllWindows()




# font = cv2.FONT_HERSHEY_SIMPLEX
# test_image = face_recognition.load_image_file("path_unknow")
# face_positions = face_recognition.face_locations(test_image)
# encodingTests = face_recognition.face_encodings(test_image, face_positions)
# test_image = cv2.cvtColor(test_image, cv2.COLOR_RGB2BGR)

# for (top, right, bottom, left), face_encoding in zip(face_positions,  encodingTests):
#     name="unKnown"
#     matches = face_recognition.compare_faces(encodings, face_encoding)
#     if True in matches:
#         first_match_index = matches.index(True)
#         name=name_faces[first_match_index]
#     cv2.rectangle(test_image, name, (left, top), (right, bottom), (0,0,255), 2)
#     cv2.putText(test_image, (left, top - 6), font, .75, (0, 255, 255), 1)
# cv2.imshow("myWindow", test_image)
# if cv2.waitKey(0) == ord('q'):
#     cv2.destroyAllWindows()
