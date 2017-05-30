#!/usr/bin/env python

# Chloe Fleming & Wendy Xu
# ROB 514
# 5/25/17

import rospy
import smach
import smach_ros
import actionlib
from move_base_msgs.msg import MoveBaseAction

class HideTimeout(smach.State):
	def __init__(self):
		smach.State.__init__(self, outcomes=['hide_done'], input_keys=['hiding_places'], output_keys=['hiding_places'])
		self.client = actionlib.SimpleActionClient('move_base', MoveBaseAction)
		# TODO: create a publisher for sound_play for text-to-speech

	def execute(self, userdata):
		# TODO: make robot travel to middle of room 
		self.client.wait_for_server()
		self.client.send_goal(userdata.hiding_places[-1])
		self.client.wait_for_result()

		# TODO: do something with expressive motion or speech here
		print "You didn't find me! I guess that was a pretty good hiding place."
		return 'hide_done'
		