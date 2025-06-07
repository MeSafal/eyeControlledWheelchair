# /***************************************************************
# *   Project: Eye Controlled Wheelchair
# *   Developers: 
# *       - Gokul Subedi
# *       - Arjun Koirala
# *       - Sushmit Poudel
# *   Date: 2080-11-23
# *   Description: This code is part of the Eye Controlled Wheelchair project, developed as a minor project of the BEI 2077 batch. 
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


import serial as ser
import sys
import pyttsx3
import threading

port = 'COM5'
prev_vlaue = 'A'
Stop_count = 0
Right_count = 0
Left_count = 0
stopCommand = True
backCommand = False

engine = pyttsx3.init()

def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def establish_connection():
    attempts = 0
    max_attempts = 3
    ser_connection = None

    while attempts < max_attempts:
        try:
            ser_connection = ser.Serial(port, 9600, timeout=1)
            print("Serial connection established.")
            break
        except ser.SerialException:
            attempts += 1
            print(f"Error: Serial connection attempt {attempts}/{max_attempts} failed. Retrying...")
    else:
        print("Error: Maximum attempts reached. Serial connection couldn't be established.")
        sys.exit()

    return ser_connection

def speak_in_background(text):
    threading.Thread(target=speak, args=(text,), daemon=True).start()

def send_to_arduino(value, ser_connection):
    global prev_vlaue, Stop_count, Right_count, Left_count, stopCommand, backCommand
    if value == 'S':
        Stop_count += 1
        if Stop_count == 3:
            Right_count = 0
            Left_count = 0
        if Stop_count > 15:
            stopCommand = True
            speak_in_background("Your Vehicle is now fully stopped")
    elif value == 'R':
        Right_count += 1
        if Right_count == 3:
            Stop_count = 0
            Left_count = 0
        if Right_count > 30:
            Right_count = 0
            if stopCommand:
                backCommand = False
                stopCommand = False
            speak("Vehicle Engaged, Now start moving forward")
    elif value == 'L':
        Left_count += 1
        if Left_count  == 3:
            Right_count  =0
            Stop_count = 0
        if Left_count == 30:
            Left_count = 0
            if stopCommand:
                backCommand = True
                stopCommand = False
            speak("Vehicle Engaged to go back")
            
            
    if not ser_connection:
        establish_connection()
    if prev_vlaue != value:
        prev_vlaue = value
        
    elif  not stopCommand and backCommand:
        if value == 'F':
            value = 'B'
        try:
            encoded_value = str(value).encode() 
            ser_connection.write(encoded_value)
            print("Sent '{}' to Arduino".format(encoded_value.decode())) 
        except Exception as e:
            print(f"Error while sending data to Arduino: {e}")
            
    elif not stopCommand and not backCommand:
        try:
            encoded_value = str(value).encode() 
            ser_connection.write(encoded_value)
            print("Sent '{}' to Arduino".format(encoded_value.decode())) 
        except Exception as e:
            print(f"Error while sending data to Arduino: {e}")
            
    else :
        try:
            encoded_value = str('S').encode() 
            ser_connection.write(encoded_value)
            print("Sent '{}' to Arduino".format(encoded_value.decode())) 
        except Exception as e:
            print(f"Error while sending data to Arduino: {e}")

def close_connection(ser_connection):
    if ser_connection is not None:
        ser_connection.close()
        print("Serial connection closed.")
