#!/usr/bin/env python

# Chloe Fleming & Wendy Xu
# ROB 514
# 5/25/17

import rospy
import smach
from parse_hiding_places import *
from hiding_places import *

class Setup(smach.State):
	def __init__(self):
		smach.State.__init__(self, outcomes=['setup_done'], input_keys=['hiding_places'], output_keys=['hiding_places'])
		self.vizpub = rospy.Publisher('visualization_marker_array', MarkerArray, queue_size=10, latch=True)

	def execute(self, userdata):
		userdata.hiding_places = HidingPlaces()
		# parse possible hiding places from XML and make these coordinates/rviz markers available
		poses = getPoseList() #from parse xml list of poses
		for pose in poses:
			userdata.hiding_places.addPose(pose)

		# display possible hiding places in rviz (mostly for us to use in debugging)
		self.vizpub.publish(userdata.hiding_places.getMarkers()) 

		return 'setup_done'
