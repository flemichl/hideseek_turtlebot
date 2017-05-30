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

class Seek(smach.State):
	def __init__(self):
		smach.State.__init__(self, outcomes=['seek_timeout', 'human_found'], input_keys=['hiding_places'], output_keys=['hiding_places'])
		self.client = actionlib.SimpleActionClient('move_base', MoveBaseAction)
		# TODO: create a publisher for sound_play for text-to-speech
		# TODO: create a subscriber belonging to this class that checks camera data for person

	def humanDetectionCallback(data):
		# TODO: do something here to set self.found
		# for now, can just be keyboard input?

		# TODO: somewhere we change found to true	
		return

	def execute(self, userdata):
		# TODO: change this countdown to text-to-speech
		for i in xrange(20):
			print i+1
			sleep(1)
		print 'Ready or not, here I come!'

		self.found = False
		self.client.wait_for_server() #make sure to wait and not interrupt

		# TODO: change this to loop through places in prioritized order and break if person found
		for place in userdata.hiding_places:
			self.client.send_goal(place)
			self.client.wait_for_result() 


		if self.found:
			return 'human_found'
		else:
			return 'seek_timeout'
