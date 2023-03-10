
# Based on HandTrack2.py, and needs handMod.py

# ----- Do something if rabbit hand symbol is detected ----
# vv started Nov 23 2021, going to add auto set up
# auto setup working good by end of Nov 23
# Nov 25 2021. Started this file to do the hand signal setup
# Nov 25. Is working good, now to do more testing a tweeting, will it run too slow on pi?
# Nov 27. Going to try integrate with pose detection, and target around the pose to get hand signal, with
    # measurment from nose to wrist, and hight from  nose to wrist
# Nov 30, started this file, copy of myHand4.py going to get aoi based off of pose detection
    # is cropping in good but still not detecting hands at distance, maybe to res drop, or the frame size shaking
# xx could make it so that it sets the aoi when the nose moves a distance based on det_ears
# xx move aoi down some? do multiple aoi's? or set aoi at same area as when set up. First try big aoi
# xx *** Dec 1, Now working to the back of my room with lights on, took pose draw off frame, made a big improvement,
    # xx using a small aoi Next try setting aoi to hand with smallest y value

# vv Problem: only works about 2 meters away, try higher resolution (but will take more comput) or have 2 cameras
 # vv try zooming - higher res with cropping works, might not need higher res.
 #vv **the best way would be to use pose detector, or movement detect, to target cropping regoin to body or hand area.
 #vv could use pose to detect left for right hand, could combine hand sig with a pose sig
 #vv Nov 28, getting coords from holistic is complicated so going to do 1 sec motion, or pose detect,
 # then crop to area, and do hand detect for as long as hand is detected.

import cv2
import time
import math
import numpy as np
import sys
import handMod as hm     # may need this as holistic needs to detect face before it will detect hands
import poseMod as pm


def setup():            # trigger this by button
    f = open("myHand1SaveVal.txt", "r+")
    f.truncate(0)
    f.close()

    # cap = cv2.VideoCapture(0)
    print("Setup initiated, place camera in desired location. Have normal lights turned on")
    time.sleep(2)
    print("Reading light value in...")
    time.sleep(1)
    print("3")
    time.sleep(1)
    print("2")
    time.sleep(1)
    print("1")
    time.sleep(1)
    ret, img1 = cap.read()
    ret, img2 = cap.read()
    ret, img3 = cap.read()
    # cv2.imshow("setup cap", img2)

    # light_v1 = np.sum(img1) // 10000
    light_v2 = np.sum(img2) // 10000
    light_v3 = np.sum(img3) // 10000

    # light_v = (light_v1 + light_v2 + light_v3) // 3
    light_v = (light_v2 + light_v3) // 2

    print("Light value read. Now turn lights off. Reading low light value in 7 seconds")
    time.sleep(7)
    # capb = cv2.VideoCapture(0)
    ret, img1b = cap.read()
    ret, img2b = cap.read()
    ret, img3b = cap.read()
    # light_v1b = np.sum(img1b) // 10000
    light_v2b = np.sum(img2b) // 10000
    light_v3b = np.sum(img3b) // 10000

    # light_vb = (light_v1b + light_v2b + light_v3b) // 3
    light_vb = (light_v2b + light_v3b) // 2

    print("Low light value read.")

    light_thr = (light_v + light_vb) // 2

    f = open("myHand1SaveVal.txt", "a")
    # f.write("\n")
    # f.write("\n")
    f.write(str(light_v))
    f.write("\n")
    f.write(str(light_thr))
    f.close()

    print("light val ", light_v)
    print("light thr ", light_thr)
    print("Light value, and threshold set")
    # cap.release()
    # cv2.destroyAllWindows()
    return None   # not necessary

# -----------------------------------------------------------

