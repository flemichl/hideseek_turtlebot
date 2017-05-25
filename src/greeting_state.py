#!/usr/bin/env python

# Chloe Fleming & Wendy Xu
# ROB 514
# 5/25/17

import rospy
import smach

class Greeting(smach.State):
	def __init__(self):
		smach.State.__init__(self, outcomes=['robot_hide', 'robot_seek', 'done'], input_keys=['hiding_places'], output_keys=['hiding_places'])
		# TODO: create a publisher for sound_play for text-to-speech
		
	def execute(self, userdata):
		# TODO: change this interaction to text-to-speech by publishing some things to sound_play node
		choice = raw_input("Would you like to play again? (y/n)")

		if len(choice) > 0 and (choice[0] == 'y' or choice[0] == 'Y'):	
			choice = raw_input("Should I hide or seek? (hide/seek)")

			while True:
				if choice == 'hide':
					print 'Ok, count to 20 while I go hide!'
					return 'robot_hide'

				elif choice == 'seek':
					print 'Ok, I will count to 20 while you hide!'
					return 'robot_seek'

				else:
					print 'Sorry, I don\'t know how to do that!'

		else:
			print'Ok, let\'s play again sometime!'
		
		return 'done'
