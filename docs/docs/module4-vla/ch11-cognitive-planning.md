---
sidebar_position: 2
title: "Cognitive Planning with Large Language Models (LLMs)"
---

## Introduction

Building on our Voice-to-Action pipeline, this chapter explores how Large Language Models (LLMs) can elevate our robot's intelligence to perform cognitive planning. We will leverage the advanced reasoning capabilities of LLMs to translate complex natural language commands, such as "pick up the red block," into a structured sequence of executable ROS 2 actions. This integration brings a higher level of autonomy and decision-making to our humanoid robot, allowing for more intuitive and flexible task execution.

## Lesson 11.1: LLM Fundamentals for Robotic Planning

**Large Language Models (LLMs)**, like GPT-4, are neural networks trained on vast amounts of text data, giving them a remarkable ability to understand context, reason, and generate human-like text. For robotics, we can leverage this to translate high-level, ambiguous human commands into concrete, step-by-step plans.

### Key LLM Capabilities for Robotics:
- **Zero-Shot/Few-Shot Learning**: LLMs can often perform tasks they haven't been explicitly trained on. By providing a few examples in a "prompt," we can guide the LLM to generate a plan in a specific format.
- **Chain-of-Thought Reasoning**: LLMs can break down a complex problem into intermediate steps, "thinking" through the problem before giving a final answer.
- **Structured Data Generation**: We can prompt an LLM to output its plan in a structured format like JSON, which is easy for a robotic system to parse.

### Prompt Engineering for Robotic Planning
**Prompt engineering** is the art of crafting the right input to an LLM to get the desired output. For robotic planning, a good prompt might include:
- **The robot's current state**: "You are a humanoid robot. Your hand is currently empty."
- **A description of the environment**: "You see a red block and a blue cube on the table in front of you."
- **A list of available actions**: "Your available actions are `moveTo(x, y, z)`, `grasp(object_id)`, and `place(x, y, z)`."
- **The user's command**: "Pick up the red block."
- **Output format instructions**: "Please provide a plan as a JSON list of actions."

## Lesson 11.2: Translating Natural Language to ROS 2 Action Sequences

The core of our cognitive planning system is a node that communicates with an LLM.

### The Workflow:
1.  **Receive Command**: The node receives the parsed natural language command (from our previous VLA chapter).
2.  **Construct Prompt**: It gathers information about the robot's state and environment (e.g., from a perception system that identifies objects and their locations) and constructs a detailed prompt for the LLM.
3.  **Query LLM**: It sends the prompt to an LLM API (like OpenAI's).
4.  **Parse Response**: It receives the LLM's response (ideally a JSON-formatted plan) and parses it into a sequence of executable steps.

**Example Interaction:**

-   **User Command**: "Put the red block on the blue cube."
-   **System State**: The robot knows the `red_block` is at `(0.5, 0.2)` and the `blue_cube` is at `(0.7, 0.5)`.
-   **Generated LLM Plan (in JSON)**:
    ```json
    [
      { "action": "moveTo", "parameters": { "x": 0.5, "y": 0.2, "z": 0.1 } },
      { "action": "grasp", "parameters": { "object_id": "red_block" } },
      { "action": "moveTo", "parameters": { "x": 0.7, "y": 0.5, "z": 0.2 } },
      { "action": "place", "parameters": { "x": 0.7, "y": 0.5, "z": 0.2 } }
    ]
    ```

## Lesson 11.3: Integrating LLM-Generated Plans with the ROS 2 Action System

Once we have a plan from the LLM, we need a "plan executor" node in ROS 2.

### Plan Executor Node:
This node subscribes to the parsed plans and orchestrates the execution of ROS 2 actions.

```python
# Conceptual Python code for a plan executor
import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
import json

# Assume custom action definitions for robot behaviors
# from my_robot_actions.action import MoveTo, Grasp

class PlanExecutor(Node):
    def __init__(self):
        super().__init__('plan_executor')
        self.subscription = self.create_subscription(
            String, # Should be a custom message for plans
            '/llm_plan',
            self.plan_callback,
            10)
        
        # Action clients for each robot capability
        self._move_client = ActionClient(self, MoveTo, 'move_to')
        self._grasp_client = ActionClient(self, Grasp, 'grasp')
        
        self.plan_queue = []
        self.is_executing = False

    def plan_callback(self, msg):
        self.get_logger().info("Received a new plan.")
        new_plan = json.loads(msg.data)
        self.plan_queue.extend(new_plan)
        if not self.is_executing:
            self.execute_next_step()

    def execute_next_step(self):
        if not self.plan_queue:
            self.get_logger().info("Plan complete!")
            self.is_executing = False
            return

        self.is_executing = True
        step = self.plan_queue.pop(0)
        action_type = step['action']
        params = step['parameters']
        
        self.get_logger().info(f"Executing: {action_type} with {params}")

        if action_type == 'moveTo':
            goal_msg = MoveTo.Goal()
            # Populate goal_msg with params...
            self._move_client.wait_for_server()
            future = self._move_client.send_goal_async(goal_msg)
            future.add_done_callback(self.goal_done_callback)
        # Add other action types...
        else:
            self.get_logger().error(f"Unknown action: {action_type}")
            self.execute_next_step() # Move to next step

    def goal_done_callback(self, future):
        # This callback is triggered when the action is done
        self.get_logger().info("Action step finished.")
        # We can check future.result() for success/failure
        self.execute_next_step() # Execute the next step in the plan

```

## Lesson 11.4: Handling Ambiguity, Error Correction, and Human Feedback in LLM Planning

Real-world planning is messy. Our system needs to be robust.

### Handling Ambiguity
If a command is ambiguous (e.g., "pick up the block" when there are multiple blocks), the system can:
-   **Ask for Clarification**: The LLM can be prompted to generate a clarifying question ("Which block do you mean, the red one or the blue one?"), which is then synthesized into speech for the user.
-   **Default Behavior**: Choose the closest or most prominent object as a default.

### Error Correction
-   **Plan Validation**: Before execution, a validation step can check if the LLM's plan is feasible (e.g., is the target location reachable?).
-   **Execution Monitoring**: The system should monitor the result of each action. If a step fails (e.g., `grasp` fails), the system can:
    1.  **Re-plan**: Query the LLM again with the updated state ("I tried to grasp the block but failed. What should I do now?").
    2.  **Ask for Help**: Inform the user about the failure and ask for guidance.

### Human-in-the-Loop Feedback
We can improve the system over time by incorporating feedback. If a plan is inefficient or incorrect, the user can provide a correction. This feedback can be stored and used in future prompts to the LLM, effectively "teaching" it to generate better plans for your specific robot and environment.

## Summary

This chapter demonstrated how Large Language Models can empower humanoid robots with cognitive planning abilities. We successfully translated natural language commands into executable ROS 2 action sequences, integrating LLM intelligence into the robot's decision-making process. This capability significantly enhances the robot's autonomy and flexibility in responding to human instructions.

## Key Takeaways

*   LLMs can be used for high-level cognitive planning in robotics.
*   Prompt engineering guides LLMs to generate structured action sequences.
*   Translating natural language to ROS 2 actions requires careful mapping.
*   Integration with ROS 2 involves validation and execution of LLM plans.
*   Handling ambiguity and errors is crucial for robust LLM-based planning.