def handsig_setup():
    f = open("myHand1SaveVal2.txt", "r+")
    f.truncate(0)
    f.close()
    print("Hand signal setup initiated, make your custom hand signal in front of camera and hold")
    detector = hm.handDetector(False, 1)
    e = time.monotonic() + 8
    while True:
        ret, img = cap.read()
        img = detector.findHands(img)  # add , draw=False to these two in order to not draw
        lmList = detector.findPosition(img, draw=False)  # leave false?
        cv2.imshow("handsig_setup", img)

        # print("detecting")

        if time.monotonic() > e: #and set_hand_sig != 0:
            print("Hand Signal set")
            cv2.imwrite('mp_handdd.jpg', img)
            break

        # if time.monotonic() > e and set_hand_sig == 0:
        #     print("Hand Signal not set, please run HAND SIGNAL setup again")
        #     break

        if cv2.waitKey(1) & 0xFF == ord('q'):
            print(img.shape)
            print(np.sum(img))
            break

        if len(lmList) != 0:
            thum = lmList[4]
            midfing = lmList[12]
            # The cords are id, w, h
            thum_y = lmList[4][2]
            midfing_y = lmList[12][2]
            ringfing_y = lmList[16][2]
            indfing_y = lmList[8][2]
            pinkfing_y = lmList[20][2]
            wrist_y = lmList[0][2]

            thum_x = lmList[4][1]
            midfing_x = lmList[12][1]
            ringfing_x = lmList[16][1]
            indfing_x = lmList[8][1]
            pinkfing_x = lmList[20][1]
            wrist_x = lmList[0][1]

            thum_mid_dif = math.hypot(midfing_x - thum_x, midfing_y - thum_y)  # how he found diff value, is length of line
            thum_ind_dif = math.hypot(indfing_x - thum_x, indfing_y - thum_y)
            thum_ring_dif = math.hypot(ringfing_x - thum_x, ringfing_y - thum_y)
            thum_pink_dif = math.hypot(pinkfing_x - thum_x, pinkfing_y - thum_y)

            mid_wrist_dif = math.hypot(wrist_x - midfing_x, wrist_y - midfing_y)  # how he found diff value, is length of line
            mid_ind_dif = math.hypot(indfing_x - midfing_x, indfing_y - midfing_y)
            mid_ring_dif = math.hypot(ringfing_x - midfing_x, ringfing_y - midfing_y)
            mid_pink_dif = math.hypot(pinkfing_x - midfing_x, pinkfing_y - midfing_y)

            # # from vid: to get mid point cords
            # mx, my = (thum_x + midfing_x) // 2, (thum_y + midfing_y) // 2  # how he found mid point
            # cv2.line(img, (thum_x, thum_y), (midfing_x, midfing_y), (255, 0, 0), 3)
            # # cv2.circle(img, (mx, my), 10, (255, 0, 0), cv2.FILLED)
            # thum_mid_diff2 = math.hypot(midfing_x - thum_x, midfing_y - thum_y)  # how he found diff value, prob is length of line
            # print(thum_mid_diff2)

            # Put all line lengths into an array, then put +/- allowance on it

            ind_base_y = lmList[5][2]
            pink_base_y = lmList[17][2]

            ind_base_x = lmList[5][1]
            pink_base_x = lmList[17][1]

            # Gives length between base of index finger and pinky
            set_palm_w = math.hypot(ind_base_x - pink_base_x, ind_base_y - pink_base_y)

            set_hand_sig = np.array([thum_mid_dif, thum_ind_dif, thum_ring_dif, thum_pink_dif, mid_wrist_dif,
                                     mid_ind_dif, mid_ring_dif, mid_pink_dif, set_palm_w])

    try:
        f = open("myHand1SaveVal2.txt", "a")
        # f.write("\n")
        # [f.write(str(i)) for i in set_hand_sig]
        # for i in list(set_hand_sig):
        #     f.write(str(i))

        f.write(str(set_hand_sig[0]))
        f.write("\n")
        f.write(str(set_hand_sig[1]))
        f.write("\n")
        f.write(str(set_hand_sig[2]))
        f.write("\n")
        f.write(str(set_hand_sig[3]))
        f.write("\n")
        f.write(str(set_hand_sig[4]))
        f.write("\n")
        f.write(str(set_hand_sig[5]))
        f.write("\n")
        f.write(str(set_hand_sig[6]))
        f.write("\n")
        f.write(str(set_hand_sig[7]))
        f.write("\n")
        f.write(str(set_hand_sig[8]))
        f.close()
    except:
        print("Could not SET hand signal setup values, please restart to run HAND SIGNAL setup")

    if len(set_hand_sig) == 9:
        print("Hand signal set")
    else:
        print("Could not SET hand signal setup values, please restart to run HAND SIGNAL setup")

    print("set_hand_sig: ", set_hand_sig)

    # # this way is more for a hard coded set up
    # indiff = thum_mid_dif + thum_ring_dif
    # outdiff = thum_ind_dif + thum_pink_dif
    # ratio = outdiff // indiff
    # # print(ratio)


