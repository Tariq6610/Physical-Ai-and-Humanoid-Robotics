---
sidebar_position: 2
title: ROS 2 Nodes, Topics, and Messages
---

---
sidebar_position: 2
title: ROS 2 Nodes, Topics, and Messages
---

## Introduction

This chapter delves into the fundamental communication mechanisms within ROS 2: nodes, topics, and messages. Understanding these core concepts is crucial for building distributed robotics applications. We will learn how to create independent computational units (nodes), establish data streams (topics), and define the structure of data exchanged (messages).

## Lesson 2.1: Understanding ROS 2 Nodes

A **ROS 2 node** is the fundamental building block of a ROS 2 system. It's an executable program that performs a specific, well-defined task. By breaking down a complex robotics application into multiple nodes, you create a modular, scalable, and maintainable system.

### Key Characteristics of Nodes:
- **Single Responsibility**: Each node should ideally be responsible for a single task (e.g., controlling a motor, reading a sensor, or planning a path).
- **Independently Executable**: You can run, stop, and restart nodes individually without affecting the rest of the system (provided other nodes handle the temporary absence of its data).
- **Communication Hub**: Nodes communicate with each other using ROS 2's communication mechanisms like topics, services, and actions.

### Creating a Simple ROS 2 Node

Here’s a conceptual example of a minimal ROS 2 node written in Python using `rclpy` (the ROS 2 Python client library):

```python
import rclpy
from rclpy.node import Node

class MyNode(Node):
    def __init__(self):
        super().__init__('my_simple_node')
        self.get_logger().info('Hello from my simple ROS 2 node!')

def main(args=None):
    rclpy.init(args=args)  # Initialize ROS 2 communication
    node = MyNode()        # Create an instance of your node
    rclpy.spin(node)       # Keep the node alive to process callbacks
    node.destroy_node()    # Clean up the node
    rclpy.shutdown()       # Shut down ROS 2 communication

if __name__ == '__main__':
    main()
```
This node, when run, will simply initialize itself and print a message. The `rclpy.spin(node)` function is crucial as it enters a loop, keeping the node running and allowing it to process any incoming data or events (which we'll see in the next lessons).

## Lesson 2.2: ROS 2 Topics for Asynchronous Communication

**Topics** are the primary method for continuous, asynchronous data exchange in ROS 2. They operate on a publish/subscribe model, where one or more nodes can **publish** data to a topic, and one or more nodes can **subscribe** to that topic to receive the data.

### Key Characteristics of Topics:
- **Asynchronous**: Publishers send data whenever they have it, without waiting to see if anyone receives it. Subscribers process data as it arrives.
- **Many-to-Many**: A single topic can have multiple publishers and multiple subscribers.
- **Strongly Typed**: Every topic is associated with a specific **message type** that defines the structure of the data being sent.

### Publisher/Subscriber Example

Let's expand our previous node to include a publisher and a subscriber on the same topic.

```python
import rclpy
from rclpy.node import Node
from std_msgs.msg import String # A standard message type for strings

class SimplePublisher(Node):
    def __init__(self):
        super().__init__('simple_publisher')
        self.publisher_ = self.create_publisher(String, 'my_topic', 10)
        self.timer = self.create_timer(1.0, self.timer_callback) # 1Hz timer
        self.get_logger().info('Publisher node started.')

    def timer_callback(self):
        msg = String()
        msg.data = f'Hello from the publisher! The time is {self.get_clock().now()}'
        self.publisher_.publish(msg)
        self.get_logger().info(f'Publishing: "{msg.data}"')

class SimpleSubscriber(Node):
    def __init__(self):
        super().__init__('simple_subscriber')
        self.subscription = self.create_subscription(
            String,
            'my_topic',
            self.listener_callback,
            10)
        self.get_logger().info('Subscriber node started.')

    def listener_callback(self, msg):
        self.get_logger().info(f'I heard: "{msg.data}"')

def main(args=None):
    rclpy.init(args=args)
    # To run both, you would typically launch them as separate processes.
    # For a simple demo, you could use a multi-threaded executor.
    # However, running them in separate terminals is the standard way.
    
    # In one terminal: run the publisher
    # publisher = SimplePublisher()
    # rclpy.spin(publisher)
    # publisher.destroy_node()

    # In another terminal: run the subscriber
    subscriber = SimpleSubscriber()
    rclpy.spin(subscriber)
    subscriber.destroy_node()

    rclpy.shutdown()
```
In this example, `SimplePublisher` creates a message every second and publishes it to the `my_topic` topic. `SimpleSubscriber` listens to `my_topic` and prints any message it receives.

## Lesson 2.3: Defining and Using ROS 2 Messages

A **ROS 2 message** is a simple data structure that defines the type of data sent over a topic. ROS 2 provides a wide range of standard message types (`std_msgs`, `geometry_msgs`, `sensor_msgs`, etc.), but you will often need to define your own custom messages for specific applications.

### Creating a Custom Message

Custom messages are defined in `.msg` files within a ROS 2 package. The file format is simple, consisting of a series of `type name` pairs.

1.  **Create a `.msg` file**: In a ROS 2 package, create a directory named `msg`, and inside it, create a file like `MyCustomMessage.msg`.

    `~/my_robot_ws/src/my_robot_interfaces/msg/MyCustomMessage.msg`
    ```
    string first_name
    string last_name
    uint8 age
    ```

2.  **Modify `CMakeLists.txt` and `package.xml`**: You must modify your package's build files to make ROS 2 aware of your new message definition so it can generate the necessary C++ and Python code.

    In `package.xml`:
    ```xml
    <build_depend>rosidl_default_generators</build_depend>
    <exec_depend>rosidl_default_runtime</exec_depend>
    <member_of_group>rosidl_interface_packages</member_of_group>
    ```

    In `CMakeLists.txt`:
    ```cmake
    find_package(rosidl_default_generators REQUIRED)
    rosidl_generate_interfaces(${PROJECT_NAME} "msg/MyCustomMessage.msg")
    ```

3.  **Build the package**: After modifying the build files, build your workspace with `colcon build`.

### Using the Custom Message

Once built, you can import and use your custom message just like a standard one:

```python
# Import your custom message
from my_robot_interfaces.msg import MyCustomMessage

# In a publisher node's callback:
msg = MyCustomMessage()
msg.first_name = 'John'
msg.last_name = 'Doe'
msg.age = 30
self.publisher_.publish(msg)

# In a subscriber node's callback:
self.get_logger().info(f'Received: {msg.first_name} {msg.last_name}, Age: {msg.age}')
```

## Lesson 2.4: Practical Node and Topic Implementation

This hands-on lesson integrates our understanding by creating a pair of ROS 2 nodes: one publishing a custom message on a topic and another subscribing to and processing that message. This reinforces the concepts of node creation, topic communication, and custom message usage in a practical context.

*This lesson is intended as a hands-on coding exercise for the reader, following the examples provided in the previous lessons.*

## Summary

This chapter provided a deep dive into ROS 2 nodes, topics, and messages. We learned how these components form the backbone of ROS 2 communication, enabling modular and distributed robotic systems. We covered the creation of nodes, the use of topics for data exchange, and the definition of messages for structured data transmission.

## Key Takeaways

*   ROS 2 nodes are independent computational units.
*   Topics provide asynchronous, many-to-many data streaming.
*   Messages define the data structures for communication.
*   Custom message types enhance application-specific data exchange.
*   Nodes can be designed to publish and subscribe to topics effectively.
