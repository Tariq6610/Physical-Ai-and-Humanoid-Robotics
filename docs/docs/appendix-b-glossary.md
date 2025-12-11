---
sidebar_position: 2
title: Appendix B - Glossary of Terms
---

# Appendix B: Glossary of Terms

This glossary defines key terms used throughout the Physical AI and Humanoid Robotics book.

## A

### Action
In ROS 2, an Action is a communication pattern that handles long-running tasks with feedback and goal management. It extends the service pattern by allowing continuous feedback during execution and the ability to cancel goals.

### Artificial Intelligence (AI)
The simulation of human intelligence processes by machines, especially computer systems. In robotics, AI enables robots to perceive, reason, learn, and make decisions.

## B

### Behavior Tree
A hierarchical tree structure that models the behavior of a robot or autonomous system. It's commonly used for complex task planning and execution in robotics.

### Bipedal Locomotion
The act of walking on two legs, which is a key challenge in humanoid robotics due to the need for balance and coordination.

## C

### Computer Vision
A field of artificial intelligence that trains computers to interpret and understand the visual world. In robotics, computer vision enables robots to identify objects, navigate spaces, and interact with their environment.

### Control System
A system that manages, commands, directs, or regulates the behavior of other devices or systems. In robotics, control systems regulate the robot's movements and actions.

## D

### Deep Learning
A subset of machine learning based on artificial neural networks with representation learning. It can learn from unstructured or unlabeled data and is used in robotics for perception and decision-making.

### Docusaurus
A modern static website generator optimized for building documentation websites. It's used to host the Physical AI and Humanoid Robotics book.

## E

### Embodiment
The physical form of an AI system. In robotics, embodiment refers to how an AI system is integrated with a physical robot body.

### End Effector
The device at the end of a robot arm that interacts with the environment. Examples include grippers, tools, or sensors.

## F

### Forward Kinematics
The use of joint parameters to compute the configuration of the kinematic chain's end-effector. It's used to determine where the robot's end effector is in space based on joint angles.

### FastAPI
A modern, fast (high-performance), web framework for building APIs with Python 3.7+ based on standard Python type hints.

## G

### Gazebo
A 3D simulation environment for robotics that provides high-fidelity physics simulation and rendering. It's commonly used for testing robot algorithms in a safe virtual environment.

### General Artificial Intelligence (AGI)
A type of AI that can understand, learn, and apply knowledge across different domains at a level equal to or exceeding human intelligence.

## H

### Hardware Acceleration
The use of specialized hardware to perform specific computing tasks more efficiently than on a general-purpose CPU. In robotics, this often involves GPUs for AI inference.

### Humanoid Robot
A robot with a body structure that resembles the human body, typically having a head, torso, two arms, and two legs.

## I

### Isaac ROS
NVIDIA's collection of hardware-accelerated perception and navigation packages for robotics applications, designed to run on NVIDIA GPUs.

### Inverse Kinematics
The mathematical process of determining the joint parameters needed to place the end-effector of a kinematic chain in a specific position and orientation.

## J

### Joint
A connection between two or more links in a robot that allows relative motion between them. Joints can be rotational, prismatic, or other types.

## K

### Kinematics
The branch of mechanics that deals with pure motion, without reference to the masses of the objects or the forces that may have caused the motion. In robotics, it describes the relationship between joint positions and end-effector positions.

## L

### LLM (Large Language Model)
A language model that contains many parameters and is trained on large amounts of text data. LLMs can be used in robotics for natural language processing and task planning.

### LiDAR
Light Detection and Ranging. A remote sensing method that uses light in the form of a pulsed laser to measure distances and create high-resolution maps of the surrounding environment.

### Localization
The process of determining the position and orientation of a robot within a known or unknown environment.

## M

### Machine Learning
A subset of AI that provides systems the ability to automatically learn and improve from experience without being explicitly programmed. It's used in robotics for perception, control, and decision-making.

### Mapping
The process of creating a representation of the environment for a robot to navigate and operate effectively.

### Middleware
Software that provides common services and capabilities to applications beyond what's offered by the operating system. ROS 2 serves as middleware for robotics applications.

## N

### Navigation Stack (Nav2)
The ROS 2 navigation stack that provides path planning, obstacle avoidance, and localization capabilities for mobile robots.

### Node
In ROS 2, a node is an executable that uses ROS 2 client library to communicate with other nodes. It's the basic unit of computation in a ROS 2 system.

## P

### Perception
The ability of a robot to interpret sensory information from its environment. This includes computer vision, audio processing, and other sensing modalities.

### Planning
The process of determining a sequence of actions to achieve a goal. In robotics, this can include motion planning, task planning, and path planning.

### Point Cloud
A set of data points in space, typically representing the external surface of an object. Point clouds are often created by 3D scanners and used in robotics for mapping and perception.

### Pose
The position and orientation of a robot or object in space, typically described by coordinates (x, y, z) and rotation angles (roll, pitch, yaw).

## R

### RAG (Retrieval-Augmented Generation)
A technique that combines information retrieval with language model generation to produce more accurate and contextually relevant responses, particularly useful for question-answering systems.

### Robot Operating System (ROS 2)
A flexible framework for writing robot software. It's a collection of tools, libraries, and conventions that aim to simplify the task of creating complex and robust robot behavior.

### ROS 2 Humble Hawksbill
The LTS (Long Term Support) version of ROS 2 released in May 2022, providing a stable platform for robotics development.

## S

### Sensor Fusion
The process of combining data from multiple sensors to improve the accuracy and reliability of the robot's perception of its environment.

### Service
In ROS 2, a service is a synchronous communication pattern where one node sends a request and waits for a response from another node.

### SLAM (Simultaneous Localization and Mapping)
A computational problem where a robot constructs or updates a map of an unknown environment while simultaneously keeping track of its location within that environment.

### State Machine
A computational model used to design algorithms that can be in one of a finite number of states at any given time. In robotics, state machines are often used to control robot behavior.

## T

### Topic
In ROS 2, a topic is a named bus over which nodes exchange messages. It implements a publish-subscribe communication pattern.

### Transformer Model
A type of deep learning architecture that uses self-attention mechanisms to process sequential data. Transformer models are the foundation for many modern language models.

## U

### URDF (Unified Robot Description Format)
An XML format for representing a robot model in ROS. It describes the robot's physical and visual properties, including links, joints, and materials.

## V

### VLA (Vision-Language-Action)
A paradigm that combines computer vision, natural language processing, and robotic action planning to enable robots to understand and execute natural language commands in visual environments.

### VSLAM (Visual SLAM)
A form of SLAM that uses visual sensors (cameras) as the primary sensor modality for mapping and localization.

## W

### Waypoint
A set of coordinates that identify a point in physical space, used by navigation systems to guide a robot from one location to another.

## Z

### Zero-Shot Learning
A machine learning approach where a model can recognize and classify objects it has never seen before, based on its understanding of related concepts.