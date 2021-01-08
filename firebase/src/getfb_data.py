#!/usr/bin/env python

import rospy
from std_msgs.msg import String
from geometry_msgs.msg import Twist
import pyrebase
import time
import os
import re
import math
import sys 

def num2str(argument): 
    switcher = { 
        0: "Z", 
        1: "A", 
        2: "B",
        3: "C", 
    }  
    return switcher.get(int(argument), "Nothing") 

def firebase_node():
    rospy.loginfo("Setting Up the Node...")
    rospy.init_node('firebase_node', anonymous=True)

    config = {
        "apiKey": "AAAA6BYFJnA:APA91bESUm5sRscZLxe2ey74U4dGHHkqkGXz04SC4xHvzRbPBEGBGm92EMbk9SWcgTv9D_NCHKtXRxXKwfXhNClWyi9JxB6IhnrukG0Vv3rOvhCl7gm0L_aKoIqR21TV7fKr1eNOnMQd",
        "authDomain": "scooby-a36d6.firebaseapp.com",
        "databaseURL": "https://scooby-a36d6-default-rtdb.firebaseio.com/",
        "storageBucket": "scooby-a36d6.appspot.com"
    }

    firebase = pyrebase.initialize_app(config)
    db = firebase.database()
    
    rate = rospy.Rate(10) # 10hz
    
    prev_goal = "Z"
    
    while not rospy.is_shutdown():
        user = db.child("move_goal").get()
        a = str(user.val())
        b = re.findall(r"[-+]?\d*\.\d+|\d+",a)
        #rospy.loginfo("Goal: "+b[1]+" "+ "status: "+b[0])
        
        goal = num2str(b[1])

        if not goal == prev_goal:
            rospy.loginfo("New Goal: "+goal)
            #rospy.loginfo(num2str(b[1]))
            file1 = open("./src/turtlebot3_project/myfile.txt","w") 
            file1.write(num2str(b[1]))
            file1.close()
            prev_goal = goal
            os.system("rosrun turtlebot3_navigation navigator.py")

        rate.sleep()


if __name__ == '__main__':
    try:
        firebase_node()
    except rospy.ROSInterruptException:
        pass
