#!/usr/bin/env python

# Chloe Fleming
# ROB 514
# 11/11/16

import rospkg
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from visualization_msgs.msg import Marker, MarkerArray
from xml.dom import minidom

def parseFromXML(poses):
	poses_xml = poses.getElementsByTagName("pose")
	pose_list = []
	for (i, pose) in enumerate(poses_xml):
		pose_list.append(handlePose(pose, i, len(poses_xml)))
	return pose_list

def handlePose(pose, idx, count):
	position = pose.getElementsByTagName("position")[0]
	orientation = pose.getElementsByTagName("orientation")[0]
	print position.toxml()
	print orientation.toxml()

	marker = Marker()
	marker.id = idx
	marker.header.frame_id = "map"
	marker.type = marker.CYLINDER
	marker.action = marker.ADD
	marker.scale.x = 0.2
	marker.scale.y = 0.2
	marker.scale.z = 1.0
	marker.color.a = 1.0
	marker.color.r = float(idx) / count
	marker.color.g = 0.0
	marker.color.b = 1.0 - float(idx) / count
	marker.pose.orientation.x = float(orientation.attributes["x"].value)
	marker.pose.orientation.y = float(orientation.attributes["y"].value)
	marker.pose.orientation.z = float(orientation.attributes["z"].value)
	marker.pose.orientation.w = float(orientation.attributes["w"].value)
	marker.pose.position.x = float(position.attributes["x"].value)
	marker.pose.position.y = float(position.attributes["y"].value)
	marker.pose.position.z = float(position.attributes["z"].value)

	goal = MoveBaseGoal()
	goal.target_pose.pose.position.x = float(position.attributes["x"].value)
      	goal.target_pose.pose.position.y = float(position.attributes["y"].value)
	goal.target_pose.pose.position.z = float(position.attributes["y"].value)
      	goal.target_pose.pose.orientation.x = float(orientation.attributes["x"].value)
      	goal.target_pose.pose.orientation.y = float(orientation.attributes["y"].value)
      	goal.target_pose.pose.orientation.z = float(orientation.attributes["z"].value)
      	goal.target_pose.pose.orientation.w = float(orientation.attributes["w"].value)
	goal.target_pose.header.frame_id = "map"

	return (marker, goal)

def getHidingPlaces():
	rospack = rospkg.RosPack()
	xml_path = rospack.get_path("hideseek_turtlebot") + "/maps/hiding_places.xml"
	poses = minidom.parse(xml_path)
	pose_list = parseFromXML(poses)
	return pose_list


