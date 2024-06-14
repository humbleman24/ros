import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.actions import IncludeLaunchDescription
from launch.conditions import IfCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution

from launch_ros.actions import Node


def generate_launch_description():

    pkg_project_bringup = get_package_share_directory('asm_bringup')
    pkg_project_gazebo = get_package_share_directory('asm_gazebo')
    pkg_project_description = get_package_share_directory('asm_description')
    pkg_ros_gz_sim = get_package_share_directory('ros_gz_sim')


    # Load the SDF file from "description" package
    sdf_file  =  os.path.join(pkg_project_description, 'models', 'vehicle_blue.sdf')
    with open(sdf_file, 'r') as info:
        robot_desc = info.read()

    # Setup to launch the simulator and Gazebo world
    gz_sim = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_ros_gz_sim, 'launch', 'gz_sim.launch.py')),
        launch_arguments={'gz_args': PathJoinSubstitution([
            pkg_project_gazebo,
            'world',
            'sensor.sdf'
        ])}.items(),
    )

    # Takes the description and joint angles as inputs and publishes the 3D poses of the robot links
    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='both',
        parameters=[
            {'use_sim_time': True},
            {'robot_description': robot_desc},
        ]
    )



    # Visualize in RViz
#    rviz = Node(
#       package='rviz2',
#       executable='rviz2',
#       name='rviz2',
#       output='screen'
#    )

    # Bridge ROS topics and Gazebo messages for establishing communication
    bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        parameters=[{
            'config_file': os.path.join(pkg_project_bringup, 'config', 'asm_bridge.yaml'),
            'qos_overrides./tf_static.publisher.durability': 'transient_local',
        }],
        output='screen'
    )
    
    # slam launch
    # use_sim_time = LaunchConfiguration('use_sim_time', default='true')
    resolution = LaunchConfiguration('resolution', default='0.05')

    publish_period_sec = LaunchConfiguration('publish_period_sec', default='1.0')

    configuration_directory = LaunchConfiguration('configuration_directory',default= os.path.join(pkg_project_bringup, 'config') )

    configuration_basename = LaunchConfiguration('configuration_basename', default='slam_map_1.lua')
    
    rviz_config_dir = os.path.join(pkg_project_bringup, 'config')+"/cartographer_1.rviz"
    
    cartographer_node = Node(
        package='cartographer_ros',
        executable='cartographer_node',
        name='cartographer_node',
        output='screen',
        parameters=[{'use_sim_time': True}],
        arguments=['-configuration_directory', configuration_directory,
                   '-configuration_basename', configuration_basename])

    cartographer_occupancy_grid_node = Node(
        package='cartographer_ros',
        executable='cartographer_occupancy_grid_node',
        name='cartographer_occupancy_grid_node',
        output='screen',
        parameters=[{'use_sim_time': True}],
        arguments=['-resolution', resolution, '-publish_period_sec', publish_period_sec])

    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        arguments=['-d', rviz_config_dir],
        parameters=[{'use_sim_time': True}],
        output='screen')
    

    # sensor react
    react = Node(
            package='asm_node',
            executable='react',
            name='sensor_react'
        )
    
    
    
    
    

    return LaunchDescription([
        gz_sim,
        robot_state_publisher,
        bridge,
        cartographer_node,
        cartographer_occupancy_grid_node,
        rviz_node,
        react
    ])
