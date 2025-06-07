# Eye Controlled Electric Wheelchair — Proof of Concept  
_A project by Gokul Subedi, Arjun Koirala, and Sushmit Poudel_

## 📜 Overview

Enable wheelchair control using eye gestures captured by a laptop camera. Data collection involved gathering a diverse dataset of image frames representing control commands (forward, left, right, stop). A deep learning–based BiLSTM model and image processing techniques recognize and classify pupil movement in real time. The trained model runs on the laptop (or mobile device) to process incoming frames, map recognized gestures to control signals, and transmit precise commands via Bluetooth to an Arduino UNO–based slave controller. The outcome is a functional system that interprets visual clues, accurately recognizes eye movements, and translates them into control signals—empowering users with improved mobility and independence.

For full technical details, see the [Project Report](report.pdf).

For research Paper, see the [Paper](report.pdf).

## 📝 Introduction

### Background
The global population of individuals reliant on wheelchairs for daily mobility stands at 75 million—about 1 percent of the world’s populace, per WHO. Among them are those with Locked-in syndrome, a rare neurological condition causing near-total paralysis except for eye movement. Locked-in syndrome can result from traumatic brain injury, stroke, or brainstem disorders. Affected individuals remain fully conscious but cannot verbally communicate or move their bodies, relying heavily on assistive technologies for interaction and mobility.

### Problem Definition
Individuals with Locked-in syndrome face profound challenges in communication and mobility. Traditional assistive technologies often fall short, leaving them isolated and dependent on caregivers for basic tasks. This project addresses that gap by providing an eye-controlled wheelchair system—reducing caregiver burden and improving users’ quality of life.

### Objectives
- **Develop** an eye-tracking–based control system for electric wheelchairs.
- **Implement** a deep learning model to classify eye gestures (forward, left, right, stop).
- **Deploy** the trained model for real-time inference on laptop (or mobile).
- **Transmit** control signals wirelessly (Bluetooth HC-05) to Arduino UNO.
- **Demonstrate** a proof-of-concept prototype that empowers users with severe mobility impairments.

## 🎥 Demo

- ![Demo Image](images/output.png)
- [Demo Video](https://drive.google.com/file/d/1QavGxvhbUL2fQrvVY9C85_1CXh6Vu2LD/view?usp=sharing)

All demo assets are in the `images/` folder.

## ✨ Features

- **Real-time Eye Tracking** with custom BiLSTM classifier
- **Grayscale Preprocessing** via OpenCV for robust detection
- **Wireless Control**: Laptop → HC-05 Bluetooth → Arduino UNO
- **Safety Engagement/Disengagement** with audio feedback
- **Modular Design**: Master (laptop) / Slave (Arduino) architecture
- **Assistive Companion Mode** via existing mobile app for caregivers

## 🛠️ Hardware Components

| Component          | Description                                 |
|--------------------|---------------------------------------------|
| Laptop             | Runs classifier & master control logic      |
| Arduino UNO        | Executes movement commands as slave         |
| HC-05 Bluetooth    | Wireless link between laptop and Arduino    |
| L298N Motor Driver | Drives two DIY-style yellow geared DC motors |
| Motors             | DIY yellow geared DC motors                 |
| Chassis            | Robotic-car prototype frame                 |
| LiPo Battery       | Powers Arduino and motors                   |

## 💻 Software & Libraries

- **Python 3.11**
- **TensorFlow** (CUDA 12.6 compatible)
- **OpenCV**, **NumPy**, **matplotlib**
- Custom BiLSTM eye-tracking scripts
- Google Colab for model development

## 🗺️ System Architecture & Flowchart

![System Block Diagram](images/block.png)  
![Transmitter System Flowchart](images/transmitter.png)
![Receiver System Flowchart](images/receiver.png)

```text
Camera → Grayscale Snips → BiLSTM Classifier → Command Mapper → Bluetooth → Arduino UNO → L298N Driver → Motors → Wheelchair Movement
```

## 🔄 Control Mapping & Safety

| Eye Gesture                          | Action                          |
|--------------------------------------|---------------------------------|
| Look Forward                         | Move Forward                    |
| Look Right (after engagement)        | Turn Right                      |
| Look Left (after engagement)         | Turn Left                       |
| Eyes Closed (short)                  | Stop                            |
| Eyes Closed (long, disengage sound)  | Disengage & Stop                |
| Eyes Open + Look Right (long)        | Engage wheelchair (audio cue)   |

**Engagement**: Open eyes + look right for a few seconds → “engaged” sound → controls active.  
**Disengagement**: Close eyes for a few seconds → “disengaged” sound → controls inactive.

## 📐 Component Roles

### Arduino UNO
Acts as slave: receives single-character commands (F, L, R, S) via HC-05.  
Maps:  
- F → both motors forward (same speed)  
- S → both motors stop  
- R → reduce right motor speed for right turn  
- L → reduce left motor speed for left turn  

### L298N Motor Driver
Converts Arduino PWM signals into appropriate voltage/current for motors.  
Ensures safe, bi-directional control of each DC gear motor.

## 📡 Communication & Control Functions

```python
def establish_connection():
    """
    Initialize serial link to Arduino (HC-05).
    Retries until successful, returns serial object.
    """

def speak_in_background(text):
    """
    Non-blocking TTS via threading, provides audio feedback.
    """

def send_to_arduino(value, ser):
    """
    Send command character ('F', 'L', 'R', 'S', etc.) over serial.
    Handles engagement/disengagement logic and special cases.
    """

def close_connection(ser):
    """
    Gracefully close serial port to free resources.
    """
```

## 📈 Model Performance

- **Loss vs. Epoch**  
  ![Loss](images/loss.png)

- **Training & Validation Accuracy**  
  ![Accuracy](images/accuracy.png)

(Graphs available in `images/` folder.)

## 🚧 Limitations & Future Work

- **Prototype Only**: Controlled-environment tests.
- **No Calibration**: Per-user/lighting calibration missing.
- **No Obstacle Avoidance**: Self-awareness not implemented.
- **Laptop-Dependent**: Mobile integration pending.

**Next Steps**:  
- Add obstacle detection & avoidance
- Implement user calibration module
- Develop native mobile app version
- Optimize for latency & power efficiency

## 🎓 Project Status

Proof of Concept with ~13 FPS real-time performance.  
Ready for extended user testing and hardware refinement.

## 👥 Project Contributors

_All contributors collaborated closely on all aspects of the project, from concept to implementation._

- **Gokul Subedi** — Software Engineer & System Designer  
- **Sushmit Paudel** — Hardware Engineer & System Designer  
- **Arjun Koirala** — Data Engineer & System Designer


## 🤝 License & Contribution

©️ All rights reserved by Gokul Subedi, Arjun Koirala, and Sushmit Poudel.  
Licensed under the [MIT License](https://opensource.org/licenses/MIT).


## 🏫 Acknowledgments

- Sagarmatha Engineering College, Dept. of Electronics & Computer Engineering
- Er. Bipin Thapa Magar
- Kaggle community and open-source contributors
