import os
from launch import LaunchDescription
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
from launch.substitutions import PathJoinSubstitution, Command, FindExecutable
from launch.actions import RegisterEventHandler
from launch.event_handlers import OnProcessStart
from ament_index_python.packages import get_package_share_directory 
from launch.actions import IncludeLaunchDescription 
from launch.launch_description_sources import PythonLaunchDescriptionSource

def generate_launch_description():

    # Параметры робота
    serial_command_topic = '/serial_command'
    serial_response_topic = '/serial_response'
    serial_port_id = '/dev/ttyUSB0'
    serial_port_baudrate = '115200'
    serial_port_polling_hz = '50'

    wheel_base_x = '0.3'
    wheel_base_y = '0.2'
    max_wheel_rpm = '200'
    ticks_per_rev = '988'
    wheel_radius = '0.0325'
    cmd_vel_topic = '/cmd_vel'

    odom_topic_id = '/odom'
    odom_frame_name = 'odom'
    base_frame_name = 'base_footprint'
    rotation_scale = '0.45'

    lidar_port = '/dev/ttyUSB1'
    
    # Пути к пакетам
    bringup_pkg_path = FindPackageShare('fourbox_bringup')
    description_pkg_path = FindPackageShare('fourbox_description')
    
    # Пути к функциональным частям
    description_content_path = PathJoinSubstitution([
        description_pkg_path, 'description', 'fourbox.urdf.xacro'
    ])
    controllers_configuration_path = PathJoinSubstitution([
        bringup_pkg_path, 'config', 'fourbox_controllers.yaml'
    ])

    # Контент
    robot_description_content = Command([
        FindExecutable(name='xacro'), 
        ' ',
        description_content_path,
        ' ',
        'encoder_ppr_arg:=', ticks_per_rev,
        ' ',
        'baudrate_arg:=', serial_port_baudrate,
        ' ',
        'serial_port_name_arg:=', serial_port_id
    ])
    
    robot_description = {'robot_description': robot_description_content}
    
    # Ноды


    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='screen',
        parameters=[robot_description]
    )

    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        output='screen',
        # arguments=['-d', rviz_config],
        # condition=IfCondition(use_rviz)
    )

    rplidar_node = Node(
        package='rplidar_ros',
        executable='rplidar_composition',
        name='rplidar_node',
        output='screen',
        parameters=[{
            'serial_port': lidar_port,
            'serial_baudrate': 115200,
            'frame_id': 'laser_frame',
            'inverted': False,
            'angle_compensate': True,
            'scan_mode': 'Standard'
        }],
        remappings=[
            ('scan', '/scan')
        ]
    )

    # Файлы запуска

    dasrobot_base_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            get_package_share_directory('dasrobot_base_controller'),
            '/launch/dasrobot_base_controller.launch.py'
        ]),
        launch_arguments={
            'serial_command_topic': serial_command_topic,
            'serial_response_topic': serial_response_topic,
            'serial_port_id': serial_port_id,
            'serial_port_baudrate': serial_port_baudrate,
            'serial_port_polling_hz': serial_port_polling_hz,

            'wheel_base_x': wheel_base_x,
            'wheel_base_y': wheel_base_y,
            'max_wheel_rpm': max_wheel_rpm,
            'ticks_per_rev': ticks_per_rev,
            'wheel_radius': wheel_radius,
            'cmd_vel_topic': cmd_vel_topic,

            'odom_topic_id': odom_topic_id,
            'odom_frame_name': odom_frame_name,
            'base_frame_name': base_frame_name,
            'rotation_scale': rotation_scale
        }.items()
    )

    ld = LaunchDescription()

    ld.add_action(robot_state_publisher_node)
    ld.add_action(dasrobot_base_launch)
    # ld.add_action(rviz_node)
    ld.add_action(rplidar_node)

    return ld