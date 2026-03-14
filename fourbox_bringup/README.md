ros2 run teleop_twist_keyboard teleop_twist_keyboard cmd --ros-args --remap cmd_vel:=/fourbox_controller/reference --ros-args -p stamped:=true
ros2 run teleop_twist_keyboard teleop_twist_keyboard cmd --ros-args -p stamped:=true

Сохранение карты:
ros2 run nav2_map_server map_saver_cli -f ~/ros2_ws/src/fourbox_hardware/maps/my_map
