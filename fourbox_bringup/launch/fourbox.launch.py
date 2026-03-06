import os
from launch import LaunchDescription
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
from launch.substitutions import PathJoinSubstitution, Command, FindExecutable
from launch.actions import RegisterEventHandler
from launch.event_handlers import OnProcessStart

def generate_launch_description():
    # Аргументы запуска
    
    # Параметры робота
    encoder_ppr = "990"
    baudrate = "115200"
    serial_port_name = "/dev/ttyUSB0"
    
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
        'encoder_ppr_arg:=', encoder_ppr,
        ' ',
        'baudrate_arg:=', baudrate,
        ' ',
        'serial_port_name_arg:=', serial_port_name
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

    
    # Controller Manager
    # controller_manager = Node(
    #     package='controller_manager',
    #     executable='ros2_control_node',
    #     parameters=[{'robot_description': robot_description_content},
    #                 robot_controllers_path],
    #     output='screen'
    # )

    controller_manager = Node(
        package='controller_manager',
        executable='ros2_control_node',
        parameters=[robot_description, controllers_configuration_path],
        output='screen'
    )
    
    # Спавнеры с ПРАВИЛЬНЫМИ аргументами
    joint_state_broadcaster_spawner = Node(
        package='controller_manager',
        executable='spawner',
        arguments=['joint_state_broadcaster', '--controller-manager', '/controller_manager'],
        output='screen',
    )
    
    # fourbox_controller_spawner = Node(
    #     package='controller_manager',
    #     executable='spawner', 
    #     arguments=['fourbox_controller', '--controller-manager', '/controller_manager'],
    #     output='screen',
    # )

    fourbox_controller_spawner = Node(
        package='controller_manager',
        executable='spawner', 
        arguments=[
            'fourbox_controller', 
            '--controller-manager', 
            '/controller_manager',
            #'--controller-ros-args','-r /fourbox_controller/odometry:=/odometry',
            '--controller-ros-args','-r /fourbox_controller/tf_odometry:=/tf',
            '--controller-ros-args','-r /fourbox_controller/reference:=/cmd_vel',

            ],
        output='screen',
    )
    
    
    # Последовательный запуск
    joint_state_broadcaster_event = RegisterEventHandler(
        OnProcessStart(
            target_action=controller_manager,
            on_start=[joint_state_broadcaster_spawner]
        )
    )
    
    mecanum_controller_event = RegisterEventHandler(
        OnProcessStart(
            target_action=joint_state_broadcaster_spawner,
            on_start=[fourbox_controller_spawner]
        )
    )
    
    return LaunchDescription([
        robot_state_publisher_node,
        controller_manager,
        joint_state_broadcaster_event,
        mecanum_controller_event,
    ])
