This is the porject for ROS2 and Gazebo simulation


Structure:
src: 
 - asm_node
   -- asm_node
     -- sensor_react.py: enable autonomous operation of the vehicle and sensor-based behavious
   -- asm_bringup
     -- launch: the launch file responsible for launching the Gazebo and Rviz and required ROS2 nodes
     -- config: yaml for the ros-gz-bridge connection; lua for cartographer configuration; rviz for Rviz2 configuration
   -- asm_description
     -- models: include the vehicle (robot) description, called by the asm_gazebo/world to spawn the robot in the world
   -- asm_gazebo:
     -- world: contain the description of the world and used by Gazebo simulation
     
     
     
Score Point: 30 + 30 + 30 + 10 + 20
 simulation software usage: use the Gazebo and rviz
 autonomous operation: the robot can move in the simulation environment without human inference
 sensor-based behaviour: robot is programmed to avoid crashing into world by utilize lidar sensor information.
 custom node development: the above two funtionality are accomplished by custom python node coding.
 Map drawing: enable the robot to simultaneously localization and mapping (SLAM) by using the cartographer package provided by Google Cartgrapher. 
