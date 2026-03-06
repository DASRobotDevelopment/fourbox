ros2 run teleop_twist_keyboard teleop_twist_keyboard cmd --ros-args --remap cmd_vel:=/fourbox_controller/reference --ros-args -p stamped:=true
ros2 run teleop_twist_keyboard teleop_twist_keyboard cmd --ros-args -p stamped:=true
