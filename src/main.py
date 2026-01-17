import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from config import MODEL_PATH
import cv2
from cv_utils import *

BaseOptions = mp.tasks.BaseOptions
HandLandmarker = mp.tasks.vision.HandLandmarker
HandLandmarkerOptions = mp.tasks.vision.HandLandmarkerOptions
HandLandmarkerResult = mp.tasks.vision.HandLandmarkerResult
VisionRunningMode = mp.tasks.vision.RunningMode

def print_result(result: HandLandmarkerResult, output_image, timestamp_ms: int):
    #print('hand landmarker result: {}'.format(result))
    global landmarks
    landmarks = result.hand_landmarks

options = HandLandmarkerOptions(
    base_options=BaseOptions(model_asset_path=str(MODEL_PATH)),
    running_mode=VisionRunningMode.LIVE_STREAM,
    result_callback=print_result                # runs callback after each detection
)

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Error: Could not open video source.")
    exit()

landmarks = None

with HandLandmarker.create_from_options(options) as landmarker:
    frame_count = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # wrap frame as an Image object for mediapipe
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        # detects landmarks
        landmarker.detect_async(mp_image, timestamp_ms=frame_count)
        frame_count += 1

        if landmarks:                           # draw landmarks and skeleton, show on webcam viewer
            draw_landmarks(frame, landmarks)
            draw_hand_skeleton(frame, landmarks)
        cv2.imshow("Hand Tracker", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):   # breaks loop if user presses 'q'
            break

cap.release()
cv2.destroyAllWindows()

