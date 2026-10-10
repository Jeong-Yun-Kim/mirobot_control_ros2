from pathlib import Path
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue


def generate_launch_description():
    desc = Path(get_package_share_directory('mirobot_description'))
    driver = Path(get_package_share_directory('mirobot_driver'))
    description = ParameterValue((desc / 'urdf/mirobot_urdf_2.urdf').read_text(), value_type=str)
    nodes = [
        IncludeLaunchDescription(PythonLaunchDescriptionSource(str(driver / 'launch/mirobot_driver.launch.py'))),
        Node(package='robot_state_publisher', executable='robot_state_publisher',
             parameters=[{'robot_description': description}], remappings=[('joint_states', 'target_joint_states')]),
        Node(package='rviz2', executable='rviz2', arguments=['-d', str(desc / 'rviz/description.rviz')]),
    ]
    nodes.append(Node(package='joint_state_publisher_gui', executable='joint_state_publisher_gui',
                      parameters=[{'robot_description': description}], remappings=[('joint_states', 'target_joint_states')]))
    return LaunchDescription(nodes)
