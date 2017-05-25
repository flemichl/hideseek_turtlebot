#!/usr/bin/env python

# Chloe Fleming & Wendy Xu
# ROB 514
# 5/25/17

import roslib
import rospy
import smach
import smach_ros
from setup_state import *
from greeting_state import *
from hide_state import *
from hide_timeout_state import *
from robot_found_state import *
from seek_state import *
from seek_timeout_state import *
from human_found_state import *

if __name__ == '__main__':
	rospy.init_node('hideseek_smach')

	sm = smach.StateMachine(outcomes=['GAMEOVER'])
	with sm:
		# transitions is a dictionary that maps state outcome string to the next state (for instance, 'setup_done' transitions to state GREETING)
		smach.StateMachine.add('SETUP', Setup(), transitions={'setup_done':'GREETING'})
		smach.StateMachine.add('GREETING', Greeting(), transitions={'robot_hide':'HIDE', 'robot_seek' : 'SEEK', 'done' : 'GAMEOVER'})
		
		smach.StateMachine.add('HIDE', Hide(), transitions={'hide_timeout':'HIDE_TIMEOUT', 'robot_found': 'ROBOT_FOUND'})
		smach.StateMachine.add('HIDE_TIMEOUT', HideTimeout(), transitions={'hide_done':'GREETING'})
		smach.StateMachine.add('ROBOT_FOUND', RobotFound(), transitions={'hide_done':'GREETING'})
		
		smach.StateMachine.add('SEEK', Seek(), transitions={'seek_timeout':'SEEK_TIMEOUT', 'human_found': 'HUMAN_FOUND'})
		smach.StateMachine.add('SEEK_TIMEOUT', SeekTimeout(), transitions={'seek_done':'GREETING'})
		smach.StateMachine.add('HUMAN_FOUND', HumanFound(), transitions={'seek_done':'GREETING'})
		
	outcome = sm.execute()

