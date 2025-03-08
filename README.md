# Hand Gesture Volume Control

A Python project that controls system volume using hand gestures via OpenCV and MediaPipe.

## 📌 Features
✔️ Detects hand gestures in real time  
✔️ Adjusts system volume based on thumb-index finger distance  
✔️ Uses OpenCV and MediaPipe for hand tracking  

## 🛠 Installation
Install required libraries:
```bash
pip install opencv-python mediapipe numpy pycaw


How to Run the script:

python volume_control.py
Then,
1. Move your hand in front of the webcam.
2. Pinch your thumb & index finger to change volume:

What is happening ?
=>When Moving fingers apart the volume increases.
=>When fingers are brought closer to eachother volume decreases.

How to exit the frame ?
=>Press ESC to exit.

How It Works ?
Step 1: Uses MediaPipe Hands to detect hand landmarks.
Step 2: Calculates the Euclidean distance between thumb & index finger.
Step 3: Maps this distance to a volume range (0-100%).
Step 4: Uses Pycaw to update the system volume in real-time.

Troubleshooting :

If Webcam is not working
=>Ensure no other app is using the webcam.
=>Try cv2.VideoCapture(1) if using an external camera.

If Volume is not changing
=>Run the script as Administrator (for system volume access).
=>Check if your microphone/speakers are properly detected.

Contribution:
Feel free to fork this repo, make improvements, and submit a pull request! Contributions are welcome.


Made by Aditi Rawat.
This project is open-source and available under the MIT License.