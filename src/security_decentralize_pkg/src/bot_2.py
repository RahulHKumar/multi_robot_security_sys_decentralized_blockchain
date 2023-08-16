#!/usr/bin/env python
import rospy
import os
# import matplotlib.pyplot as plt
# import numpy as np
from security_decentralize_pkg.msg import custom_1
from security_decentralize_pkg.msg import custom_2
from security_decentralize_pkg.msg import custom_3
from security_decentralize_pkg.msg import block2
from security_decentralize_pkg.msg import malicious_flags
import math


import hashlib

import numpy as np
import cv2
from aruco import pose_estimation, aruco_display, ARUCO_DICT

t1=""
t3=""
t2=""
# x1=2
# x2=-1
# x3=3
# y1=3
# y2=-1
# y3=2
#
# plt.scatter(x2,y2,color='blue')
# plt.arrow(x1,y1,0.25,0,ec="green",head_width=0.1)
# x=np.array([x1,x3])
# y=np.array([y1,y3])
# plt.scatter(x,y,color='red')
# plt.arrow(x2,y2,-0.25,0,ec="green",head_width=0.1)
# plt.arrow(x3,y3,0,0.25,ec="green",head_width=0.1)
# plt.title("Robot 2")
# plt.grid()
# plt.xlim([-5,5])
# plt.ylim([-5,5])
# plt.show()


def create_hash_from_transaction(s):
    str1 = ""

    for ele in s:
        str1 += ele
    h=hashlib.sha256(str1.encode()).hexdigest()
    return h
    rospy.loginfo(str1)
    rospy.loginfo(hashlib.sha256(str1.encode()).hexdigest())

def talker():
    aruco_type = "DICT_ARUCO_ORIGINAL"

    arucoDict = cv2.aruco.Dictionary_get(ARUCO_DICT[aruco_type])

    arucoParams = cv2.aruco.DetectorParameters_create()

    cap = cv2.VideoCapture("VID_20230518_224046.mp4")
    intrinsic_camera = np.array(((933.15867, 0, 657.59),(0,933.1586, 400.36993),(0,0,1)))
    distortion = np.array((-0.43948,0.18514,0,0))

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    req_id=2

    pub=rospy.Publisher('message_client2',custom_2,queue_size=1000)
    pub_hash=rospy.Publisher('client2_hash',block2,queue_size=1000)
    rospy.Subscriber('message_client1',custom_1,sub1)
    # rospy.Subscriber('message_client3',custom_3,sub3)
    rospy.Subscriber('mal_bot_flag',malicious_flags,sub_flag)
    rospy.init_node('custom_talker_2',anonymous=True)

    r=rospy.Rate(1)

    msg=custom_2()
    msg2=block2()

    msg.robot_name.data="Robot_2"

    # msg.location.x=-1.0
    # msg.location.y=-1.0
    msg.location.theta=-90.0

    while not rospy.is_shutdown():
        ret, img = cap.read()

        output,rec = pose_estimation(img, ARUCO_DICT[aruco_type], intrinsic_camera, distortion,req_id)

        msg.location.x=math.ceil(rec[0][0][0]/10)
        msg.location.y=math.ceil(rec[0][0][1]/10)

        rospy.loginfo("robot1")
        rospy.loginfo(msg)
        pub.publish(msg)
        t2="x="+str(msg.location.x)+","+"y="+str(msg.location.y)+","+"w="+str(msg.location.theta)
        # rospy.loginfo(t1)
        # rospy.loginfo(t2)
        # rospy.loginfo(t3)
        hash2=create_hash_from_transaction([str(t1),str(t2),str(t3)])

        rospy.loginfo("hash=")
        rospy.loginfo(hash2)
        msg2.robot_hash.data=hash2
        pub_hash.publish(msg2)

        cv2.imshow('Estimated Pose', output)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        # r.sleep()
        rospy.sleep(2.5)

    cap.release()
    cv2.destroyAllWindows()


def sub1(data1):
    global t1
    # rospy.loginfo("robot1")
    # rospy.loginfo(data1)
    t1="x="+str(data1.location.x)+","+"y="+str(data1.location.y)+","+"w="+str(data1.location.theta)


def sub3(data3):
    global t3
    # rospy.loginfo("robot3")
    # rospy.loginfo(data3)
    t3="x="+str(data3.location.x)+","+"y="+str(data3.location.y)+","+"w="+str(data3.location.theta)

def sub_flag(data_flag):
    flag="0"
    flag=data_flag.bot2_mal.data
    if(flag=="1"):
        rospy.loginfo("Malicious bot 2 killed")
        os._exit(0)

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
