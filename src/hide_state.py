#!/usr/bin/env python

# Chloe Fleming & Wendy Xu
# ROB 599
# 5/25/17

import rospy
import smach
import smach_ros
import actionlib
from move_base_msgs.msg import MoveBaseAction
from time import sleep
from std_msgs.msg import String
from geometry_msgs.msg import PoseWithCovarianceStamped
from cmvision_3d.msg import Blobs3d

'''def humanDetectionCallback(message):
	global found
	# TODO: change this to a cmvision callback
	if 'found' in message.data:
		found = True
	return'''

def humanDetectionCallback(data):
	global found
	
	# if we see a blob of the player's color, then they found us!
	if len(data.blobs) > 0:
		found = True

def poseCallback(data):
	global position
	position = data.pose.pose.position

class Hide(smach.State):
	def __init__(self):
		smach.State.__init__(self, outcomes=['hide_timeout', 'robot_found'], input_keys=['hiding_places'], output_keys=['hiding_places'])
		self.client = actionlib.SimpleActionClient('move_base', MoveBaseAction) # we send navgoals, like a pub that waits for response
		self.blob_subscriber = rospy.Subscriber('/blobs_3d', Blobs3d, humanDetectionCallback) 
		#self.key_subscriber = rospy.Subscriber('/hideseek/keyinput', String, humanDetectionCallback)
		self.pose_subscriber = rospy.Subscriber('/amcl_pose', PoseWithCovarianceStamped, poseCallback)

	def execute(self, userdata):
		global found, position
		found = False

		self.client.wait_for_server()
		self.client.send_goal(userdata.hiding_places.getBestHiding((position.x, position.y, position.z)))
		self.client.wait_for_result()

		#wait for a certain amount of time before it gives up
		for i in xrange(30):
			sleep(1)
			if found:
				return 'robot_found'
		
		return 'hide_timeout'

		