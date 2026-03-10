#!/usr/bin/env python3
import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.conditions import IfCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch.substitutions import Command
from launch_ros.substitutions import FindPackageShare
from launch.actions import TimerAction

def generate_launch_description():
    # Аргументы запуска
    use_rviz = LaunchConfiguration('rviz', default='false')
    use_sim_time = LaunchConfiguration('use_sim_time', default='true')
    cmd_topic = LaunchConfiguration('cmd_topic', default='/cmd_vel')

    # Объявление аргументов запуска
    #DeclareLaunchArgument('rviz', default_value='false', description='Launch RViz2')
    declare_use_sim_time = DeclareLaunchArgument('use_sim_time', default_value='true')
    #DeclareLaunchArgument('cmd_topic', default_value='/cmd_vel')

    
    bringup_pkg_name = 'fourbox_bringup'
    simulation_pkg_path = FindPackageShare(bringup_pkg_name)
    
    # map_path = PathJoinSubstitution([simulation_pkg_path, 'maps', 'my_room.yaml'])
    slam_params_path = PathJoinSubstitution([simulation_pkg_path, 'config', 'mapper_params_online_async.yaml'])
    twist_mux_params_path = PathJoinSubstitution([simulation_pkg_path, 'config', 'twist_mux_params.yaml'])
    #rviz_file_path = PathJoinSubstitution([simulation_pkg_path, 'config', 'rviz_navigation_config.rviz'])
    
    # Launch файлы
    slam_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            PathJoinSubstitution([
                FindPackageShare('slam_toolbox'), 'launch', 'online_async_launch.py'
            ])
        ]),
        launch_arguments={
            'params_file': slam_params_path,
            'use_sim_time': use_sim_time
        }.items()
    )

    nav2_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            PathJoinSubstitution([
                FindPackageShare('nav2_bringup'), 'launch', 'navigation_launch.py'
            ])
        ]),
        launch_arguments={

            'use_sim_time': use_sim_time,
            'autostart': 'true',                 # ✅ Автозапуск!

        }.items(),
    )
    
    # Ноды
    # rviz2_node = Node(
    #     package='rviz2',
    #     executable='rviz2',
    #     name='rviz2',
    #     arguments=['-d', rviz_file_path],
    #     parameters=[{'use_sim_time': use_sim_time}],
    #     output='screen'
    # )
    
    twist_mux_node = Node(
        package='twist_mux',
        executable='twist_mux',
        name='twist_mux',
        output='screen',
        parameters=[twist_mux_params_path],
        remappings=[('/cmd_vel_out', cmd_topic)]
    )
    
    ld = LaunchDescription()
    
    ld.add_action(declare_use_sim_time)
    #ld.add_action(rviz2_node)
    ld.add_action(TimerAction(period=2.0, actions=[slam_launch]))      # SLAM через 2 сек
    ld.add_action(TimerAction(period=5.0, actions=[nav2_launch]))      # Nav2 через 5 сек  
    ld.add_action(TimerAction(period=3.0, actions=[twist_mux_node]))   # TwistMux через 3 сек
    
    return ld