#!/usr/bin/env python

# Chloe Fleming
# ROB 514
# 11/11/16

import rospy
from std_msgs.msg import String

if __name__ == '__main__':
	rospy.init_node('tour_keyinput')
	pub = rospy.Publisher('/hideseek/keyinput', String, queue_size=10)

	text = "go"
	while text[0] != 'q':
		text = raw_input()
		message = String()
		message.data = text
		pub.publish(message)
		
