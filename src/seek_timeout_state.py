#!/usr/bin/env python

# Chloe Fleming & Wendy Xu
# ROB 514
# 5/25/17

import rospy
import smach
import smach_ros
import actionlib
from move_base_msgs.msg import MoveBaseAction
from sound_play.libsoundplay import SoundClient

class SeekTimeout(smach.State):
	def __init__(self):
		smach.State.__init__(self, outcomes=['seek_done'], input_keys=['hiding_places'], output_keys=['hiding_places'])
		self.client = actionlib.SimpleActionClient('move_base', MoveBaseAction)
		self.soundhandle = SoundClient(blocking=True)

	def execute(self, userdata):
		self.client.wait_for_server()
		self.client.send_goal(userdata.hiding_places.getHomePosition())
		self.client.wait_for_result()

		# TODO: do something with expressive motion

		print "I can't find you. I give up! You win!"
		self.soundhandle.say('I can\'t find you. I give up! You win!')
		return 'seek_done'
		