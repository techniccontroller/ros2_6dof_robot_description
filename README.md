# ROS 2 six-DOF robot description

ROS 2 Humble description package for the six-axis arm. The model uses simple
URDF primitives and the approximate dimensions, inertias, limits, and frame
assumptions documented at the top of `urdf/6dof-robot.urdf`.

## Build and display

```bash
cd ~/ros2_ws
rosdep install --from-paths src --ignore-src -r -y
colcon build --packages-select ros2_6dof_robot_description
source install/setup.bash
ros2 launch ros2_6dof_robot_description display.launch.py
```

The display launch starts `robot_state_publisher`, RViz, and the graphical
joint sliders. For a system without a desktop, use `use_gui:=false`. When the
Pico driver is publishing `/joint_states`, disable both demo publishers:

```bash
ros2 launch ros2_6dof_robot_description display.launch.py \
  use_joint_state_publisher:=false
```

The driver and URDF both use `joint_1` through `joint_6`. The parallel-jaw
gripper is controlled by `gripper_joint`: 0 to 180 degrees maps linearly to a
0 to 40 mm jaw opening. The root frame is `base_link`; `tcp_link` is centred
between the fingers, 15 mm inward from their tips. RViz shows the TF frames by
default.

## Model status

This model is appropriate for visualization and initial kinematic work. The
link shapes, inertial properties, joint limits, and idealized spherical wrist
must be checked against the physical robot before dynamics, collision-sensitive
planning, or real-world operation.
