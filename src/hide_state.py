#!/usr/bin/env python

# Chloe Fleming & Wendy Xu
# ROB 514
# 5/25/17

import rospy
import smach
import smach_ros
import actionlib
from move_base_msgs.msg import MoveBaseAction
from time import sleep
from std_msgs.msg import String

def humanDetectionCallback(message):
	global found
	# TODO: change this to a cmvision callback
	if 'found' in message.data:
		found = True
	return

class Hide(smach.State):
	def __init__(self):
		smach.State.__init__(self, outcomes=['hide_timeout', 'robot_found'], input_keys=['hiding_places'], output_keys=['hiding_places'])
		self.client = actionlib.SimpleActionClient('move_base', MoveBaseAction) # we send navgoals, like a pub that waits for response
		# TODO: create a subscriber belonging to this class that checks camera data for person
		self.keysubscriber = rospy.Subscriber('/hideseek/keyinput', String, humanDetectionCallback)

	def execute(self, userdata):
		global found
		found = False
		self.client.wait_for_server()

		# TODO: change this to pick the "best" hiding place or random
		self.client.wait_for_server()
		self.client.send_goal(userdata.hiding_places[0])
		self.client.wait_for_result()

		for i in xrange(30):
			sleep(1)
			if found:
				return 'robot_found'
		
		return 'hide_timeout'

		