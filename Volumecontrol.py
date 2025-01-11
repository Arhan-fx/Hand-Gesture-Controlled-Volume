import cv2
import mediapipe as mp
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume


class HandTracker:
    def __init__(self, detection_confidence=0.7, tracking_confidence=0.7, max_hands=2):
        self.hands = mp.solutions.hands.Hands(
            static_image_mode=False,
            max_num_hands=max_hands,
            min_detection_confidence=detection_confidence,
            min_tracking_confidence=tracking_confidence
        )
        self.mpDraw = mp.solutions.drawing_utils

    def detect_hands(self, img, draw=True):
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(img_rgb)
        if self.results.multi_hand_landmarks and draw:
            for hand_landmarks in self.results.multi_hand_landmarks:
                self.mpDraw.draw_landmarks(img, hand_landmarks, mp.solutions.hands.HAND_CONNECTIONS)
        return img

    def get_landmark_positions(self, img, hand_no=0):
        positions = []
        if self.results.multi_hand_landmarks:
            hand = self.results.multi_hand_landmarks[hand_no]
            for id, landmark in enumerate(hand.landmark):
                h, w, c = img.shape
                cx, cy = int(landmark.x * w), int(landmark.y * h)
                positions.append((id, cx, cy))
        return positions


def main():
    cap = cv2.VideoCapture(0)
    tracker = HandTracker(detection_confidence=0.8, tracking_confidence=0.8)
    
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    min_volume, max_volume = volume.GetVolumeRange()[:2]

    while True:
        success, img = cap.read()
        if not success:
            break

        img = tracker.detect_hands(img)
        landmarks = tracker.get_landmark_positions(img)

        if len(landmarks) >= 8:
            x1, y1 = landmarks[4][1], landmarks[4][2]  # Thumb tip
            x2, y2 = landmarks[8][1], landmarks[8][2]  # Index finger tip

            cv2.circle(img, (x1, y1), 10, (255, 0, 0), cv2.FILLED)
            cv2.circle(img, (x2, y2), 10, (255, 0, 0), cv2.FILLED)
            cv2.line(img, (x1, y1), (x2, y2), (0, 255, 0), 2)

            distance = math.hypot(x2 - x1, y2 - y1)
            vol = min_volume + (max_volume - min_volume) * (distance / 200)
            vol = max(min_volume, min(vol, max_volume))
            volume.SetMasterVolumeLevel(vol, None)

            vol_percent = int((vol - min_volume) / (max_volume - min_volume) * 100)
            cv2.putText(img, f'Volume: {vol_percent}%', (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        cv2.imshow("Hand Tracker Volume Control", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
