import os
import cv2
import face_recognition
import pickle
encodings = []
names = []

image_dir = '..'
for root, directories, files in os.walk(image_dir):
    for file in files:
        path =os.path.join(root, files)
        name = os.path.splitext(file)[0]
        person = face_recognition.load_image_file(path)
        encoding = face_recognition.face_encoding(person)[0]
        encodings.append(encoding)
        names.append(name)

with open('train.pkl', 'wb') as f:
    pickle.dump(names, f)
    pickle.dump(encodings, f)