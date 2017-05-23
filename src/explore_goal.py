#!/usr/bin/env python

# Chloe Fleming
# ROB 599
# 5/23/17

import rospy
import actionlib
from frontier_exploration.msg import ExploreTaskAction, ExploreTaskGoal
import std_msgs.msg

# see end of this file for an example complete messsage generated with rviz
def pubExplorationGoal(x, y):
    goal = ExploreTaskGoal()
    #action.action_goal.header = std_msgs.msg.Header()
    #action.action_goal.header.stamp = rospy.Time.now()
    #goal.explore_center.header.frame_id = 'map'
    goal.explore_boundary.header.frame_id = 'map'
    goal.explore_center.point.x = x
    goal.explore_center.point.y = y
    explore_client.send_goal(goal)
    explore_client.wait_for_result(rospy.Duration.from_sec(5.0))

if __name__ == '__main__':
  rospy.init_node('explore_goal')
  explore_client = actionlib.SimpleActionClient('explore_server', ExploreTaskAction)
  explore_client.wait_for_server()
  
  # subscribe to another node that will indicate when it is time to sweep the room
  #rospy.Subscriber('???', MoveBaseActionResult, pubExplorationGoal)

  pubExplorationGoal(5, 5)

  rospy.spin()


# an example complete exploration goal message:
'''
header: 
  seq: 0
  stamp: 
    secs: 497
    nsecs: 122000000
  frame_id: ''
goal_id: 
  stamp: 
    secs: 497
    nsecs: 122000000
  id: /explore_client-4-497.122000000
goal: 
  explore_boundary: 
    header: 
      seq: 19
      stamp: 
        secs: 494
        nsecs: 848000000
      frame_id: map
    polygon: 
      points: 
        - 
          x: 6.41105794907
          y: 1.7436195612
          z: -0.00143432617188
        - 
          x: 3.28504276276
          y: 1.68363153934
          z: 0.294555664062
        - 
          x: 3.02357244492
          y: -0.934897124767
          z: 0.00247192382812
        - 
          x: 4.4475235939
          y: -1.05219256878
          z: 0.00247192382812
        - 
          x: 6.37510871887
          y: -0.795688152313
          z: 0.00247192382812
  explore_center: 
    header: 
      seq: 25
      stamp: 
        secs: 496
        nsecs: 950000000
      frame_id: map
    point: 
      x: 4.7991604805
      y: 0.374941498041
      z: 0.00247192382812
'''