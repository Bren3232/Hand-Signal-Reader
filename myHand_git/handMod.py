# pip install --upgrade pip
# From Advanced Computer Vision with Python - Full Course
# https://youtu.be/01sAkU_NvOY
# https://www.computervision.zone/courses/advance-computer-vision-with-python/

import cv2
import mediapipe as mp
import time

class handDetector():               # didn't work until I added complexity, as in "hands.py"
    def __init__(self, mode=False, maxHands=2, complexity=1, detectionCon=0.5, trackCon=0.5):
        self.mode = mode        # if mode set True it will always look for new pose, if False with track based on Con
        self.maxHands = maxHands            # max number of hands to find
        self.complexity = complexity
        self.detectionCon = detectionCon    # Level of Con to start tracking
        self.trackCon = trackCon            # Level of Confidence to keep tracking

        self.mpHands = mp.solutions.hands       # ctrl + click on hands to change confidence values  "hands.py"
        self.hands = self.mpHands.Hands(self.mode, self.maxHands, self.complexity, self.detectionCon, self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils


    def findHands(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        # print(results.multi_hand_landmarks)

        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)
        return img

    def findPosition(self, img, handNo=0, draw=True):

        lmList = []
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]

            for id, lm in enumerate(myHand.landmark):
                # print(id, lm)                                       # prints x, y, z of mark
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                # print(id, cx, cy)
                lmList.append([id, cx, cy])
                if draw:
                    cv2.circle(img, (cx, cy), 5, (255, 0, 255), cv2.FILLED)  # draws circle on id'd landmark

        return lmList

def main():
    pTime = 0
    cTime = 0
    cap = cv2.VideoCapture(0)
    detector = handDetector()

    while True:
        red, img = cap.read()
        img = detector.findHands(img)
        lmList = detector.findPosition(img)
        if len(lmList) != 0:
            print(lmList[4])


        cTime = time.time()
        fps = 1 / (cTime-pTime)
        pTime = cTime

        cv2.putText(img, str(int(fps)),(18,78), cv2.FONT_HERSHEY_PLAIN, 3, (255, 8, 255), 3)

        cv2.imshow("Image", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


if __name__ == "__main__":
    main()







