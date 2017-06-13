#!/usr/bin/env python

# Chloe Fleming & Wendy Xu
# ROB 599
# 5/25/17

import rospy
import smach
import smach_ros
import actionlib
from move_base_msgs.msg import MoveBaseAction
from sound_play.libsoundplay import SoundClient
from time import sleep, time
from std_msgs.msg import String
from geometry_msgs.msg import PoseWithCovarianceStamped
from cmvision_3d.msg import Blobs3d

# leaving this for convenience of testing other features without doing player color calibration
def manualCallback(message):
	global found
	if 'found' in message.data:
		found = True
		print "Manually detected human player."
	return

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
		# controlling navigation stack
		self.client = actionlib.SimpleActionClient('move_base', MoveBaseAction)

		# text-to-speech
		self.soundhandle = SoundClient(blocking=True)

		# human player detection
		self.blob_subscriber = rospy.Subscriber('/blobs_3d', Blobs3d, humanDetectionCallback) 
		self.key_subscriber = rospy.Subscriber('/hideseek/keyinput', String, manualCallback)
		self.pose_subscriber = rospy.Subscriber('/amcl_pose', PoseWithCovarianceStamped, poseCallback)

	def execute(self, userdata):
		global found, position
		found = False
		hiding_place = userdata.hiding_places.getBestHiding((position.x, position.y, position.z))
		userdata.hiding_places.updatePlaceHistory(hiding_place)
		
		self.client.wait_for_server()
		self.client.send_goal(hiding_place)
		self.client.wait_for_result()

		#wait for a certain amount of time before it gives up
		hide_time = time()
		for i in xrange(30):
			sleep(1)
			if found:
				userdata.hiding_places.updateTimeStats(hiding_place, time() - hide_time)
				return 'robot_found'
		
		userdata.hiding_places.updateTimeStats(hiding_place, time() - hide_time)
		return 'hide_timeout'

		