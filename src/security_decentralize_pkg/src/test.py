import numpy as np
import cv2
from aruco import pose_estimation, aruco_display, ARUCO_DICT

aruco_type = "DICT_ARUCO_ORIGINAL"

arucoDict = cv2.aruco.Dictionary_get(ARUCO_DICT[aruco_type])

arucoParams = cv2.aruco.DetectorParameters_create()

cap = cv2.VideoCapture("VID_20230518_224046.mp4")
intrinsic_camera = np.array(((933.15867, 0, 657.59),(0,933.1586, 400.36993),(0,0,1)))
distortion = np.array((-0.43948,0.18514,0,0))

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

req_id=1

while cap.isOpened():

    ret, img = cap.read()

    output,rec = pose_estimation(img, ARUCO_DICT[aruco_type], intrinsic_camera, distortion,req_id)
    # print(type(output))
    # print(rec)
    str_coordinate=np.array_str(output)
    print(rec[0][0][0])
    print(rec[0][0][1])

    cv2.imshow('Estimated Pose', output)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
