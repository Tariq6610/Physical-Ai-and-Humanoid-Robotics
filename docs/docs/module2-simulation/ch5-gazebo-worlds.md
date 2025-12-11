---
sidebar_position: 1
title: Simulating Worlds with Gazebo
---

## Introduction

Having designed our robot's physical structure with URDF, we now bring it to life in a virtual environment. This chapter introduces the Gazebo simulator, a powerful 3D robotics simulator widely used in the ROS 2 ecosystem. We will learn how to create virtual worlds, import our URDF model, and interact with it under realistic physics, covering fundamental concepts like gravity, collisions, and friction.

## Lesson 5.1: Getting Started with Gazebo Simulator

Gazebo is a powerful 3D robotics simulator that accurately simulates populations of robots in complex indoor and outdoor environments. It offers robust physics engines (like ODE, Bullet, Simbody, and DART), high-quality graphics, and a convenient programmatic interface. Crucially, Gazebo is tightly integrated with ROS 2, making it the de facto standard for simulating ROS 2-powered robots.

### Installation

For ROS 2 Humble users, Gazebo Fortress (part of the Gazebo Garden ecosystem) is typically installed alongside ROS 2. If you don't have it, or if you're using a different ROS 2 distribution, you can install it via the official Gazebo documentation.

Assuming you have ROS 2 Humble installed, you can often launch Gazebo directly.

### Launching a Simple Gazebo World

Let's begin by launching a basic Gazebo empty world. Open your terminal and run:

```bash
gazebo
```

or, more commonly within a ROS 2 context:

```bash
ros2 launch gazebo_ros gazebo.launch.py
```

This command will typically open two windows:
1.  **Gazebo Server (gzserver)**: This is the backend process that handles physics, sensors, and simulation logic. You usually don't see a GUI for this.
2.  **Gazebo Client (gzclient)**: This is the graphical user interface (GUI) that allows you to visualize the world, interact with objects, and inspect robot properties.

If successful, you should see an empty 3D world with a grid plane and a light source.

### Exploring the Gazebo User Interface

The `gzclient` interface provides several tools for interacting with your simulation:

*   **Left Panel**:
    *   **World**: Lists all models and entities currently in your simulation (e.g., ground plane, light sources, any robots or objects you add).
    *   **Insert**: Provides a library of pre-defined models you can drag and drop into your world (e.g., simple shapes, common objects like tables, chairs, or even basic robots).
    *   **Layers**: Manages visibility of different layers in the simulation.
*   **Top Toolbar**:
    *   **Selection Tools**: Allows you to select, move, rotate, and scale objects in the world.
    *   **Object Insertion**: Quick buttons for inserting common shapes (box, sphere, cylinder).
    *   **Light Sources**: Tools to add and manipulate light sources.
    *   **Simulation Controls**: Play, pause, and reset the simulation (often depicted as VCR-like buttons).
*   **3D Viewport**: The main area where you visualize your simulation. You can typically navigate using your mouse:
    *   **Orbit**: Left-click and drag.
    *   **Pan**: Right-click and drag.
    *   **Zoom**: Scroll wheel.

### Spawning a Simple Model

Let's add a simple box to our world.
1.  Click the "Insert" tab in the left panel.
2.  Expand the "Models" section.
3.  Drag and drop a "Cube" into the 3D viewport.
4.  You can then use the selection tools (move, rotate) from the top toolbar to position it.
5.  Press the "Play" button (triangle icon) on the top toolbar to start the physics simulation. Observe how the cube falls onto the ground plane due to gravity.

### Summary

In this lesson, you've taken your first steps with the Gazebo simulator. You've learned how to launch a basic empty world, navigate its user interface, and spawn simple objects. This hands-on experience provides the foundation for creating more complex and realistic simulation environments for your robotic projects. In the next lessons, we'll explore how to build custom worlds and integrate your URDF robot models.

## Lesson 2.2: Creating Custom Gazebo Worlds and Importing URDF Models

While pre-built Gazebo worlds are useful for quick tests, real-world robotics often requires custom environments. Gazebo uses the **Simulation Description Format (SDF)** to define worlds, models, and other simulation elements. SDF is a comprehensive XML format that describes all aspects of a simulation, including physics properties, sensor definitions, and graphical elements.

### Understanding SDF for World Creation

An SDF world file typically contains:

*   **`<world>` tag**: The root element, containing all other elements of the simulation.
*   **`<light>` tag**: Defines light sources (e.g., directional, point, spot).
*   **`<model>` tag**: Used to include static or dynamic models (e.g., ground plane, walls, furniture, robots).
*   **`<physics>` tag**: Configures the physics engine parameters.

