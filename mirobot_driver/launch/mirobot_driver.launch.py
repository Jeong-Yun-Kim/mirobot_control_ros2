from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
from launch_ros.parameter_descriptions import ParameterValue


def generate_launch_description():
    return LaunchDescription([
        DeclareLaunchArgument('params', default_value=PathJoinSubstitution([
            FindPackageShare('mirobot_driver'), 'config', 'driver.yaml'])),
        DeclareLaunchArgument('port', default_value='/dev/ttyUSB0'),
        DeclareLaunchArgument('baud', default_value='115200'),
        DeclareLaunchArgument('dry_run', default_value='false'),
        Node(package='mirobot_driver', executable='serial_bridge', output='screen',
             parameters=[LaunchConfiguration('params'), {
                 'port': LaunchConfiguration('port'),
                 'baud': ParameterValue(LaunchConfiguration('baud'), value_type=int),
                 'dry_run': ParameterValue(LaunchConfiguration('dry_run'), value_type=bool)}]),
    ])
