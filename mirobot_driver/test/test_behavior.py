import math
from unittest.mock import Mock, patch

import rclpy
from sensor_msgs.msg import JointState
from mirobot_driver.serial_bridge import SerialBridge


def test_dry_run_and_joint_units():
    rclpy.init(args=['--ros-args', '-p', 'dry_run:=true'])
    with patch('mirobot_driver.serial_bridge.serial.Serial', side_effect=AssertionError('device access')) as device:
        node = SerialBridge()
        try:
            assert node.ser is None
            assert not node._reader_thread.is_alive()
            device.assert_not_called()
            # Capture formatting only; never transmit to a serial device.
            node._send_line = Mock()
            node.on_target_joints(JointState(name=list(reversed(node.joint_names)),
                                            position=[0.0, 0.0, 0.0, 0.0, 0.0, math.pi / 2]))
            assert node._send_line.call_args.args[0] == 'M21 G90 X90.00 Y0.00 Z0.00 A0.00 B0.00 C0.00 F2000'
            node._send_line.reset_mock()
            node.on_target_joints(JointState(name=['missing'] * 6, position=[0.0] * 6))
            node._send_line.assert_not_called()
        finally:
            node.destroy_node()
            rclpy.shutdown()