# now set up save and recieve from txt

# -----------------------------------------------------------


# On start up
# def on_startup():
cap = cv2.VideoCapture(0)
#cap.set(3, 1280)
#cap.set(4, 720)
# # temp -------------
# aoiy1, aoiy2, aoix1, aoix2 = motion_aoi()
# print(aoiy1)
# cap.release()
# sys.exit()
# # temp end -------------

print("Cover camera to run LIGHTING setup, or wait 10 seconds if previously setup")  # or cover camera to read input
# time.sleep(5)
tm = time.monotonic() + 10

while True:
    # print("while loop run")
    ret, start_img = cap.read()
    # cv2.imshow("while loop cap", start_img)
    # print(np.sum(start_img) // 10000)
    if tm < time.monotonic():
        break
    # if cv2.waitKey(1) & 0xFF == ord('s'):
    #     print("Going to setup")
    #     setup()
    if np.sum(start_img) // 10000 < 600:
        print("Going to LIGHTING setup")
        # cap.release()
        setup()
        break

time.sleep(3)
print("Cover camera to run HAND SIGNAL setup, or wait 10 seconds if previously setup")  # or cover camera to read input
tm2 = time.monotonic() + 10
while True:
    # print("while loop run")
    ret, start_img2 = cap.read()
    # cv2.imshow("while loop cap", start_img)
    # print(np.sum(start_img) // 10000)
    if tm2 < time.monotonic():
        break
    # if cv2.waitKey(1) & 0xFF == ord('s'):
    #     print("Going to setup")
    #     setup()
    if np.sum(start_img2) // 10000 < 600:
        print("Going to HAND SIGNAL setup")
        # cap.release()
        handsig_setup()
        break

# f = open("myHand1SaveVal.txt", "r")
# try:
try:
    f = open("myHand1SaveVal.txt", "r")
    light_setval = int(f.readline())
    light_thres = int(f.readline())
    f.close()
    # print("light_val from txt is: ", light_val)
    # print("light_thres from txt is: ", light_thres)
except:
    f = open("myHand1SaveVal.txt", "r+")
    print("Could not retrieve lighting setup values, please restart to run LIGHTING setup")
    f.truncate(0)
    f.close()
    sys.exit()

try:                # see np.genfromtxt, np.loadtxt, np.fromfile
    f = open("myHand1SaveVal2.txt", "r")
    lis = f.read().splitlines()                # gets ride of the \n at end hof each element
    f.close()

    set_hand_sig = np.asarray(list(map(float, lis)))         # best way    converts all elements from strings to floats
    # set_hand_sig = [float(i) for i in lis]       # also works
    print("set_hand_sig from txt is: ", set_hand_sig)
    if len(set_hand_sig) != 9:
        print("****Could not retrieve hand signal setup values, please restart to run HAND SIGNAL setup")
        sys.exit()
except:
    f = open("myHand1SaveVal2.txt", "r+")
    print("Could not retrieve hand signal setup values, please restart to run HAND SIGNAL setup")
    f.truncate(0)
    f.close()
    sys.exit()


# print("lightval ", light_val)
# print("light thres ", light_thres)

# time.sleep(10)
cap.release()  ################
# cv2.destroyAllWindows()
# sys.exit() # ------------------------------


