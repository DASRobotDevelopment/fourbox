import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.conditions import IfCondition 
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration, FindExecutable, Command, PathJoinSubstitution

def generate_launch_description():
    
    # Аргументы запуска
    use_rviz = LaunchConfiguration('rviz', default='true')

    rviz_arg_declare = DeclareLaunchArgument(
        'rviz',
        default_value='true',
        description='Start RViz'
    )

    # Пути к пакетам
    fourbox_description_pkg_path = get_package_share_directory('fourbox_description')
    
    # Конфиги
    rviz_config_file = os.path.join(fourbox_description_pkg_path, 'config', 'fourbox_description_config.rviz')
    
    # Контент
    robot_description_content = Command([
        PathJoinSubstitution([FindExecutable(name="xacro")]),
        ' ',
        PathJoinSubstitution([fourbox_description_pkg_path, 'description', 'fourbox.urdf.xacro'])
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

    joint_state_publisher_node = Node(
        package='joint_state_publisher_gui',
        executable='joint_state_publisher_gui',
        name='joint_state_publisher_gui',
        output='screen'
    )

    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        arguments=['-d', rviz_config_file],
        output='screen',
        condition=IfCondition(use_rviz),
        parameters=[robot_description]
    )
    
    # Запуск
    ld = LaunchDescription()

    ld.add_action(rviz_arg_declare)
    ld.add_action(robot_state_publisher_node)
    ld.add_action(joint_state_publisher_node)
    ld.add_action(rviz_node)

    return ld