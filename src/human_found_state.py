#!/usr/bin/env python

# Chloe Fleming & Wendy Xu
# ROB 599
# 5/25/17

import rospy
import smach
import smach_ros
from sound_play.libsoundplay import SoundClient

class HumanFound(smach.State):
	def __init__(self):
		smach.State.__init__(self, outcomes=['seek_done'], input_keys=['hiding_places'], output_keys=['hiding_places'])
		self.soundhandle = SoundClient(blocking=True)

	def execute(self, userdata):
		# TODO: do something with expressive motion
		self.soundhandle.stopAll()
		print "I found you! I win!"
		self.soundhandle.say('I found you! I win!')
		return 'seek_done'
		