pTime = 0
cTime = 0
cap = cv2.VideoCapture(0)
cap.set(3, 640)           # 320x240  1280x720 1920x1080 default 640x480   max for my cam seems to be 1280x960
cap.set(4, 480)
# cap.set(15, 0.1)
detector = hm.handDetector(False, 1)            #@ just hm added here   set to detect 1 hand
posedet = pm.poseDetector()

# with mp_hqolistic.Holistic(
#     model_complexity=1,
#     min_detection_confidence=0.5,
#     min_tracking_confidence=0.5) as holistic:      # this goes just above while loop with loop indented below

# results = holistic.process(img)    this goes just in side while loop

reset = 1
light = 1
thres = 500   # thres for diffs
todet = 0
cnt = 0         # count to reset, in case the light is block for a few seconds

temp = 0    # for testing


while True:
    ret, img = cap.read()
    # ret2, img2 = cap.read()
    ret, img3 = cap.read()
    # ret4, img4 = cap.read()

    if ret == True:
        # img = detector.findHands(img)                   # add , draw=False to these two in order to not draw
        # lmList = detector.findPosition(img, draw=False)  # leave false?

        # if light detected or if motion detected

        # Activate by motion detection, lights coming on will also trigger
        imdiff = cv2.absdiff(img, img3)
        imdiffs = np.sum(imdiff) // 1000
        # print("imdiffs: ", imdiffs)
        # cv2.imshow("imdiff", imdiff)

        # time.sleep(0.5)

        light_val = np.sum(img) // 10000
        # print("light_thres test ", light_thres)
        # light_thres = 1000

        # thres = light_val + 400             # VV maybe remove this thres can be kept on 500 or use proper motion code
        # print("thresssssssssssss: ", thres)

        if light_val > light_thres:                # try summing just certain color chans see if faster or more accurate
            light = 1
            cnt = 0
        else:
            light = 0
            # thres = 500

        if imdiffs > thres:
            todet = 1
            # print("detected movement")
        else:
            todet = 0

        # print("light = ", light)
        if light == 0 and todet == 0:
            cnt += 1
            time.sleep(0.5)
#             print("counting to reset: ", cnt)
            if cnt > 3:
                reset = 1
                cnt = 0
#                 print("reset = 1")

        print("IN OUTER =======================================")
#         reset = 1   ## part of temp for 3rd while loop
        if temp < time.monotonic() and todet == 1:  ## *** tempoarry for testing
            print("IN INNER ++++++")
#         if todet == 1 and reset == 1:           # no sleep required in lights and motion
        # if light == 1 and reset == 1:         # for just lights or lights and motion with no sleep

            et = time.monotonic() + 9
#             swt = time.monotonic() + 1   # switch time
#             print("***", set_hand_sig)
            set_hand_sig2 = set_hand_sig[0:8]
            set_palm_w = set_hand_sig[8]
#             count = 41
            aoibox_x2 = 0
            aoibox_x1 = 0
            aoibox_y2 = 0
            aoibox_y1 = 0

            while True:
#                 if reset == 0:
#                     break
                
                ret, img = cap.read()    # 320x240  1280x720  default 640x480
#                 print(img.shape, " 00000")
                #xx Pose start -------------
                poseimg = posedet.findPose(img, draw=False)  # add , draw=False to these two in order to not draw # xx img[180:540, 320:960]
                poselmList = posedet.findPosition(poseimg, draw=False)  # xx OR as in PoseEst2.py lmList = detector.findPose(frame, draw=False)

#                 # cv2.imshow("Image 2nd while loop", poseimg)
#                 if count > 50:
#                     count = 0
                    
#                 # added on pi, count replaced with time ** is working best
#                 if swt < time.monotonic():
#                     swt = time.monotonic() + 1  # (was0.5) this only causes delay try while loop for hands
                # -- end ---- 
