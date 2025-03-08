import cv2
import mediapipe as mp
import numpy as np
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from comtypes import CLSCTX_ALL


def initialize_audio():
    """Initializes the audio system and retrieves volume range."""
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = interface.QueryInterface(IAudioEndpointVolume)
    vol_range = volume.GetVolumeRange()
    return volume, vol_range[0], vol_range[1]


def calculate_distance(thumb, index, frame_shape):
    """Calculates Euclidean distance between thumb and index fingertips."""
    h, w, _ = frame_shape
    thumb_x, thumb_y = int(thumb.x * w), int(thumb.y * h)
    index_x, index_y = int(index.x * w), int(index.y * h)
    distance = np.hypot(index_x - thumb_x, index_y - thumb_y)
    return distance, (thumb_x, thumb_y), (index_x, index_y)


def map_volume(distance, min_distance=40, max_distance=150):
    """Maps the calculated distance to a volume percentage."""
    return np.interp(distance, [min_distance, max_distance], [0, 100])


def set_volume(volume, volume_percentage):
    """Sets system volume based on the mapped percentage."""
    volume.SetMasterVolumeLevelScalar(volume_percentage / 100.0, None)


def main():
    """Main function to process video frames and control volume based on hand gestures."""
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
    mp_drawing = mp.solutions.drawing_utils
    volume, min_vol, max_vol = initialize_audio()
    
    cap = cv2.VideoCapture(0)
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb_frame)
        
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                
                distance, thumb_pos, index_pos = calculate_distance(
                    hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP],
                    hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP],
                    frame.shape
                )
                
                vol_percent = map_volume(distance)
                set_volume(volume, vol_percent)
                
                cv2.line(frame, index_pos, thumb_pos, (20, 196, 100), 2)
                cv2.putText(frame, f'Current Volume: {int(vol_percent)}%', (50, 50),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
        
        cv2.imshow("Hand Gesture - Volume Control", frame)
        if cv2.waitKey(1) & 0xFF == 27:
            break
    
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
