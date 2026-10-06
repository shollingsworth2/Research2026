# Vision imports
import cv2
import numpy as np
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

class VisionSystem:

    FRAME_COUNT_THRESHOLD = 40
    faceCount = 0
    noseCount = 0

    def __init__(self):
        pass


    def track_hand_near_face(self, landmark_list):
        distanceLeftFromFaceY = abs(landmark_list[19].y - landmark_list[0].y)
        distanceLeftFromFaceX = abs(landmark_list[19].x - landmark_list[0].x)
        distanceRightFromFaceY = abs(landmark_list[20].y - landmark_list[0].y)
        distanceRightFromFaceX = abs(landmark_list[20].x - landmark_list[0].x)
        if distanceRightFromFaceY < 0.05 and distanceRightFromFaceX < 0.05 or distanceLeftFromFaceY < 0.05 and distanceLeftFromFaceX < 0.05:
            self.faceCount += 1
            print("near face", self.faceCount)

    def track_hand_above_nose(self, landmark_list):
        if landmark_list[19].y < landmark_list[0].y or landmark_list[20].y < landmark_list[0].y:
            self.noseCount +=1
            print("above nose", self.noseCount)


    def reset_face_count(self):
        self.faceCount = 0

    def reset_nose_count(self):
        self.noseCount = 0

    def check_hand_near_face(self):
        if self.faceCount > self.FRAME_COUNT_THRESHOLD:
            self.reset_face_count()
            return True
        return False

    def check_hand_above_nose(self):
        if self.noseCount > self.FRAME_COUNT_THRESHOLD:
            self.reset_nose_count()
            return True
        return False