Let's create a simple custom world. Create a file named `my_custom_world.sdf` in a new directory `worlds/` within your project, for example, `~/my_robot_ws/src/my_robot_description/worlds/my_custom_world.sdf`.

```xml
<?xml version="1.0" ?>
<sdf version="1.7">
  <world name="my_empty_world">
    <gravity>0 0 -9.8</gravity>
    <magnetic_field>6e-06 2.3e-05 -4.2e-05</magnetic_field>
    <atmosphere type="adiabatic"/>

    <light name="sun" type="directional">
      <cast_shadows>1</cast_shadows>
      <pose>0 0 10 0 -0 0</pose>
      <diffuse>0.8 0.8 0.8 1</diffuse>
      <specular>0.2 0.2 0.2 1</specular>
      <attenuation>
        <range>1000</range>
        <constant>0.9</constant>
        <linear>0.01</linear>
        <quadratic>0.001</quadratic>
      </attenuation>
      <direction>-0.5 0.1 -0.9</direction>
      <spot>
        <inner_angle>0</inner_angle>
        <outer_angle>0</outer_angle>
        <falloff>0</falloff>
      </spot>
    </light>

    <model name="ground_plane">
      <static>true</static>
      <link name="link">
        <collision name="collision">
          <geometry>
            <plane>
              <normal>0 0 1</normal>
              <size>100 100</size>
            </plane>
          </geometry>
          <surface>
            <friction>
              <ode>
                <mu>1.0</mu>
                <mu2>1.0</mu2>
              </ode>
            </friction>
          </surface>
        </collision>
        <visual name="visual">
          <geometry>
            <plane>
              <normal>0 0 1</normal>
              <size>100 100</size>
            </plane>
          </geometry>
          <material>
            <ambient>0.8 0.8 0.8 1</ambient>
            <diffuse>0.8 0.8 0.8 1</diffuse>
            <specular>0.8 0.8 0.8 1</specular>
          </material>
        </visual>
      </link>
    </model>

  </world>
</sdf>
```

You can launch this world using:

```bash
gazebo -s libgazebo_ros_factory.so ~/my_robot_ws/src/my_robot_description/worlds/my_custom_world.sdf
```
*(Note: Adjust the path to your SDF file.)*

### Importing URDF Models into Gazebo

Our previously created URDF models (from Module 1) need to be imported into Gazebo. While URDF primarily defines the robot's kinematic and dynamic properties, Gazebo requires additional information, specifically related to physics (e.g., inertia, friction for individual links) and sensors. These are often added as `<gazebo>` extensions within the URDF file itself, or as a separate XACRO file.

To include a URDF model in an SDF world, you typically use a Gazebo launch file that spawns the URDF model. The `gazebo_ros` package provides tools for this.

A typical ROS 2 launch file to spawn a URDF model in Gazebo:

```python
import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource

def generate_launch_description():
    pkg_name = 'my_robot_description' # Replace with your robot's package name
    urdf_file = os.path.join(get_package_share_directory(pkg_name), 'urdf', 'my_robot.urdf') # Adjust path
    
    with open(urdf_file, 'r') as infp:
        robot_desc = infp.read()

    return LaunchDescription([
        # Launch Gazebo world
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource([os.path.join(
                get_package_share_directory('gazebo_ros'), 'launch', 'gazebo.launch.py')]),
            launch_arguments={'world': os.path.join(get_package_share_directory(pkg_name), 'worlds', 'my_custom_world.sdf')}.items(),
        ),

        # Spawn robot entity
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            name='robot_state_publisher',
            output='screen',
            parameters=[{'robot_description': robot_desc}],
        ),
        Node(
            package='gazebo_ros',
            executable='spawn_entity.py',
            arguments=['-topic', 'robot_description', '-entity', 'my_robot'],
            output='screen'
        )
    ])
```
This launch file:
1.  Launches your custom Gazebo world.
2.  Starts `robot_state_publisher` to publish the robot's TF (transformations) based on its URDF.
3.  Uses `spawn_entity.py` from `gazebo_ros` to insert your URDF-defined robot into the Gazebo simulation.

### Summary

This lesson introduced you to creating custom Gazebo worlds using SDF and the essential process of integrating your URDF robot models into these simulations. You've learned about the structure of an SDF world file and how to use ROS 2 launch files to effectively spawn your robot within Gazebo, bringing your digital twin to life. The ability to create tailored environments is crucial for realistic testing and development, which we will build upon in the next lesson as we begin to interact with our simulated robot.

## Lesson 2.3: Interacting with the Simulated Robot - Physics and Controls

