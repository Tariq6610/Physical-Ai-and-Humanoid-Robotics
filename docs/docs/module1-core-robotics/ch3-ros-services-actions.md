---
sidebar_position: 3
title: ROS 2 Services and Actions for Complex Behaviors
---

## Introduction

Building upon our understanding of ROS 2 nodes, topics, and messages, this chapter introduces two more advanced communication patterns: Services and Actions. These mechanisms are essential for implementing more complex, coordinated behaviors in robotic systems, enabling both synchronous request-reply interactions and asynchronous, goal-oriented operations with feedback.

## Lesson 3.1: ROS 2 Services for Synchronous Communication

While topics are great for continuous data streams, sometimes a node needs to request a specific task from another node and wait for a result. This is where **ROS 2 Services** come in. Services provide a synchronous, request-reply communication pattern.

### Key Characteristics of Services:
- **Synchronous**: A client sends a request and waits for the server to process it and return a response.
- **One-to-One**: A single service server handles requests from one or more clients, but each request is a one-to-one interaction.
- **Strongly Typed**: Like topics, services have a specific type, defined in a `.srv` file. This file defines both the structure of the request and the structure of the response.

### Creating a Custom Service

Similar to messages, custom services are defined in `.srv` files within a `srv` directory in a ROS 2 package. The request and response parts are separated by `---`.

1.  **Create a `.srv` file**: `~/my_robot_ws/src/my_robot_interfaces/srv/MyCustomSrv.srv`
    ```
    # Request
    int64 a
    int64 b
    ---
    # Response
    int64 sum
    ```

2.  **Modify `CMakeLists.txt` and `package.xml`**: Update your build files to recognize the new service definition, similar to how you handled custom messages.

3.  **Build the package**: Build your workspace with `colcon build`.

### Service Server and Client Example

Here’s how you would implement a server that provides the service and a client that calls it.

**Service Server Node:**
```python
import rclpy
from rclpy.node import Node
from my_robot_interfaces.srv import MyCustomSrv

class MyServiceServer(Node):
    def __init__(self):
        super().__init__('my_service_server')
        self.srv = self.create_service(MyCustomSrv, 'my_service', self.service_callback)
        self.get_logger().info('Service server started.')

    def service_callback(self, request, response):
        self.get_logger().info(f'Incoming request: a={request.a}, b={request.b}')
        response.sum = request.a + request.b
        return response

def main(args=None):
    rclpy.init(args=args)
    node = MyServiceServer()
    rclpy.spin(node)
    rclpy.shutdown()
```

**Service Client Node (Asynchronous call):**
```python
import rclpy
from rclpy.node import Node
from my_robot_interfaces.srv import MyCustomSrv

class MyServiceClient(Node):
    def __init__(self):
        super().__init__('my_service_client')
        self.cli = self.create_client(MyCustomSrv, 'my_service')
        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('service not available, waiting again...')
        self.req = MyCustomSrv.Request()

    def send_request(self, a, b):
        self.req.a = a
        self.req.b = b
        self.future = self.cli.call_async(self.req)
        self.future.add_done_callback(self.future_callback)

    def future_callback(self, future):
        try:
            response = future.result()
            self.get_logger().info(f'Result of service call: {response.sum}')
        except Exception as e:
            self.get_logger().error(f'Service call failed: {e}')

def main(args=None):
    rclpy.init(args=args)
    client_node = MyServiceClient()
    client_node.send_request(5, 10)
    
    while rclpy.ok():
        rclpy.spin_once(client_node)
        if client_node.future.done():
            break
            
    client_node.destroy_node()
    rclpy.shutdown()
```

## Lesson 3.2: ROS 2 Actions for Asynchronous, Goal-Oriented Tasks

For long-running tasks like navigating to a point, executing a multi-step manipulation, or performing a lengthy computation, services are not ideal because they block the client. **ROS 2 Actions** are designed for these scenarios.

### Key Characteristics of Actions:
- **Asynchronous**: The client sends a goal to the action server and does not have to wait for it to complete.
- **Goal-Oriented**: The client sends a specific goal to be achieved.
- **Feedback**: The server can provide continuous feedback on the progress of the goal.
- **Preemptible**: The client can request to cancel the goal at any time.