# 
# #                 if len(poselmList) != 0 and count > 40:  
#                              
#                 # added on pi, count replaced with time **
#                 if len(poselmList) != 0 and swt > time.monotonic() + 0.2:
                ## Seems to work just as good without delaying
                if len(poselmList) != 0:
                    # The cords are id, w, h
                    nose_y = poselmList[0][2]
                    nose_x = poselmList[0][1]

                    r_ear_y = poselmList[8][2]
                    l_ear_y = poselmList[7][2]
                    r_ear_x = poselmList[8][1]
                    l_ear_x = poselmList[7][1]
                    # Gives length between ears
                    det_ears = int(math.hypot(r_ear_x - l_ear_x, r_ear_y - l_ear_y) * 3)


                    #xx decent values, good one, aoi based around nose
                    aoibox_y1 = int(nose_y - det_ears * 0.5)
                    if aoibox_y1 < 0:
                        aoibox_y1 = 0
                    aoibox_y2 = int(nose_y + det_ears * 1)  # was 1
                    if aoibox_y2 > img.shape[0]:
                        aoibox_y2 = img.shape[0]
                    aoibox_x1 = int(nose_x - det_ears * 1.3)  # was 1.2
                    if aoibox_x1 < 0:
                        aoibox_x1 = 0
                    aoibox_x2 = int(nose_x + det_ears * 1.3)
                    if aoibox_x2 > img.shape[1]:
                        aoibox_x2 = img.shape[1]
                    #xx end of aoi based around nose


                    #xx Trying aoi based on hand with smallest y value, might not work as good as above because
                    # arm pose detect is not as stable as face detect
#                     pose_rwrist_y = poselmList[16][2]
#                     pose_lwrist_y = poselmList[15][2]
#                     pose_rwrist_x = poselmList[16][1]
#                     pose_lwrist_x = poselmList[15][1]
# 
#                     if pose_rwrist_y < pose_lwrist_y:
#                         pose_wrist_y = pose_rwrist_y
#                         pose_wrist_x = pose_rwrist_x
#                     else:
#                         pose_wrist_y = pose_lwrist_y
#                         pose_wrist_x = pose_lwrist_x
# 
#                     ##pose_wrist_y = min(pose_rwrist_y, pose_lwrist_y)
# 
#                     aoibox_y1 = int(pose_wrist_y - det_ears * 0.8)
#                     if aoibox_y1 < 0:
#                         aoibox_y1 = 0
#                     aoibox_y2 = int(pose_wrist_y + det_ears * 0.8)
#                     if aoibox_y2 > img.shape[0]:
#                         aoibox_y2 = img.shape[0]
#                     aoibox_x1 = int(pose_wrist_x - det_ears * 0.8)
#                     if aoibox_x1 < 0:
#                         aoibox_x1 = 0
#                     aoibox_x2 = int(pose_wrist_x + det_ears * 0.8)
#                     if aoibox_x2 > img.shape[1]:
#                         aoibox_x2 = img.shape[1]
                    #xx ------------- end of aoi based on hand ---------------

                    # count = 0
#                     print(aoibox_x2, type(aoibox_x2))
#                     print(aoibox_x1, type(aoibox_x1))
#                     print(aoibox_y2, type(aoibox_y2))
#                     print(aoibox_y1, type(aoibox_y1))

                    #xx pose end ------ and aoibox_x1 and aoibox_y2 and aoibox_y1
                
#                 while swt > time.monotonic() + 0.5:
#                     ret, img = cap.read()
#                     
#                     if swt < time.monotonic() + 0.5:
#                         break
                    
                    
                if aoibox_x2 > aoibox_x1 + 20 and aoibox_y2 > aoibox_y1 + 20:      # tab in from here down to go back to old way. New way sees to help, could use time also
