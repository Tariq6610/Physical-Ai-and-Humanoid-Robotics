---
sidebar_position: 3
title: Appendix C - Common ROS 2 CLI Commands
---

# Appendix C: Common ROS 2 CLI Commands

This appendix provides a reference for commonly used ROS 2 command-line interface (CLI) commands.

## Environment Setup

### Source ROS 2 Environment
```bash
source /opt/ros/humble/setup.bash
```

### Create an alias for convenience
Add to your `~/.bashrc`:
```bash
alias ros2humble='source /opt/ros/humble/setup.bash'
```

## Package Management

### Create a new package
```bash
cd ~/ros2_ws/src
ros2 pkg create --build-type ament_python my_robot_package
# or for C++
ros2 pkg create --build-type ament_cmake my_robot_package
```

### Build packages
```bash
cd ~/ros2_ws
colcon build
# Source the workspace
source install/setup.bash
```

### List installed packages
```bash
ros2 pkg list
```

### Get information about a package
```bash
ros2 pkg xml <package_name>
```

## Node Management

### List active nodes
```bash
ros2 node list
```

### Get information about a node
```bash
ros2 node info <node_name>
```

## Topic Communication

### List active topics
```bash
ros2 topic list
```

### Get information about a topic
```bash
ros2 topic info /topic_name
```

### Echo messages from a topic
```bash
ros2 topic echo /topic_name MessageTypeName
# Example:
ros2 topic echo /cmd_vel geometry_msgs/msg/Twist
```

### Publish a message to a topic
```bash
ros2 topic pub /topic_name MessageType "{field1: value1, field2: value2}"
# Example:
ros2 topic pub /chatter std_msgs/String "data: 'Hello World'"
```

### Show topic publishing rate
```bash
ros2 topic hz /topic_name
```

### Show topic delay and bandwidth
```bash
ros2 topic delay /topic_name
ros2 topic bw /topic_name
```

## Service Communication

### List active services
```bash
ros2 service list
```

### Get information about a service
```bash
ros2 service info <service_name>
```

### Call a service
```bash
ros2 service call /service_name ServiceTypeName "{request_field: value}"
# Example:
ros2 service call /add_two_ints example_interfaces/srv/AddTwoInts "{a: 1, b: 2}"
```

## Action Communication

### List active actions
```bash
ros2 action list
```

### Get information about an action
```bash
ros2 action info /action_name
```

### Send a goal to an action
```bash
ros2 action send_goal /action_name ActionType "{goal_fields: values}"
# Example:
ros2 action send_goal /fibonacci action_tutorials_interfaces/action/Fibonacci "{order: 10}"
```

## Parameter Management

### List parameters of a node
```bash
ros2 param list <node_name>
```

### Get a parameter value
```bash
ros2 param get <node_name> <parameter_name>
# Example:
ros2 param get /talker use_sim_time
```

### Set a parameter value
```bash
ros2 param set <node_name> <parameter_name> <value>
# Example:
ros2 param set /talker qos_overrides./chatter.publisher.depth 20
```

### Dump all parameters to a file
```bash
ros2 param dump <node_name> --output params.yaml
```

## Launch Files

### Run a launch file
```bash
ros2 launch <package_name> <launch_file>.py
# Example:
ros2 launch turtlesim turtlesim_and_mimic_launch.py
```

## Lifecycle Nodes

### List lifecycle nodes
```bash
ros2 lifecycle list <node_name>
```

### Change lifecycle state
```bash
ros2 lifecycle set <node_name> <state>
# Example:
ros2 lifecycle set /lifecycle_talker configure
```

## Bag (Recording/Playback)

### Record topics to a bag file
```bash
ros2 bag record <topic_name1> <topic_name2> --output my_bag
# Record all topics:
ros2 bag record -a --output my_bag
```

### Play back a bag file
```bash
ros2 bag play my_bag
```

### Check bag info
```bash
ros2 bag info my_bag
```

## Quality of Service (QoS)

### Override QoS settings when running a node
```bash
ros2 run <package_name> <node_name> --ros-args --param qos_overrides./<topic_name>.<publisher|subscriber>.<depth|reliability|durability>:=<value>
```

## Common Message Types

### Standard Messages
- `std_msgs/msg/String` - Simple string message
- `std_msgs/msg/Int32` - 32-bit integer
- `std_msgs/msg/Float64` - 64-bit float
- `std_msgs/msg/Bool` - Boolean value

### Geometry Messages
- `geometry_msgs/msg/Twist` - Linear and angular velocity
- `geometry_msgs/msg/Pose` - Position and orientation
- `geometry_msgs/msg/Point` - 3D point
- `geometry_msgs/msg/Quaternion` - Rotation in quaternion form

### Sensor Messages
- `sensor_msgs/msg/JointState` - Joint positions, velocities, efforts
- `sensor_msgs/msg/LaserScan` - Laser range data
- `sensor_msgs/msg/Image` - Image data
- `sensor_msgs/msg/CameraInfo` - Camera calibration data

## Debugging and Monitoring

### Monitor system performance
```bash
# Show CPU and memory usage of ROS 2 processes
htop
# Monitor network traffic
iftop
```

### Check network connectivity
```bash
# Check if ROS 2 nodes can communicate
ros2 topic list
# Check DDS domain
echo $ROS_DOMAIN_ID
```

### Enable logging
```bash
# Set log level
export RCUTILS_LOGGING_SEVERITY_THRESHOLD=DEBUG
# Or set for a specific node
ros2 run <package> <node> --ros-args --log-level DEBUG
```

## Simulation Commands

### Launch Gazebo
```bash
# Launch empty world
ros2 launch gazebo_ros empty_world.launch.py
# Launch with GUI
ros2 launch gazebo_ros gazebo.launch.py
```

### Spawn models in Gazebo
```bash
ros2 run gazebo_ros spawn_entity.py -entity my_robot -file /path/to/model.sdf -x 0 -y 0 -z 1
```

## Useful Tools

### ROS 2 Doctor
```bash
# Check system configuration
ros2 doctor
# Run specific checks
ros2 doctor --report
```

### Run with custom DDS
```bash
# Use Fast DDS
RMW_IMPLEMENTATION=rmw_fastrtps_cpp ros2 run <package> <node>
# Use Cyclone DDS
RMW_IMPLEMENTATION=rmw_cyclonedx_cpp ros2 run <package> <node>
```

## Troubleshooting Commands

### Check if ROS 2 daemon is running
```bash
ps aux | grep ros
```

### Kill ROS 2 daemon if needed
```bash
pkill -f ros
```

### Check ROS 2 environment variables
```bash
printenv | grep ROS
```

### Reset ROS 2 environment
```bash
unset ROS_DOMAIN_ID
unset RMW_IMPLEMENTATION
```

## Workspace Management

### Create a new workspace
```bash
mkdir -p ~/ros2_ws/src
cd ~/ros2_ws
colcon build
source install/setup.bash
```

### Add workspace to bashrc
```bash
echo "source ~/ros2_ws/install/setup.bash" >> ~/.bashrc
```

This reference covers the most commonly used ROS 2 CLI commands. For more detailed information, refer to the official ROS 2 documentation or use the `--help` flag with any command.