Now that we have our custom Gazebo world and our URDF robot model spawned within it, the next crucial step is to interact with it. This involves understanding how to apply forces, control joints, and observe the physics that govern its behavior in the simulated environment.

### Understanding Gazebo Physics

Gazebo's physics engine is what gives our simulated robots realistic motion. Key aspects include:

*   **Gravity**: By default, Gazebo applies gravity. You can configure its vector in the SDF world file.
*   **Collisions**: Gazebo detects collisions between links of your robot and between the robot and its environment. These are defined by the `<collision>` tags in your URDF/SDF.
*   **Friction**: Surface friction is crucial for realistic interaction. This can be configured in the `<surface>` tag within `<collision>` in SDF, specifying `mu` and `mu2` for dynamic and static friction coefficients.
*   **Inertia**: Defined in the URDF's `<inertial>` tag, inertia dictates how a link responds to forces and torques. Accurate inertia values are vital for realistic dynamic behavior.

### Interacting with the Robot via ROS 2

The primary way to control and interact with your robot in Gazebo (especially in a ROS 2 context) is through ROS 2 interfaces.

#### 1. Applying Forces and Torques

You can apply forces and torques to specific links of your robot using ROS 2 topics. The `gazebo_ros_force_system` plugin, commonly added to robot URDFs or Gazebo models, exposes topics for this purpose.

For example, to apply a wrench (force and torque) to a link:
```bash
ros2 topic pub /<robot_name>/<link_name>/apply_wrench geometry_msgs/msg/WrenchStamped "{header: {stamp: {sec: 0, nanosec: 0}, frame_id: 'world'}, wrench: {force: {x: 10.0, y: 0.0, z: 0.0}, torque: {x: 0.0, y: 0.0, z: 0.0}}}" -1
```
This command applies a 10N force in the x-direction to a specified link.

#### 2. Joint Control

Controlling robot joints is fundamental for making it move. In ROS 2 and Gazebo, this is typically achieved using `ros2_control`, a powerful framework for robot hardware abstraction.

To control a joint, you would generally:
1.  **Define a `ros2_control` interface** in your robot's URDF/XACRO file. This specifies how the joint is actuated (e.g., position, velocity, effort control).
2.  **Load the `ros2_control` controllers** using a ROS 2 launch file. Common controllers include `joint_state_broadcaster` (to publish joint positions) and `joint_trajectory_controller` (to send commands to move joints to specific positions over time).
3.  **Publish commands** to the controller's input topic.

Example of sending a position command to a joint controller:
```bash
ros2 topic pub /joint_group_effort_controller/commands std_msgs/msg/Float64MultiArray "{data: [1.57]}" -1
```
This would command a joint (or a group of joints) to move to 1.57 radians.

#### 3. Reading Sensor Data

Simulated sensors in Gazebo can publish data directly to ROS 2 topics, mirroring real hardware. For example, a simulated camera can publish `/image_raw`, an IMU can publish `/imu/data`, and a LiDAR can publish `/scan`.

You can inspect these topics using standard ROS 2 command-line tools:
```bash
ros2 topic list
ros2 topic echo /imu/data
```
This allows you to develop and test your robot's perception and control algorithms using simulated data before deploying on physical hardware.

### Observing Robot Behavior

As you apply forces or control joints, you can observe the robot's response in the Gazebo GUI. Pay attention to:
*   **Visual feedback**: Does the robot move as expected?
*   **Joint states**: Use `rqt_plot` to visualize joint positions, velocities, and efforts from the `joint_states` topic.
*   **Sensor outputs**: Visualize camera feeds, LiDAR scans, or IMU data to ensure sensors are working correctly.

### Summary

In this lesson, you've learned how to bring your simulated robot to life within Gazebo. By understanding Gazebo's physics and utilizing ROS 2 interfaces, you can apply forces, control joints, and read sensor data, enabling detailed development and testing of your robot's behaviors. This ability to interact with the digital twin is a cornerstone of modern robotics development, providing a safe, repeatable, and cost-effective platform for innovation. The knowledge gained here is crucial as we move towards more complex navigation and manipulation tasks.

## Summary

This chapter provided a foundational understanding of the Gazebo simulator. We learned how to set up Gazebo, create custom simulation environments, and effectively import and interact with our URDF robot model. By simulating our robot under realistic physical conditions, we've established a safe and efficient platform for developing and testing complex robotic behaviors.

## Key Takeaways

*   Gazebo is a powerful 3D robotics simulator compatible with ROS 2.
*   Custom worlds can be created using SDF.
*   URDF models can be imported into Gazebo for simulation.
*   Gazebo simulates realistic physics, including gravity, collisions, and friction.
*   Simulated environments are crucial for safe and efficient robot development.