#                     count += 1              # xx could make it so that it sets the aoi when the nose moves a distance based on det_ears
                    # img.flags.writeable = False    # speed up
                    img = detector.findHands(img[aoibox_y1:aoibox_y2, aoibox_x1:aoibox_x2]) #xx getting error here try? # add , draw=False to these two in order to not draw   [180:540, 320:960]# vv
                    lmList = detector.findPosition(img, draw=False)  # leave false?

                    cTime = time.time()            # FPS section
                    fps = 1 / (cTime - pTime)
                    pTime = cTime
                    cv2.putText(img, str(int(fps)), (18, 34), cv2.FONT_HERSHEY_PLAIN, 2, (0, 8, 255), 1)

                    cv2.imshow("Image 2nd while loop", img)

                    # print("detecting")

                    # if time.monotonic() > et:
                    #     print("**alarm**")

                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        print(img.shape)
                        print(np.sum(img))
                        break

                    if len(lmList) != 0:
                        thum = lmList[4]
                        midfing = lmList[12]
                        # The cords are id, w, h
                        thum_y = lmList[4][2]
                        midfing_y = lmList[12][2]
                        ringfing_y = lmList[16][2]
                        indfing_y = lmList[8][2]
                        pinkfing_y = lmList[20][2]
                        wrist_y = lmList[0][2]

                        thum_x = lmList[4][1]
                        midfing_x = lmList[12][1]
                        ringfing_x = lmList[16][1]
                        indfing_x = lmList[8][1]
                        pinkfing_x = lmList[20][1]
                        wrist_x = lmList[0][1]


                        # # from vid: to get mid point cords
                        # mx, my = (thum_x + midfing_x) // 2, (thum_y + midfing_y) // 2  # how he found mid point
                        # # cv2.line(img, (thum_x, thum_y), (midfing_x, midfing_y), (255, 0, 0), 3)
                        # # cv2.circle(img, (mx, my), 10, (255, 0, 0), cv2.FILLED)
                        # thum_mid_diff2 = math.hypot(midfing_x - thum_x, midfing_y - thum_y)
                        # print(thum_mid_diff2)

                        thum_mid_dif = math.hypot(midfing_x - thum_x, midfing_y - thum_y)
                        thum_ind_dif = math.hypot(indfing_x - thum_x, indfing_y - thum_y)
                        thum_ring_dif = math.hypot(ringfing_x - thum_x, ringfing_y - thum_y)
                        thum_pink_dif = math.hypot(pinkfing_x - thum_x, pinkfing_y - thum_y)

                        mid_wrist_dif = math.hypot(wrist_x - midfing_x, wrist_y - midfing_y)
                        mid_ind_dif = math.hypot(indfing_x - midfing_x, indfing_y - midfing_y)
                        mid_ring_dif = math.hypot(ringfing_x - midfing_x, ringfing_y - midfing_y)
                        mid_pink_dif = math.hypot(pinkfing_x - midfing_x, pinkfing_y - midfing_y)

                        ind_base_y = lmList[5][2]
                        pink_base_y = lmList[17][2]
                        ind_base_x = lmList[5][1]
                        pink_base_x = lmList[17][1]
                        # Gives length between base of index finger and pinky
                        det_palm_w = math.hypot(ind_base_x - pink_base_x, ind_base_y - pink_base_y)

                        # indiff = thum_mid_dif + thum_ring_dif
                        # outdiff = thum_ind_dif + thum_pink_dif
                        # ratio = outdiff // indiff
                        # # print(ratio)

                        # Put all line lengths into an array, then put +/- allowance on it
                        hand_sig = np.array([thum_mid_dif, thum_ind_dif, thum_ring_dif, thum_pink_dif, mid_wrist_dif,
                                                mid_ind_dif, mid_ring_dif, mid_pink_dif])


                        x = np.allclose(hand_sig, np.multiply(set_hand_sig2, (det_palm_w / set_palm_w)), 0, (det_palm_w * 0.5))

                        
                        if x == True:
                            print("correct, reset = 0")
                            reset = 0
                            print("000000")
                            
                            temp = time.monotonic() + 3
                            
                            # print(np.multiply(hand_sig, 0.8))
                            break


        # cTime = time.time()
        # fps = 1/(cTime-pTime) # causes random error
        # pTime = cTime

        cv2.putText(img, str(int(fps)), (18, 34), cv2.FONT_HERSHEY_PLAIN, 2, (0, 8, 255), 1)

        cv2.imshow("Image", img)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            print(img.shape)
            print(np.sum(img))
            print(img.shape)
            break

    else:
        print("Failed to capture frame")
        break

cap.release()
cv2.destroyAllWindows()

