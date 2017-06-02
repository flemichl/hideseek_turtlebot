#!/usr/bin/env python

# Chloe Fleming & Wendy Xu
# ROB 514
# 5/31/17

from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from visualization_msgs.msg import Marker, MarkerArray
from heapq import heappush, heappop #unfamilar with these
from math import sqrt

class HidingPlaces:
	def __init__(self):
		self.pose_count = 0
		self.poses = {}
		self.navgoals = {}
		self.quality = {}
		self.marker_array = MarkerArray()

	def addPose(self, pose):
		self.pose_count += 1
		px, py, pz, orx, ory, orz, orw, idx = pose
		self.poses[idx] = (px, py, pz, orx, ory, orz, orw)
		self.quality[idx] = 7

		marker = Marker()
		marker.id = idx
		marker.header.frame_id = "map"
		marker.type = marker.CYLINDER
		marker.action = marker.ADD
		marker.scale.x = 0.2
		marker.scale.y = 0.2
		marker.scale.z = 1.0
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

	def getMarkers(self):
		return self.marker_array

	def getHomePosition(self):
		return self.navgoals[self.pose_count - 1]

	def getRankedGoals(self, start_position):
		x0, y0, z0 = start_position
		idx_heap = []

		# exclude last item in list because it is the "home" position
		for i in xrange(self.pose_count - 1):
			px, py, pz, _, _, _, _ = self.poses[i]
			distance = sqrt((px - x0)**2 + (py - y0)**2)
			heappush(idx_heap, (distance, i))
		
		idx_sorted = [heappop(idx_heap) for i in range(len(idx_heap))]
		navgoals_sorted = [self.navgoals[idx] for (d, idx) in idx_sorted]
		return navgoals_sorted

	def getBestHiding(self, start_position):
		x0, y0, z0 = start_position
		idx_heap = []

		# exclude last item in list because it is the "home" position
		for i in xrange(self.pose_count - 1):
			px, py, pz, _, _, _, _ = self.poses[i]
			distance = -1 * sqrt((px - x0)**2 + (py - y0)**2)
			heappush(idx_heap, (distance, i)) #heap stuff
		
		(distance, idx) = heappop(idx_heap)
		return self.navgoals[idx]


		# could make a list to start saving where found