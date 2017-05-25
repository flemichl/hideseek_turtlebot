#!/usr/bin/env python

# Chloe Fleming & Wendy Xu
# ROB 514
# 5/25/17

import rospy
import smach
from parse_hiding_places import *

class Setup(smach.State):
	def __init__(self):
		smach.State.__init__(self, outcomes=['setup_done'], output_keys=['hiding_places'])
		self.vizpub = rospy.Publisher('visualization_marker_array', MarkerArray, queue_size=10)

	def execute(self, userdata):
		hiding_places = []
		marker_array = MarkerArray()
		# parse possible hiding places from XML and make these coordinates/rviz markers available
		places_markers = getHidingPlaces()
		for (marker, pose) in places_markers:
			marker_array.markers.append(marker)
			hiding_places.append(pose)

		# display possible hiding places in rviz (mostly for us to use in debugging)
		self.vizpub.publish(marker_array) 
		userdata.hiding_places = hiding_places[:]

		return 'setup_done'
