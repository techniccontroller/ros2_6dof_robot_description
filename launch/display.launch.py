# Copyright 2026 Edgar Welte
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0

"""Display the robot model with optional demo joint controls and RViz."""

from pathlib import Path

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.conditions import IfCondition
from launch.substitutions import LaunchConfiguration, PythonExpression
from launch_ros.actions import Node


def generate_launch_description():
    """Create the model visualization launch description."""
    package_share = Path(
        get_package_share_directory("ros2_6dof_robot_description")
    )
    robot_description = (package_share / "urdf" / "6dof-robot.urdf").read_text(
        encoding="utf-8"
    )

    use_gui = LaunchConfiguration("use_gui")
    use_joint_state_publisher = LaunchConfiguration("use_joint_state_publisher")
    use_rviz = LaunchConfiguration("use_rviz")

    gui_condition = IfCondition(
        PythonExpression(
            [
                "'",
                use_joint_state_publisher,
                "' == 'true' and '",
                use_gui,
                "' == 'true'",
            ]
        )
    )
    non_gui_condition = IfCondition(
        PythonExpression(
            [
                "'",
                use_joint_state_publisher,
                "' == 'true' and '",
                use_gui,
                "' != 'true'",
            ]
        )
    )

    return LaunchDescription(
        [
            DeclareLaunchArgument(
                "use_gui",
                default_value="true",
                description="Use sliders to publish demo joint states.",
            ),
            DeclareLaunchArgument(
                "use_joint_state_publisher",
                default_value="true",
                description=(
                    "Start a joint-state publisher. Set false when the robot "
                    "driver already publishes joint_states."
                ),
            ),
            DeclareLaunchArgument(
                "use_rviz",
                default_value="true",
                description="Start RViz with the package configuration.",
            ),
            Node(
                package="robot_state_publisher",
                executable="robot_state_publisher",
                name="robot_state_publisher",
                output="screen",
                parameters=[{"robot_description": robot_description}],
            ),
            Node(
                package="joint_state_publisher_gui",
                executable="joint_state_publisher_gui",
                name="joint_state_publisher_gui",
                condition=gui_condition,
            ),
            Node(
                package="joint_state_publisher",
                executable="joint_state_publisher",
                name="joint_state_publisher",
                condition=non_gui_condition,
            ),
            Node(
                package="rviz2",
                executable="rviz2",
                name="rviz2",
                output="screen",
                arguments=["-d", str(package_share / "rviz" / "display.rviz")],
                condition=IfCondition(use_rviz),
            ),
        ]
    )
