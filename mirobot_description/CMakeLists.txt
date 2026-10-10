cmake_minimum_required(VERSION 3.8)
project(mirobot_description)

find_package(ament_cmake REQUIRED)
find_package(xacro REQUIRED)  # xacro 사용 시

install(
  DIRECTORY
    config
    launch
    meshes
    rviz
    urdf
  DESTINATION share/${PROJECT_NAME}/
)

find_package(rclcpp REQUIRED)
find_package(sensor_msgs REQUIRED)
find_package(std_msgs REQUIRED)
find_package(serial REQUIRED)
foreach(executable mirobot_gcode_writer mirobot_gcode_writer_isaac)
  add_executable(${executable} src/${executable}.cpp)
  target_compile_features(${executable} PUBLIC cxx_std_14)
  ament_target_dependencies(${executable} rclcpp sensor_msgs std_msgs serial)
  install(TARGETS ${executable} DESTINATION lib/${PROJECT_NAME})
endforeach()
ament_package()
