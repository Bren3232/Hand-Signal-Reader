# pip install --upgrade pip
# From Advanced Computer Vision with Python - Full Course
# https://youtu.be/01sAkU_NvOY
# https://www.computervision.zone/courses/advance-computer-vision-with-python/

# pose sections starts at 48min
# he talks about how to get values out of this at 1h 20

import cv2
import mediapipe as mp          # go to media pipe website to see landmark numbers
import time

class poseDetector():

    def __init__(self, mode=False, complexity=1, smooth=True, enable_seg=False, smooth_seg=True,
                 detectionCon=0.5, trackCon=0.5):

        self.mode = mode            # self in all spots, means the variable that is passed to the class
        self.complexity = complexity
        self.smooth = smooth
        self.enable_seg = enable_seg
        self.smooth_seg = smooth_seg
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpDraw = mp.solutions.drawing_utils
        self.mpPose = mp.solutions.pose
        self.pose = self.mpPose.Pose(self.mode, self.complexity, self.smooth, self.enable_seg, self.smooth_seg,
                                     self.detectionCon, self.trackCon)

    def findPose(self, frame, draw=True):

        frameRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.results = self.pose.process(frameRGB)
        if self.results.pose_landmarks:
            if draw:
                self.mpDraw.draw_landmarks(frame, self.results.pose_landmarks, self.mpPose.POSE_CONNECTIONS)
        return frame

    def findPosition(self, frame, draw=True):
        lmList = []
        if self.results.pose_landmarks:
            for id, lm in enumerate(self.results.pose_landmarks.landmark):
                h, w, c = frame.shape
                # print(id, lm)           # print landmark with id number
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmList.append([id, cx, cy])        # can add more value outputs here
                if draw:
                    cv2.circle(frame, (cx, cy), 5, (255, 0, 0), cv2.FILLED)     # puts circles over the points
        return lmList


# cap.release()
# cv2.destroyAllWindows()

def main():
    cap = cv2.VideoCapture("Yoga.mp4")
    pTime = 0
    detector = poseDetector()
    while True:
        ret, frame = cap.read()
        frame = detector.findPose(frame)
        lmList = detector.findPose(frame)
        # if len(lmList) != 0:
        #     print(lmList[14])        # lmList[14] should print elbow position, printing slowdown fps
        #     cv2.circle(frame, (lmList[14][1], lmList[14][2]), 15, (0, 0,255), cv2.FILLED)
        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime

        cv2.putText(frame, str(int(fps)), (70, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)
        cv2.imshow("Frame", frame)
        cv2.waitKey(1)

    # if cv2.waitKey(1) & 0xFF == ord('q'):
    #     break


if __name__ == "__main__":
    main()

