from DesignTestLight import HueLightSystem
from DesignTestVision import VisionSystem

# Vision imports
import cv2
import numpy as np
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

# creating objects
hueSystem = HueLightSystem()

visionSys = VisionSystem()

# 1. Configure the Pose Landmarker Options
model_path = 'C:\\Users\\green\\Documents\\CodeFolder\\pose_landmarker_full.task' # Ensure this matches your downloaded file name
base_options = python.BaseOptions(model_asset_path=model_path)
options = vision.PoseLandmarkerOptions(
    base_options=base_options,
    running_mode=vision.RunningMode.VIDEO # Optimized for tracking across frames
)

# 2. Open the camera stream
cap = cv2.VideoCapture(0)

with vision.PoseLandmarker.create_from_options(options) as landmarker:
    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            break

        frame = cv2.flip(frame, 1)

        # Convert the image to MediaPipe's Image format (requires RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

        # Get the timestamp in milliseconds (required for VIDEO running mode)
        timestamp_ms = int(cap.get(cv2.CAP_PROP_POS_MSEC))
        if timestamp_ms == 0:
            timestamp_ms = int(cv2.getTickCount() / cv2.getTickFrequency() * 1000)

        # 3. Run detection
        detection_result = landmarker.detect_for_video(mp_image, timestamp_ms)

        # 4. Draw keypoints manually (Since legacy drawing_utils are also removed)
        if detection_result.pose_landmarks:
            h, w, _ = frame.shape
            for landmark_list in detection_result.pose_landmarks:

                # my additions ___________________________________
                visionSys.track_hand_near_face(landmark_list)
                visionSys.track_hand_above_nose(landmark_list)
                if visionSys.check_hand_near_face():
                    hueSystem.change_all_lights_pink()
                if visionSys.check_hand_above_nose():
                    hueSystem.change_all_lights_green()
                # ________________________________________________

                for landmark in landmark_list:
                    # Convert normalized coordinates back to actual pixel locations
                    cx, cy = int(landmark.x * w), int(landmark.y * h)

                    # Only draw if the keypoint is reasonably visible
                    if landmark.presence > 0.5:
                        cv2.circle(frame, (cx, cy), 5, (0, 255, 0), -1)

        # Display output
        cv2.imshow('MediaPipe Tasks Pose', frame)
        if cv2.waitKey(5) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()