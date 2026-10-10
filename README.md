# mirobot_control_ros2

## 간단한 소개

미로봇 한 대의 로봇 모델 표시와 관절·XYZ 명령 및 시리얼 통신을 구성한다.
하드웨어 없는 모델 표시와 실제 드라이버 실행을 구분한다.

## 권장 실행 환경

Ubuntu 22.04, ROS2 Humble, Python 3.10을 권장한다.
실제 제어에는 USB 시리얼로 연결한 미로봇 한 대가 필요하며, RViz에는 그래픽 세션을 사용한다.
같은 OS·ROS2·Python에서 장비 없이 빌드와 제한된 실행 검증을 수행했으며 실물 동작은 미검증 상태이다.

## 패키지 구조

| 경로 | 역할 |
| --- | --- |
| `mirobot_description` | URDF/Xacro, 메시, RViz와 C++ 시리얼 실행 파일을 제공한다. |
| `mirobot_driver` | Python 시리얼 브리지와 관절·XYZ CLI를 제공한다. |
| `mirobot_driver/config/driver.yaml` | 포트, baudrate, 작업 범위와 상태 조회 주기를 지정한다. |
| `dependencies.repos` | C++ 빌드에 필요한 `serial` 소스의 커밋을 고정한다. |

## 빌드 및 실행 방법

ROS2 Humble이 설치된 새 터미널에서 다음 순서로 구성한다.

```bash
source /opt/ros/humble/setup.bash
sudo apt install python3-colcon-common-extensions python3-rosdep python3-vcstool python3-venv
mkdir -p ~/mirobot_control_ws/src
cd ~/mirobot_control_ws
git clone https://github.com/Jeong-Yun-Kim/mirobot_control_ros2.git src/mirobot_control_ros2
vcs import src < src/mirobot_control_ros2/dependencies.repos
rosdep update
rosdep install --from-paths src --ignore-src -r -y --rosdistro humble
colcon build
source install/setup.bash
```

`rosdep`을 처음 사용하는 시스템은 `sudo rosdep init`을 먼저 실행한다.

장치 없이 모델을 표시하며, 화면 없는 환경에서는 두 번째 명령을 사용한다.

```bash
ros2 launch mirobot_description mirobot_description.launch.py
ros2 launch mirobot_description mirobot_description.launch.py gui:=false rviz:=false
```

장치 없는 드라이버 검사는 다음 명령으로 시리얼 열기를 차단하며, 동작 완료나 로봇 피드백을 모사하지 않는다.

```bash
ros2 launch mirobot_driver mirobot_driver.launch.py dry_run:=true
```

실제 장비는 포트와 `driver.yaml`의 작업 범위를 확인한 뒤 연결하며, 드라이버 시작 시 초기화 명령을 전송한다.

```bash
ros2 launch mirobot_driver mirobot_driver.launch.py port:=/dev/ttyUSB0 baud:=115200
```

다른 터미널에서 같은 환경을 source한 뒤 다음 CLI 중 하나를 실행한다.
관절 메시지는 rad, XYZ는 mm를 사용하며 관절 CLI의 degree 입력은 rad로 변환한다.

```bash
source /opt/ros/humble/setup.bash
source ~/mirobot_control_ws/install/setup.bash
ros2 run mirobot_driver send_joint_target
# XYZ 입력 모드
ros2 run mirobot_driver mirobot_xyz
```

RViz와 드라이버를 함께 사용할 때는 `ros2 launch mirobot_driver mirobot_full_control.launch.py`를 실행하며, 이 화면은 측정 위치가 아닌 관절 명령을 표시한다.
한 포트에는 하나의 제어 프로그램만 연결한다.
`mirobot_gcode_writer`와 `mirobot_gcode_writer_isaac`는 빌드·설치되지만 실행 시 자동 원점복귀를 수행하므로 이번 장비 없는 검증에서 실행하지 않는다.
Isaac USD·RMPflow 자료는 보존 자료이며, Isaac 환경과 토픽·장비를 별도로 준비해야 하고 연동은 미검증 상태이다.

## 참고 목록

- [Jeong-Yun-Kim/Mirobot_ros2](https://github.com/Jeong-Yun-Kim/Mirobot_ros2)의 소스를 분리하여 사용한다.
- [RoverRobotics-forks/serial-ros2](https://github.com/RoverRobotics-forks/serial-ros2)를 기존 C++ 시리얼 코드의 빌드 의존성으로 사용한다.
- 기존 파일의 저작권과 라이선스 선언을 보존하며, 상충하거나 미정인 선언은 새 라이선스로 확정하지 않는다.
