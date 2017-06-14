#!/usr/bin/env python

# Chloe Fleming & Wendy Xu
# ROB 514
# 5/31/17

from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from visualization_msgs.msg import Marker, MarkerArray
from heapq import heappush, heappop #unfamilar with these
from math import sqrt
from collections import defaultdict

class HidingPlaces:
	def __init__(self):
		self.pose_count = 0
		self.poses = {}
		self.navgoals = {}
		self.history = {}
		self.timestats = defaultdict(list)
		self.marker_array = MarkerArray()

	def addPose(self, pose):
		px, py, pz, orx, ory, orz, orw = pose
		idx = self.pose_count
		self.poses[idx] = (px, py, pz, orx, ory, orz, orw)
		self.pose_count += 1

		marker = Marker()
		marker.id = idx
		marker.header.frame_id = "map"
		marker.type = marker.CYLINDER
		marker.action = marker.ADD
		marker.scale.x = 0.2
		marker.scale.y = 0.2
		marker.scale.z = 1.0

		# set home position marker red
		# all other markers should be blue
		if idx == 0:
			marker.color.a = 1.0
			marker.color.r = 1.0
			marker.color.g = 0.0
			marker.color.b = 0.0
		else:
			marker.color.a = 1.0
			marker.color.r = 0.0
			marker.color.g = 0.0
			marker.color.b = 1.0

		marker.pose.orientation.x = orx
		marker.pose.orientation.y = ory
		marker.pose.orientation.z = orz
		marker.pose.orientation.w = orw
		marker.pose.position.x = px
		marker.pose.position.y = py
		marker.pose.position.z = pz
		self.marker_array.markers.append(marker)

		goal = MoveBaseGoal()
		goal.target_pose.pose.position.x = px
		goal.target_pose.pose.position.y = py
		goal.target_pose.pose.position.z = pz
		goal.target_pose.pose.orientation.x = orx
		goal.target_pose.pose.orientation.y = ory
		goal.target_pose.pose.orientation.z = orz
		goal.target_pose.pose.orientation.w = orw
		goal.target_pose.header.frame_id = "map"
		self.navgoals[idx] = goal
		self.history[goal] = 0

	def getMarkers(self):
		return self.marker_array

	# home position will be stored as first entry in hiding place list
	def getHomePosition(self):
		return self.navgoals[0]

	# keep a list of how long it took human/robot player to be found at a certain hiding place
	def updateTimeStats(self, hiding_place, seektime):
		print "Updating time stats with", seektime
		self.timestats[hiding_place].append(seektime)

	# keep track of where players have been hiding
	def updatePlaceHistory(self, hiding_place):
		print "Updating hiding place history..."
		# contribution of previous turns decreases by half with each successive turn
		for i in xrange(1, self.pose_count):
			self.history[self.navgoals[i]] *= 0.5

		# set contribution of last hiding place/turn to 1
		self.history[hiding_place] = 1

	# compute quality metric based on distance, hiding history, and avg seek time
	# set A, B, and C to tune contributions of these three factors
	def placeQualityForHiding(self, i, start_position, A=2, B=-10, C=0.5):
		place = self.navgoals[i]
		x0, y0, z0 = start_position
		px, py, pz, _, _, _, _ = self.poses[i]
		distance = sqrt((px - x0)**2 + (py - y0)**2)

		if len(self.timestats[place]) > 0:
			avgtime = sum(self.timestats[place]) / len(self.timestats[place])
		else:
			avgtime = 300 # arbitrary high maximum time value

		# factors in a good hiding place:
		# far from current location (A >= 1)
		# not recently used (B < 0)
		# not quickly found (C >= 1)
		quality = (A * distance) + (B * self.history[place]) + (C * avgtime)
		print "Place", i, ":", "quality=", quality, "distance=", distance, "history=", self.history[place], "time=", avgtime
		return quality

	def placeQualityForSeeking(self, i, start_position):
		# factors in ranking seeking places:
		# start with places nearby (A < 0)
		# not recently used (B < 0)
		# not quickly found (C >= 1)
		return self.placeQualityForHiding(i, start_position, A=-2)	

	def getRankedGoals(self, start_position):
		idx_heap = []

		# exclude last item in list because it is the "home" position
		for i in xrange(1, self.pose_count):
			quality = self.placeQualityForSeeking(i, start_position)
			heappush(idx_heap, (-1*quality, i)) #heap stuff
			# this will automatically put smallest value on top of heap (so we should make quality negative)
		
		idx_sorted = [heappop(idx_heap) for i in range(len(idx_heap))]
		print "Hiding places will be visited in this order:", idx_sorted
		navgoals_sorted = [self.navgoals[idx] for (q, idx) in idx_sorted]
		return navgoals_sorted

	def getBestHiding(self, start_position):
		x0, y0, z0 = start_position
		idx_heap = []

		# exclude last item in list because it is the "home" position
		for i in xrange(1, self.pose_count):
			quality = self.placeQualityForHiding(i, start_position)
			heappush(idx_heap, (-1*quality, i)) #heap stuff
			# this will automatically put smallest value on top of heap (so we should make quality negative)
		
		(quality, idx) = heappop(idx_heap) # get the best hiding place (smallest negative quality)
		print "Best hiding:", quality, idx, self.poses[idx]
		return self.navgoals[idx]

