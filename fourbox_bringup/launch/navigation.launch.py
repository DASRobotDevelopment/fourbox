#!/usr/bin/env python3
import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.conditions import IfCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
from launch.actions import TimerAction
from launch_ros.parameter_descriptions import ParameterFile


def generate_launch_description():
    # Аргументы запуска
    use_rviz = LaunchConfiguration('rviz', default='false')
    use_sim_time = LaunchConfiguration('use_sim_time', default='false')
    cmd_topic = LaunchConfiguration('cmd_topic', default='/cmd_vel')
    
    # Объявления
    declare_use_sim_time = DeclareLaunchArgument('use_sim_time', default_value='false')
    declare_rviz = DeclareLaunchArgument('rviz', default_value='false')
    declare_cmd_topic = DeclareLaunchArgument('cmd_topic', default_value='/cmd_vel')
    
    bringup_pkg_name = 'fourbox_bringup'
    simulation_pkg_path = FindPackageShare(bringup_pkg_name)
    
    # ✅ Пути к параметрам
    slam_params_path = PathJoinSubstitution([simulation_pkg_path, 'config', 'mapper_params_online_async.yaml'])
    nav2_params_path = PathJoinSubstitution([simulation_pkg_path, 'config', 'nav2_params.yaml'])
    twist_mux_params_path = PathJoinSubstitution([simulation_pkg_path, 'config', 'twist_mux_params.yaml'])
    
    # SLAM
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
    
    # ✅ Nav2 — все ПРЯМЫЕ НОДЫ
    map_server = Node(
        package='nav2_map_server',
        executable='map_server',
        name='map_server',
        output='screen',
        parameters=[nav2_params_path]
    )
    
    controller_server = Node(
        package='nav2_controller',
        executable='controller_server',
        name='controller_server',
        output='screen',
        parameters=[nav2_params_path],
        remappings=[
            ('/tf', 'tf'),
            ('/tf_static', 'tf_static'),
            ('cmd_vel', '/cmd_vel_nav')
        ]
    )
    
    planner_server = Node(
        package='nav2_planner', 
        executable='planner_server',
        name='planner_server',
        output='screen',
        parameters=[nav2_params_path]
    )
    
    bt_navigator = Node(
        package='nav2_bt_navigator',
        executable='bt_navigator',
        name='bt_navigator',
        output='screen',
        parameters=[nav2_params_path]
    )
    
    lifecycle_manager = Node(
        package='nav2_lifecycle_manager',
        executable='lifecycle_manager',
        name='lifecycle_manager_navigation',
        output='screen',
        parameters=[{
            'use_sim_time': use_sim_time,
            'autostart': True,
            'node_names': [
                'map_server',
                'controller_server', 
                'planner_server',
                "behavior_server",     # ✅ ДОБАВЬ!
                'bt_navigator'
            ]
        }]
    )

    behavior_server = Node(
        package='nav2_behaviors',
        executable='behavior_server',
        name='behavior_server',
        output='screen',
        parameters=[nav2_params_path]
    )
    
    fourbox_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            PathJoinSubstitution([
                FindPackageShare('fourbox_bringup'), 'launch', 'fourbox.launch.py'
            ])
        ])
    )
    
    # TwistMux
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
    ld.add_action(declare_rviz)
    ld.add_action(declare_cmd_topic)
    
    ld.add_action(fourbox_launch)
    
    # ✅ ПОЛНАЯ последовательность запуска
    ld.add_action(TimerAction(period=2.0, actions=[slam_launch]))           # 1. SLAM
    ld.add_action(TimerAction(period=5.0, actions=[twist_mux_node]))        # 2. TwistMux
    ld.add_action(TimerAction(period=6.0, actions=[map_server]))            # 3. Map Server ✅
    ld.add_action(TimerAction(period=7.0, actions=[controller_server]))     # 4. Controller
    ld.add_action(TimerAction(period=8.0, actions=[planner_server]))        # 5. Planner
    ld.add_action(TimerAction(period=9.5, actions=[behavior_server]))  # Behavior 
    ld.add_action(TimerAction(period=9.0, actions=[bt_navigator]))          # 6. BT Navigator
    ld.add_action(TimerAction(period=10.0, actions=[lifecycle_manager]))    # 7. Lifecycle Manager

    
    return ld
