import cv2
import numpy as np
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

# Lights stuff

import time
from python_hue_v2 import Hue, BridgeFinder

#https://pypi.org/project/python-hue-v2/#description

finder = BridgeFinder()
time.sleep(1)  # wait for search
# Get server by mdns
host_name = finder.get_bridge_server_lists()[0]  # Here we use first Hue Bridge
addresses = finder.get_bridge_addresses()
# or hue = Hue('ip address','app-key')
#hue = Hue(addresses[0], 'hue app key')  # create Hue instance

# If you don't have hue-app-key, press the button and call bridge.connect() (this only needs to be run a single time)
hue = Hue(host_name)
app_key = hue.bridge.connect() # you can get app_key and storage on disk

print(app_key)
print(addresses)

lights = hue.lights

print(lights)

# Saffie messing around
bodypartDict = {
    0 : "nose", 1 : "left eye (inner)", 2 : "left eye", 3 : "left eye (outer)", 4 : "right eye (inner)", 5 : "right eye",
    6 : "right eye (outer)", 7 : "left ear", 8 : "right ear", 9 : "mouth (left)", 10 : "mouth (right)", 11 : "left shoulder",
    12 : "right shoulder", 13 : "left elbow", 14 : "right elbow", 15 : "left wrist", 16 : "right wrist", 17 : "left pinky",
    18 : "right pinky", 19 : "left index", 20 : "right index", 21 : "left thumb", 22 : "right thumb", 23 : "left hip",
    24 : "right hip", 25 : "left knee", 26 : "right knee", 27 : "left ankle", 28 : "right ankle", 29 : "left heel",
    30 : "right heel", 31 : "left foot index", 32 : "right foot index"
}

# 1. Configure the Pose Landmarker Options
model_path = 'C:\\Users\\green\\Documents\\CodeFolder\\pose_landmarker_full.task' # Ensure this matches your downloaded file name
base_options = python.BaseOptions(model_asset_path=model_path)
options = vision.PoseLandmarkerOptions(
    base_options=base_options,
    running_mode=vision.RunningMode.VIDEO # Optimized for tracking across frames
)

# 2. Open the camera stream
cap = cv2.VideoCapture(0)

frameCount = 0

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
                count = 0

                #if landmark_list[18].y < landmark_list[0].y:
                #    print("left hand above nose")
                #    for light in lights:
                #        light.color_xy = {'x':0.451, 'y':0.172}

                distanceLeftFromFaceY = abs(landmark_list[19].y - landmark_list[0].y)
                distanceLeftFromFaceX = abs(landmark_list[19].x - landmark_list[19].x)
                distanceRightFromFaceY = abs(landmark_list[20].y - landmark_list[19].y)
                distanceRightFromFaceX = abs(landmark_list[20].x - landmark_list[20].x)

                #print("distance left from face y: " + str(distanceLeftFromFaceY))
                #print("left index: " + str(landmark_list[19].y) + " nose: " + str(landmark_list[0].y))

                if distanceRightFromFaceY < 0.05 and distanceRightFromFaceX < 0.05 or distanceLeftFromFaceY < 0.05 and distanceLeftFromFaceX < 0.05:
                    frameCount += 1
                    print(frameCount)

                #print(landmark_list[18].y)

                for landmark in landmark_list:
                    # Convert normalized coordinates back to actual pixel locations
                    cx, cy = int(landmark.x * w), int(landmark.y * h)
                    #print(bodypartDict.get(count), "x", cx, "y", cy)
                    #print(count)
                    count += 1


                    # Only draw if the keypoint is reasonably visible
                    if landmark.presence > 0.5:
                        cv2.circle(frame, (cx, cy), 5, (0, 255, 0), -1)

        # Display output
        cv2.imshow('MediaPipe Tasks Pose', frame)
        if cv2.waitKey(5) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
