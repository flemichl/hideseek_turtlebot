#!/usr/bin/env python

# Chloe Fleming & Wendy Xu
# ROB 514
# 5/25/17

import rospy
import smach
import smach_ros

class HumanFound(smach.State):
	def __init__(self):
		smach.State.__init__(self, outcomes=['seek_done'], input_keys=['hiding_places'], output_keys=['hiding_places'])
		# TODO: create a publisher for sound_play for text-to-speech

	def execute(self, userdata):
		# TODO: do something with expressive motion or speech here
		print "Found you!"
		return 'seek_done'
		