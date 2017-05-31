#!/usr/bin/env python

# Chloe Fleming & Wendy Xu
# ROB 514
# 5/25/17

import rospy
import smach
from sound_play.libsoundplay import SoundClient

class Greeting(smach.State):
	def __init__(self):
		smach.State.__init__(self, outcomes=['robot_hide', 'robot_seek', 'done'], input_keys=['hiding_places'], output_keys=['hiding_places'])
		self.soundhandle = SoundClient(blocking=True)
		
	def execute(self, userdata):
		print "Would you like to play again? (y/n)"
		self.soundhandle.say('Would you like to play again?')
		choice = raw_input()

		if len(choice) > 0 and (choice[0] == 'y' or choice[0] == 'Y'):	
			print "Should I hide or seek? (hide/seek)"
			self.soundhandle.say('Should I hide or seek?')
			rolechoice = raw_input()

			if 'hide' in rolechoice:
				self.soundhandle.say('Ok, close your eyes and count to 10 while I go hide!')
				print 'OOk, close your eyes and count to 10 while I go hide!'
				return 'robot_hide'

			elif 'seek' in rolechoice:
				self.soundhandle.say('Ok, I will count to 10 while you hide')
				print 'Ok, I will count to 10 while you hide!'
				return 'robot_seek'

			else: #if they are silly and chose something else
				self.soundhandle.say('Sorry, I don\'t know how to do that!')
				print 'Sorry, I don\'t know how to do that!'

		else: #they've selected "N" or "hi wendy"
			self.soundhandle.say('Ok, let\'s play again sometime!')
			print'Ok, let\'s play again sometime!'
		
		return 'done'