An action is defined by three parts: a **goal**, a **result**, and **feedback**. These are defined in a `.action` file.

### Creating a Custom Action

1.  **Create a `.action` file**: `~/my_robot_ws/src/my_robot_interfaces/action/MyCustomAction.action`
    ```
    # Goal
    int32 order
    ---
    # Result
    int32[] sequence
    ---
    # Feedback
    int32[] partial_sequence
    ```

2.  **Modify build files and build**, just as you did for messages and services.

### Action Server and Client Example

**Action Server Node:**
```python
import rclpy
from rclpy.node import Node
from rclpy.action import ActionServer
from my_robot_interfaces.action import MyCustomAction
import time

class MyActionServer(Node):
    def __init__(self):
        super().__init__('my_action_server')
        self._action_server = ActionServer(
            self,
            MyCustomAction,
            'my_action',
            self.execute_callback)
        self.get_logger().info('Action server started.')

    def execute_callback(self, goal_handle):
        self.get_logger().info('Executing goal...')
        
        feedback_msg = MyCustomAction.Feedback()
        feedback_msg.partial_sequence = []

        for i in range(goal_handle.request.order):
            feedback_msg.partial_sequence.append(i)
            self.get_logger().info(f'Feedback: {feedback_msg.partial_sequence}')
            goal_handle.publish_feedback(feedback_msg)
            time.sleep(1)

        goal_handle.succeed()
        
        result = MyCustomAction.Result()
        result.sequence = feedback_msg.partial_sequence
        return result

def main(args=None):
    rclpy.init(args=args)
    node = MyActionServer()
    rclpy.spin(node)
    rclpy.shutdown()
```

**Action Client Node:**
```python
import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from my_robot_interfaces.action import MyCustomAction

class MyActionClient(Node):
    def __init__(self):
        super().__init__('my_action_client')
        self._action_client = ActionClient(self, MyCustomAction, 'my_action')

    def send_goal(self, order):
        goal_msg = MyCustomAction.Goal()
        goal_msg.order = order

        self._action_client.wait_for_server()
        self._send_goal_future = self._action_client.send_goal_async(
            goal_msg, 
            feedback_callback=self.feedback_callback)
        self._send_goal_future.add_done_callback(self.goal_response_callback)

    def goal_response_callback(self, future):
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().info('Goal rejected :(')
            return

        self.get_logger().info('Goal accepted :)')
        self._get_result_future = goal_handle.get_result_async()
        self._get_result_future.add_done_callback(self.get_result_callback)

    def get_result_callback(self, future):
        result = future.result().result
        self.get_logger().info(f'Result: {result.sequence}')
        rclpy.shutdown()

    def feedback_callback(self, feedback_msg):
        self.get_logger().info(f'Received feedback: {feedback_msg.feedback.partial_sequence}')

def main(args=None):
    rclpy.init(args=args)
    action_client = MyActionClient()
    action_client.send_goal(10)
    rclpy.spin(action_client)
```

## Lesson 3.3: Implementing Services and Actions in Practice

This hands-on lesson involves creating the custom interfaces and nodes described above. The goal is to build and run the service and action examples, observing their different communication patterns and behaviors in a live ROS 2 system.

*This lesson is intended as a hands-on coding exercise for the reader, following the examples provided in the previous lessons.*

## Summary

This chapter expanded our ROS 2 communication toolkit by introducing Services and Actions. We learned that Services are ideal for immediate request-reply interactions, while Actions provide a robust framework for managing complex, long-duration tasks with continuous feedback. Mastering these patterns is crucial for developing sophisticated and responsive robotic behaviors.

## Key Takeaways

*   ROS 2 Services enable synchronous request-reply communication.
*   ROS 2 Actions provide asynchronous, goal-oriented communication with feedback.
*   Services are suitable for short, atomic tasks.
*   Actions are designed for complex, long-running operations.
*   Implementing both patterns allows for diverse robotic control strategies.
