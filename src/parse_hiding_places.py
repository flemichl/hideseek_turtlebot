#!/usr/bin/env python

# Chloe Fleming
# ROB 514
# 11/11/16

import rospkg
from xml.dom import minidom

def parseFromXML(poses):
	poses_xml = poses.getElementsByTagName("pose")
	pose_list = []
	for (i, pose) in enumerate(poses_xml):
		pose_list.append(handlePose(pose, i))
	return pose_list

def handlePose(pose, idx):
	position = pose.getElementsByTagName("position")[0]
	orientation = pose.getElementsByTagName("orientation")[0]
	print position.toxml()
	print orientation.toxml()

	orx = float(orientation.attributes["x"].value)
	ory = float(orientation.attributes["y"].value)
	orz = float(orientation.attributes["z"].value)
	orw = float(orientation.attributes["w"].value)
	px = float(position.attributes["x"].value)
	py = float(position.attributes["y"].value)
	pz = float(position.attributes["z"].value)

	return (px, py, pz, orx, ory, orz, orw, idx)

def getPoseList():
	rospack = rospkg.RosPack()
	xml_path = rospack.get_path("hideseek_turtlebot") + "/maps/hiding_places.xml"
	poses = minidom.parse(xml_path)
	pose_list = parseFromXML(poses)
	return pose_list


