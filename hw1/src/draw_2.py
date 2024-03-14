#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
from math import pi


class Draw2():

    def __init__(self):

        self.X = 0
        self.TURN_ANGLE_1 = pi/2
        self.TURN_ANGLE_2 = 1.215


    def turn(self, publisher, rate, angle):

        turn_vel_msg = Twist()
        turn_vel_msg.angular.z = angle
        turn1_time_to_complete = (pi * 1) / (pi-turn_vel_msg.angular.z)

        start_turn1_time = rospy.Time.now().to_sec()
        while rospy.Time.now().to_sec() - start_turn1_time < turn1_time_to_complete:
            publisher.publish(turn_vel_msg)
            rate.sleep()

        turn_vel_msg.angular.z = 0
        publisher.publish(turn_vel_msg)


    def circle(self, publisher, rate, angle):

        circle_vel_msg = Twist()
        circle_vel_msg.linear.x = angle
        circle_vel_msg.angular.z = -1 
        circle_time_to_complete = (pi * 1) / abs(circle_vel_msg.linear.x) + 1.05

        start_circle_time = rospy.Time.now().to_sec()
        while rospy.Time.now().to_sec() - start_circle_time < circle_time_to_complete:
            publisher.publish(circle_vel_msg)
            rate.sleep()

        circle_vel_msg.linear.x = 0
        circle_vel_msg.angular.z = 0
        publisher.publish(circle_vel_msg)


    def straight(self, publisher, rate, threshold):

        st_vel_msg = Twist()
        st_vel_msg.linear.x = 1

        while abs(self.X - threshold) > 0.5:
            publisher.publish(st_vel_msg)
            rate.sleep()

        st_vel_msg.linear.x = 0
        publisher.publish(st_vel_msg)


    def poseCallback(self, pose_message):
        
        self.X = pose_message.x


    def draw_two(self):

        rospy.init_node('draw_circle_node', anonymous=True)
        velocity_publisher = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)
        rospy.Subscriber("/turtle1/pose", Pose, self.poseCallback) 
        r_rate = rospy.Rate(1)

        # 90 degree turn
        self.turn(velocity_publisher, r_rate, self.TURN_ANGLE_1)

        # Draw the semi circle
        self.circle(velocity_publisher, r_rate, self.TURN_ANGLE_1)    

        # First straight
        self.straight(velocity_publisher, r_rate, 5)
        
        # Last turn
        self.turn(velocity_publisher, r_rate, self.TURN_ANGLE_2)

        # Last straight
        self.straight(velocity_publisher, r_rate, 8.8)
    

        rospy.spin()

if __name__ == '__main__':
    try:
        draw_2 = Draw2()
        draw_2.draw_two()

    except rospy.ROSInterruptException:
        pass
