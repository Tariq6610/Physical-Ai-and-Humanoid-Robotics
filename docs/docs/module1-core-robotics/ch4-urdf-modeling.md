---
sidebar_position: 4
title: Modeling a Humanoid Robot with URDF
---

## Introduction

In this chapter, we shift our focus to the physical representation of our humanoid robot. We will explore the Unified Robot Description Format (URDF), a powerful XML-based language used in ROS 2 to describe a robot's kinematic and dynamic properties, visual appearance, and collision models. Mastering URDF is fundamental for accurately simulating and controlling our robot in a virtual environment.

## Lesson 4.1: Fundamentals of URDF - Links and Joints

A URDF file describes a robot as a tree of **links** connected by **joints**.

-   **`<link>`**: Represents a rigid body part of the robot. It has physical properties like mass and inertia.
-   **`<joint>`**: Defines the kinematic and dynamic relationship between two links. It specifies the type of motion allowed between the links.

### The `<link>` Element

Each link has three key sub-elements:

1.  **`<inertial>`**: Defines the dynamic properties of the link, including its `mass` and `inertia` tensor. The inertia tensor describes the link's resistance to rotational motion.
2.  **`<visual>`**: Defines the visual appearance of the link (what you see). It includes the shape (`<geometry>`) and `material` (color).
3.  **`<collision>`**: Defines the collision geometry of the link (what the physics engine uses for collision detection). It's often a simpler shape than the visual geometry to save computation.

### The `<joint>` Element

The joint element connects two links (a `parent` and a `child`) and defines how they can move relative to each other.

-   **`type`**: The most important attribute. It can be:
    -   `revolute`: A hinge joint that rotates around a single axis (e.g., an elbow).
    -   `continuous`: A revolute joint with no angle limits.
    -   `prismatic`: A sliding joint that moves along an axis.
    -   `fixed`: A rigid connection between two links with no motion.
    -   `floating`: Allows motion in all 6 degrees of freedom.
    -   `planar`: Allows motion in a 2D plane.
-   **`<parent>`** and **`<child>`**: The two links connected by the joint.
-   **`<origin>`**: The transform (position and orientation) of the joint's frame relative to the parent link's frame.
-   **`<axis>`**: The axis of rotation (for revolute joints) or translation (for prismatic joints).
-   **`<limit>`**: For revolute and prismatic joints, this defines the motion limits (e.g., `lower`, `upper`, `velocity`, `effort`).

## Lesson 4.2: Adding Visual and Collision Properties to URDF

For a robot to be visualized and to interact with a simulated world, its links need `<visual>` and `<collision>` properties.

### Visual Properties

The `<visual>` tag defines what the robot looks like.

-   **`<geometry>`**: Can be a primitive shape (`<box>`, `<cylinder>`, `<sphere>`) or a 3D mesh file (`<mesh filename="..."/>`), typically in STL or DAE format.
-   **`<material>`**: Defines the color of the link. It can have a simple `<color>` tag with RGBA values or reference a more complex material definition.

### Collision Properties

The `<collision>` tag defines the physical bounds of the link for the physics engine.

-   **`<geometry>`**: Similar to the visual geometry, but often simplified to a primitive shape (e.g., a cylinder for an arm link) to speed up collision checks. Using complex meshes for collision can be computationally expensive.

**Example of a Link with Visual and Collision Elements:**
```xml
<link name="upper_arm">
  <inertial>
    <mass value="1.0" />
    <inertia ixx="0.01" ixy="0.0" ixz="0.0" iyy="0.01" iyz="0.0" izz="0.01" />
  </inertial>
  <visual>
    <geometry>
      <cylinder length="0.5" radius="0.05" />
    </geometry>
    <material name="blue">
      <color rgba="0.0 0.0 1.0 1.0" />
    </material>
  </visual>
  <collision>
    <geometry>
      <cylinder length="0.5" radius="0.05" />
    </geometry>
  </collision>
</link>
```

## Lesson 4.3: Building a Simple Humanoid URDF Model

Let's apply these concepts to create a basic humanoid URDF. We'll define a torso, a head, and a single arm.

The root link of a URDF is often a "base_link" or a "torso". All other links are connected to it through a chain of joints.

```xml
<?xml version="1.0"?>
<robot name="simple_humanoid">

  <!-- Torso Link -->
  <link name="torso">
    <inertial>
      <mass value="10.0" />
      <inertia ixx="0.1" ixy="0.0" ixz="0.0" iyy="0.1" iyz="0.0" izz="0.1" />
    </inertial>
    <visual>
      <geometry>
        <box size="0.3 0.5 0.7" />
      </geometry>
      <material name="gray">
        <color rgba="0.5 0.5 0.5 1.0" />
      </material>
    </visual>
    <collision>
      <geometry>
        <box size="0.3 0.5 0.7" />
      </geometry>
    </collision>
  </link>

  <!-- Head Link -->
  <link name="head">
    <inertial>
      <mass value="2.0" />
      <inertia ixx="0.01" ixy="0.0" ixz="0.0" iyy="0.01" iyz="0.0" izz="0.01" />
    </inertial>
    <visual>
      <geometry>
        <sphere radius="0.15" />
      </geometry>
      <material name="white">
        <color rgba="1.0 1.0 1.0 1.0" />
      </material>
    </visual>
    <collision>
      <geometry>
        <sphere radius="0.15" />
      </geometry>
    </collision>
  </link>

  <!-- Neck Joint (connects torso and head) -->
  <joint name="neck_joint" type="revolute">
    <parent link="torso"/>
    <child link="head"/>
    <origin xyz="0 0 0.45" rpy="0 0 0"/>
    <axis xyz="0 0 1"/>
    <limit lower="-1.57" upper="1.57" velocity="1.0" effort="10.0"/>
  </joint>

  <!-- Right Arm Link -->
  <link name="right_upper_arm">
    <inertial>
      <mass value="1.5" />
      <inertia ixx="0.01" ixy="0.0" ixz="0.0" iyy="0.01" iyz="0.0" izz="0.01" />
    </inertial>
    <visual>
      <geometry>
        <cylinder length="0.4" radius="0.05" />
      </geometry>
      <material name="blue"/>
    </visual>
    <collision>
      <geometry>
        <cylinder length="0.4" radius="0.05" />
      </geometry>
    </collision>
  </link>

  <!-- Right Shoulder Joint -->
  <joint name="right_shoulder_joint" type="revolute">
    <parent link="torso"/>
    <child link="right_upper_arm"/>
    <origin xyz="0 -0.3 0.25" rpy="0 1.57 0"/>
    <axis xyz="0 1 0"/>
    <limit lower="-1.57" upper="1.57" velocity="1.0" effort="10.0"/>
  </joint>

</robot>
```
This example illustrates how links are defined with their properties and connected by joints to form the robot's structure. A complete humanoid model would have many more links and joints for the legs, a second arm, hands, etc.

## Summary

This chapter provided a comprehensive introduction to URDF, the standard format for describing robots in ROS 2. We covered the essential elements of URDF, including links, joints, and how to define their physical, visual, and collision properties. Through practical application, we began building a simplified humanoid robot model, a crucial step for simulation and control.

## Key Takeaways

*   URDF is an XML-based language for robot description in ROS 2.
*   Links represent the rigid bodies of a robot.
*   Joints define the connections and motion constraints between links.
*   Visual and collision properties are vital for realistic simulation.
*   A well-defined URDF is foundational for robot simulation and control.
