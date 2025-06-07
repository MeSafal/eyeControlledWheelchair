# /***************************************************************
# *   Project: Eye Controlled Wheelchair
# *   Developers: 
# *       - Gokul Subedi
# *       - Arjun Koirala
# *       - Sushmit Poudel
# *   Date: 2080-11-23
# *   Description: This code is part of the Eye Controlled Wheelchair project, developed as a minor project for the BEI 2077 batch. 
# *
# *   ©️ All rights reserved. This code is the intellectual property of the developers listed above. Unauthorized use, reproduction, 
#       or distribution of this code, in whole or in part, without prior written permission from the developers, is strictly prohibited and 
#       may be subject to legal action.
# *
# *   By accessing or using this code, you agree to abide by the following terms and conditions, which apply only if the developers 
#     permit the use of the code:
# *
# *   1. The code may be used, modified, and distributed for non-commercial purposes, provided proper attribution is given to the 
#         original developers.
# *   2. Any modifications made to the code must be clearly documented, and the original developers shall not be held liable for any 
#         issues arising from such modifications.
# *   3. This code is provided "as is," without warranty of any kind, express or implied, including but not limited to the warranties 
#         of merchantability, fitness for a particular purpose, and non-infringement.
# *   4. The developers or copyright holders shall not be liable for any claim, damages, or other liability, whether in an action of 
#         contract, tort, or otherwise, arising from, out of, or in connection with the code or the use or other dealings in the code.
# *
# *   Licensed under the Apache License, Version 2.0 (the "License");
# *   you may not use this file except in compliance with the License.
# *   You may obtain a copy of the License at
# *
# *       http://www.apache.org/licenses/LICENSE-2.0
# *
# *   Unless required by applicable law or agreed to in writing, software
# *   distributed under the License is distributed on an "AS IS" BASIS,
# *   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# *   See the License for the specific language governing permissions and
# *   limitations under the License.
# ***************************************************************/




import cv2
import torch
import os
import serial as ser
import torchvision.transforms as transforms
from classifier import EyeClassifier 
from sendData import *

print("Import done")

speak_in_background("""Vehicle Being Ready, Here is a general reminder for you. 
        1., 2 second right look, engage vehichle 
        2., 2 second left look, engaged vehicle for back
        3., 2 second eye close, disengage vehicle
        """)

ser_connection = establish_connection()

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print(f'Using device: {device}')

model = EyeClassifier(4).to(device)  # Assuming EyeClassifier takes number of classes as argument
model.load_state_dict(torch.load('minorModel.pth', map_location=device))
model.eval()

class_mapping = {
    0: 'S',
    1: 'F',
    2: 'R',
    3: 'L'
}

def predict_eye_position(frame, model, label):
    # Preprocess the input frame
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    transform = transforms.Compose([
        transforms.ToPILImage(),
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])
    frame_tensor = transform(frame_rgb).unsqueeze(0).to(device)

    with torch.no_grad():
        output = model(frame_tensor)
        probabilities = torch.softmax(output, dim=1)
        confidence, predicted = torch.max(probabilities.data, 1)
        predicted_class = class_mapping[predicted.item()]  

        send_to_arduino(predicted_class, ser_connection)
    return predicted_class

cap = cv2.VideoCapture(0)

label_counter = 0

while True:
    ret, frame = cap.read()

    if ret:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        faceDetected = False

        if len(faces) > 0: 
            faceDetected = True
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

                face_roi = frame[y:y+h, x:x+w]

                gray_face = cv2.cvtColor(face_roi, cv2.COLOR_BGR2GRAY)

                eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
                eyes = eye_cascade.detectMultiScale(gray_face)

                if len(eyes) > 0:
                    for i, (ex, ey, ew, eh) in enumerate(eyes):
                        cv2.rectangle(face_roi, (ex, ey), (ex+ew, ey+eh), (0, 255, 0), 2)

                        eye_roi = face_roi[ey:ey+eh, ex:ex+ew]

                        eye_position = predict_eye_position(eye_roi, model, f"label_{label_counter}")

                        label_counter += 1
        else:
            send_to_arduino('N', ser_connection)

    cv2.imshow('Webcam', cv2.flip(frame, 1))

    if cv2.waitKey(1) & 0xFF == ord('q'):
        close_connection(ser_connection)
        break

cap.release()
cv2.destroyAllWindows()
