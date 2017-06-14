# hideseek-turtlebot

###  Installing Project & Dependencies

On the Turtlebot 2, install the sound_play package:

	sudo apt-get install ros-indigo-sound-play
 
On the workstation computer, checkout and build [cmvision](https://github.com/kbogert/cmvision/tree/indigo-devel), [cmvision_3d](http://wiki.ros.org/cmvision_3d), and hideseek_turtlebot by following [these instructions](http://answers.ros.org/question/252478/how-to-build-a-package-from-source-on-ubuntu-mate-1604-lts-and-ros-kinetic/). Make sure to switch to the indigo-devel branch before building cmvision. If you get a build error related to WxWidgets when you do catkin_make, you should do this:

  `sudo apt-get install libwxgtk2.8-dev libwxgtk2.8-dbg python-wxtools python-wxgtk2.8-dbg`
 
### Setting Up the Playing Area

Generate a map of the selected playing area using any appropriate method, and update the .yaml file to set the map origin and scale to reasonable values. Select a few initial hiding places for the robot to choose from by estimating pose coordinates on this map, as well as a “home” position. Update this file with the selected pose coordinates:

	$(rospack find hideseek_turtlebot)/maps/hiding_places.xml
 
### Player Color Calibration 

The human player should wear a bright solid-colored shirt of a color that does not occur frequently (preferably at all) in the mapped playing area. On the Turtlebot 2, start any node that will launch depth sensing and color camera topics from the Kinect. For instance:

	roslaunch turtlebot_bringup 3dsensor.launch
 
On the workstation, run the following command to launch a GUI for color selection:

  `rosrun cmvision colorgui image:=/camera/rgb/image_color`
 
Put both players in the mapped playing area and make sure that the human player is standing in view of the Kinect. Click in the GUI to select a few samples of the human’s shirt color, and save the corresponding RGB and Threshold values. Repeat this in several different lighting conditions around the mapped playing area. Edit this text file to include all of the sampled colors by following [this example](http://wiki.ros.org/cmvision).

  `$(rospack find cmvision_3d)/colors/example.txt`
 
### Running Hide & Seek Game

Copy the hideseek_turtlebot package directory to the Turtlebot 2 catkin workspace and source the package. Then run the following command to start amcl, 3D sensor data from Kinect, and the sound_play node:

  `roslaunch hideseek_turtlebot hideseek_turtlebot.launch`
 
On the workstation, source the package and use a different launch file to start up gameplay, cmvision, and rviz:

  `roslaunch hideseek_turtlebot hideseek_workstations.launch`
 
The hideseek_smach.py node will launch in its own terminal to output smach log messages and serve as the player interface. Follow the robot prompts and enter appropriate text strings to indicate whether the robot should hide or seek, and when the game should end. The Turtlebot 2 will perform better if you give it a 2D Pose Estimate and/or short navigation goal in rviz prior to sending the robot to hide or seek.
 
