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
import keyboard

# Change the port name to COM5
port = 'COM5'

# Establish serial connection
try:
    ser_connection = ser.Serial(port, 9600, timeout=1)
except ser.SerialException:
    print("Error: Serial connection couldn't be established. Check the port.")
    sys.exit()

print("Serial connection established. Press 'L' to turn LED off and 'R' to turn it on.")

try:
    while True:
        # Check for keyboard input
        if keyboard.is_pressed('l'):
            ser_connection.write(b'L')
            print("Sent 'L' to Arduino")
        elif keyboard.is_pressed('r'):
            ser_connection.write(b'R')
            print("Sent 'R' to Arduino")
except KeyboardInterrupt:
    print("\nKeyboard Interrupt. Exiting...")
finally:
    ser_connection.close()
