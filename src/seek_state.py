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
from std_msgs.msg import String
from geometry_msgs.msg import PoseWithCovarianceStamped
from cmvision_3d.msg import Blobs3d

'''def humanDetectionCallback(message):
	global found
	# TODO: change this to a cmvision callback
	if 'found' in message.data:
		found = True
		print "message"
	return'''

def humanDetectionCallback(data):
	global found
	
	# if we see a blob of the player's color, then we found them!
	if len(data.blobs) > 0:
		found = True

	# TODO: us tf to translate blob from camera frame into map
	# add the player's location (from blob tf) as a new hiding place

def poseCallback(data):
	global position
	position = data.pose.pose.position

class Seek(smach.State):
	def __init__(self):
		smach.State.__init__(self, outcomes=['seek_timeout', 'human_found'], input_keys=['hiding_places'], output_keys=['hiding_places'])
		self.client = actionlib.SimpleActionClient('move_base', MoveBaseAction)
		self.soundhandle = SoundClient(blocking=True)
		self.blob_subscriber = rospy.Subscriber('/blobs_3d', Blobs3d, humanDetectionCallback) 
		#self.key_subscriber = rospy.Subscriber('/hideseek/keyinput', String, humanDetectionCallback)
		self.pose_subscriber = rospy.Subscriber('/amcl_pose', PoseWithCovarianceStamped, poseCallback)

	def execute(self, userdata):
		global found, position
		for i in xrange(4):
			self.soundhandle.stopAll()
			print i+1
			self.soundhandle.say(str(i+1))
		self.soundhandle.stopAll()
		print '10. Ready or not, here I come!'
		self.soundhandle.say('Ready or not, here I come!')

		found = False
		self.client.wait_for_server() #make sure to wait and not interrupt

		print "ranking hiding places by distance from", position #I don't remember seeing this output
		#puts ranked goals in a list to interate through
		#I need to ask how userdata works?
		ranked_places = userdata.hiding_places.getRankedGoals((position.x, position.y, position.z))
		
		# TODO: interrupt nav goal if found has been set
		for place in ranked_places:
			self.client.send_goal(place)
			self.client.wait_for_result()
			self.soundhandle.stopAll()
			print 'Are you there?' 
			self.soundhandle.say('Are you there?')
			#TODO test when the "found" statement needs to be sent
			if found:
				return 'human_found'

		return 'seek_timeout'
