import face_recognition
#pip install opencv-python
import cv2  
image=face_recognition.load_image_file('./unknown\un1.jpg')
face_locations = face_recognition.face_locations(image)
row1, col1, row2, col2 = face_locations
cv2.rectangle(img=image, (col1, row1), (col2, row2), (0,0,255), 2)

image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
cv2.imshow("myWindow", image)
if cv2.waitKey(0) == ord('q'):
    cv2.destroyAllWindows()