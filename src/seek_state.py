#!/usr/bin/env python

# Chloe Fleming & Wendy Xu
# ROB 599
# 5/25/17

import rospy
import smach
import smach_ros
import actionlib
from actionlib_msgs.msg import GoalID
from move_base_msgs.msg import MoveBaseAction
from sound_play.libsoundplay import SoundClient
from std_msgs.msg import String
from geometry_msgs.msg import PoseWithCovarianceStamped
from cmvision_3d.msg import Blobs3d
from time import time

# leaving this for convenience of testing other features without doing player color calibration
def manualCallback(message):
	global found
	if 'found' in message.data:
		found = True
		# cancel all navigation goals 
		# this way, robot will stop moving as soon as it has identified the human player
		self.move_cancel.publish(GoalID())
		print "Manually detected human player."
	return

def humanDetectionCallback(data):
	global found
	
	# if we see a blob of the player's color, then we found them!
	if len(data.blobs) > 0:
		found = True
		# cancel all navigation goals 
		# this way, robot will stop moving as soon as it has identified the human player
		self.move_cancel.publish(GoalID())

	# TODO: us tf to translate blob from camera frame into map
	# add the player's location (from blob tf) as a new hiding place

def poseCallback(data):
	global position
	position = data.pose.pose.position

class Seek(smach.State):
	def __init__(self):
		smach.State.__init__(self, outcomes=['seek_timeout', 'human_found'], input_keys=['hiding_places'], output_keys=['hiding_places'])
		# controlling navigation stack
		self.client = actionlib.SimpleActionClient('move_base', MoveBaseAction)
		self.move_cancel = rospy.publisher("/move_base/cancel", GoalID, queue_size=10)

		# text-to-speech
		self.soundhandle = SoundClient(blocking=True)

		# human player detection
		self.blob_subscriber = rospy.Subscriber('/blobs_3d', Blobs3d, humanDetectionCallback) 
		self.key_subscriber = rospy.Subscriber('/hideseek/keyinput', String, manualCallback)
		self.pose_subscriber = rospy.Subscriber('/amcl_pose', PoseWithCovarianceStamped, poseCallback)

	def execute(self, userdata):
		global found, position
		for i in xrange(5):
			self.soundhandle.stopAll()
			print i+1
			self.soundhandle.say(str(i+1))
		self.soundhandle.stopAll()
		print 'Ready or not, here I come!'
		self.soundhandle.say('Ready or not, here I come!')

		found = False
		self.client.wait_for_server() #make sure to wait and not interrupt

		#puts ranked goals in a list to interate through
		#I need to ask how userdata works?
		ranked_places = userdata.hiding_places.getRankedGoals((position.x, position.y, position.z))
		phrases = ["Are you there?", "Not here either.", "I'm having trouble finding you.", "I don't want to play anymore!"]

		start_time = time()
		for (i, phrase) in enumerate(phrases):
			place = ranked_places[i]
			self.client.send_goal(place)
			# if we see the human player while navigating, we will interrupt current nav goal
			# waiting for result will return with a failure status
			self.client.wait_for_result()

			# check to see if human has been detected
			if found:
				userdata.hiding_places.updateTimeStats(place, time() - start_time)
				return 'human_found'

			print phrase
			self.soundhandle.stopAll()
			self.soundhandle.say(phrase)

		# robot doesn't know where human was, so can't update statistics
		# this is an interesting part of human gameplay too!
		return 'seek_timeout'
