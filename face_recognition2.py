import face_recognition
#pip install opencv-python
import cv2  
name_face=face_recognition.load_image_file('path')
name_face_encode = face_recognition.face_encodings(name_face)[0]

encodings = [name_face]
name_faces = ['Donal']
font = cv2.FONT_HERSHEY_SIMPLEX
test_image = face_recognition.load_image_file('path unknow face')
face_positions = face_recognition.face_locations(test_image)
encodingTests = face_recognition.face_encodings(test_image, face_positions)

test_image = cv2.cvtColor(test_image, cv2.COLOR_RGB2BGR)

for (top, right, bottom, left), face_encoding in zip(face_positions,  encodingTests):
    name="unKnown"
    matches = face_recognition.compare_faces(encodings, face_encoding)
    if True in matches:
        first_match_index = matches.index(True)
        name=name_faces[first_match_index]
    cv2.rectangle(test_image, name, (left, top), (right, bottom), (0,0,255), 2)
    cv2.putText(test_image, (left, top - 6), font, .75, (0, 255, 255), 1)
cv2.imshow("myWindow", test_image)
if cv2.waitKey(0) == ord('q'):
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
