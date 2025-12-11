---
sidebar_position: 1
title: Building a Voice-to-Action Pipeline
---

## Introduction

In this pivotal chapter, we empower our humanoid robot with the ability to understand and respond to natural language. We will construct a complete Voice-to-Action (VLA) pipeline, enabling speech input to be processed and translated into executable commands for our robot. Our journey begins with implementing robust speech-to-text functionality using advanced models like Whisper, laying the foundation for intuitive human-robot interaction.

## Lesson 4.1: Speech-to-Text Fundamentals and Whisper Integration

The ability for a robot to understand spoken commands is a significant leap towards intuitive human-robot interaction. This is achieved through **Speech-to-Text (STT)** technology, which converts spoken language into written text. With the advent of powerful AI models, STT has become highly accurate and accessible. In this lesson, we will integrate **OpenAI's Whisper model**, a state-of-the-art STT system, into our ROS 2-based VLA pipeline.

### Speech-to-Text Fundamentals

At its core, STT involves several stages:

1.  **Audio Capture**: The robot's microphone captures raw audio signals.
2.  **Preprocessing**: The raw audio is cleaned (e.g., noise reduction, normalization) and segmented into smaller, manageable chunks.
3.  **Feature Extraction**: Relevant features are extracted from the audio (e.g., Mel-frequency cepstral coefficients - MFCCs) that represent phonetic information.
4.  **Acoustic Model**: A machine learning model (historically Hidden Markov Models, now deep neural networks) maps the extracted audio features to phonemes or sub-word units.
5.  **Language Model**: This model uses knowledge of grammar, syntax, and vocabulary to assemble the phonemes into coherent words and sentences, predicting the most likely sequence of words.

Modern STT models, especially those based on end-to-end deep learning architectures like transformers, often combine these steps into a single neural network, simplifying the pipeline and improving accuracy.

### Introduction to OpenAI Whisper

OpenAI's Whisper is a general-purpose speech recognition model trained on a large dataset of diverse audio. Its key advantages include:

*   **High Accuracy**: Achieves state-of-the-art performance across various languages and domains.
*   **Robustness**: Handles different accents, background noise, and technical jargon well.
*   **Multilingual Support**: Can transcribe and translate speech in multiple languages.
*   **Open-Source**: The model and its weights are publicly available, allowing for local deployment.

### Integrating Whisper into a ROS 2 System

To integrate Whisper into our robot's perception stack, we will create a ROS 2 node that captures audio, processes it with Whisper, and publishes the transcribed text to a ROS 2 topic.

#### Step 1: Audio Capture Node

First, we need a way to capture audio from the robot's microphone and make it available in ROS 2. This can be done with a dedicated ROS 2 audio driver node or by leveraging existing tools. For simplicity, we can simulate this or use a basic audio input.

#### Step 2: Whisper ROS 2 Node (Conceptual)

We will create a Python ROS 2 node that performs the STT conversion.

```python
import rclpy
from rclpy.node import Node
from std_msgs.msg import String # For publishing transcribed text
from std_msgs.msg import UInt8MultiArray # For receiving audio data

import numpy as np
import whisper # Assuming whisper is installed via pip

class WhisperSTTNode(Node):
    def __init__(self):
        super().__init__('whisper_stt_node')
        self.declare_parameter('whisper_model', 'small')
        self.whisper_model_name = self.get_parameter('whisper_model').get_parameter_value().string_value
        self.model = whisper.load_model(self.whisper_model_name)

        self.subscription = self.create_subscription(
            UInt8MultiArray,
            '/audio/raw', # Topic where raw audio data is published
            self.audio_callback,
            10
        )
        self.publisher = self.create_publisher(
            String,
            '/speech_to_text/transcript', # Topic for transcribed text
            10
        )
        self.get_logger().info(f'Whisper STT Node initialized with model: {self.whisper_model_name}')

        # Buffer for incoming audio (Whisper expects ~30s chunks)
        self.audio_buffer = np.array([])
        self.sampling_rate = 16000 # Whisper's expected sampling rate

    def audio_callback(self, msg):
        # Convert byte array to numpy array (assuming mono 16kHz PCM audio)
        audio_data = np.frombuffer(msg.data, dtype=np.int16).astype(np.float32) / 32768.0
        self.audio_buffer = np.concatenate((self.audio_buffer, audio_data))

        # Process audio in chunks (e.g., every 5 seconds of new audio)
        # This is a simplification; a more robust solution would handle variable audio lengths
        if len(self.audio_buffer) >= self.sampling_rate * 5: # If we have at least 5 seconds of audio
            self.get_logger().info('Processing audio chunk...')
            # Take the last 30 seconds or whatever length Whisper is optimized for
            # For simplicity, let's process the current buffer up to 30s
            process_chunk = self.audio_buffer[-self.sampling_rate * 30:] if len(self.audio_buffer) > self.sampling_rate * 30 else self.audio_buffer
            
            # Reset buffer or keep a sliding window
            self.audio_buffer = np.array([]) # Clear buffer after processing

            try:
                result = self.model.transcribe(process_chunk, fp16=False) # fp16=True for GPU
                transcript_msg = String()
                transcript_msg.data = result["text"].strip()
                if transcript_msg.data: # Only publish if there's actual speech
                    self.publisher.publish(transcript_msg)
                    self.get_logger().info(f'Transcript: "{transcript_msg.data}"')
            except Exception as e:
                self.get_logger().error(f"Error during transcription: {e}")

def main(args=None):
    rclpy.init(args=args)
    node = WhisperSTTNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

```

#### Step 3: Launching the Whisper Node

You would include this node in a ROS 2 launch file, possibly alongside an audio capture node:

```python
# In your launch file (e.g., launch/vla_pipeline.launch.py)
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        # Assuming an audio capture node publishes to /audio/raw
        # Example: Node(package='audio_driver', executable='audio_node', ...)
        
        Node(
            package='my_vla_package', # Replace with your package name
            executable='whisper_stt_node',
            name='whisper_stt_node',
            output='screen',
            parameters=[{'whisper_model': 'base'}] # or 'small', 'medium', 'large'
        )
    ])
```

### Summary

Integrating a robust Speech-to-Text system like OpenAI Whisper is the foundational step for enabling voice control in our humanoid robot. By creating a dedicated ROS 2 node, we can effectively capture audio, transcribe it into text, and publish it as a standard ROS 2 message. This transcribed text then becomes the input for the next stages of our Voice-to-Action pipeline, where we will parse natural language commands and map them to robot actions.

## Lesson 4.2: Parsing Natural Language Commands for Robot Control

Once we have successfully transcribed spoken commands into text using Speech-to-Text (STT), the next critical step in our Voice-to-Action (VLA) pipeline is to make sense of that text. This involves **parsing natural language commands** to extract meaning, identify key entities, determine intent, and transform the unstructured human language into a structured, machine-interpretable format that our robot can act upon.

### The Challenge of Natural Language Understanding (NLU)

Natural language is inherently complex and ambiguous. The same command can be phrased in countless ways, and context often plays a crucial role in its interpretation. For a robot, this presents several challenges:

*   **Variability**: "Move forward," "Go ahead," "Advance," and "Proceed" all convey a similar command.
*   **Ambiguity**: "Pick up the block" – which block? What color? Where is it?
*   **Context Dependence**: "Turn left" – left relative to what? The robot, the table, or the user?
*   **Implicit Information**: Commands often omit details that are obvious to a human but need to be inferred by a robot.

### Approaches to Natural Language Parsing

There are several techniques we can employ to tackle these challenges:

1.  **Keyword Spotting / Rule-Based Parsing**:
    *   **Concept**: The simplest approach. We define a set of keywords and phrases that, when detected, trigger specific robot actions.
    *   **Pros**: Easy to implement for simple commands, fast.
    *   **Cons**: Very brittle, does not handle synonyms or variations well, struggles with complex sentences, poor scalability.
    *   *Example*: If "move forward" is detected, trigger a `move_forward` action.

2.  **Intent Recognition and Entity Extraction (NLU Systems)**:
    *   **Concept**: This is a more sophisticated approach, often using machine learning (e.g., neural networks) to understand the user's **intent** (what they want to achieve) and extract **entities** (the specific pieces of information relevant to that intent).
    *   **Intent**: The goal or purpose of the command (e.g., `MOVE`, `PICK_UP`, `REPORT_STATUS`).
    *   **Entities**: The parameters or arguments for the intent (e.g., `direction: forward`, `object: red_block`, `location: table`).
    *   **Pros**: More robust to variations in phrasing, can handle more complex commands, scalable with more training data.
    *   **Cons**: Requires training data, can be complex to set up.
    *   *Tools*: Libraries like Rasa NLU, spaCy, or even large language models (LLMs) can be adapted for this.

3.  **Semantic Parsing / Abstract Meaning Representation**:
    *   **Concept**: Aims to convert natural language directly into a formal, machine-executable representation (e.g., a logical form, a set of API calls, or a robot-specific command structure).
    *   **Pros**: Highly expressive, directly generates executable commands.
    *   **Cons**: Very complex to develop, requires deep linguistic understanding or very large datasets.

### Practical Implementation: Intent and Entity Extraction

For our humanoid robot, a hybrid approach combining rule-based methods with a lightweight NLU system (or a small LLM for intent/entity extraction) often provides a good balance between complexity and capability.

Let's consider a simple example using Python and basic string matching, which can be extended with NLU libraries.

**Example Command**: "Robot, move forward by two meters."

1.  **Tokenization**: Break the sentence into words: `["Robot", ",", "move", "forward", "by", "two", "meters", "."]`
2.  **Intent Recognition**: Look for keywords indicating an action. "move" suggests a `MOVE` intent.
3.  **Entity Extraction**:
    *   **Direction**: "forward" -> `direction: FORWARD`
    *   **Distance**: "two meters" -> `distance: 2.0`, `unit: METERS`

#### Conceptual Python Logic

```python
import re

def parse_command(transcript):
    transcript = transcript.lower()
    intent = None
    entities = {}

    # Intent: Move
    if re.search(r'\b(move|go|walk|advance|proceed)\b', transcript):
        intent = 'MOVE'
        if re.search(r'\b(forward|ahead)\b', transcript):
            entities['direction'] = 'FORWARD'
        elif re.search(r'\b(backward|back|reverse)\b', transcript):
            entities['direction'] = 'BACKWARD'
        elif re.search(r'\b(left)\b', transcript):
            entities['direction'] = 'LEFT'
        elif re.search(r'\b(right)\b', transcript):
            entities['direction'] = 'RIGHT'
        
        # Extract distance
        distance_match = re.search(r'\b(by|for)\s+(\w+)\s+(meters|metres|cms|centimeters|centimetres)\b', transcript)
        if distance_match:
            try:
                num_word = distance_match.group(2)
                # Simple word-to-number conversion (can be expanded)
                num_map = {'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5, 'six': 6, 'seven': 7, 'eight': 8, 'nine': 9, 'ten': 10}
                if num_word.isdigit():
                    entities['distance'] = float(num_word)
                elif num_word in num_map:
                    entities['distance'] = float(num_map[num_word])
                
                unit = distance_match.group(3)
                if unit in ['meters', 'metres']:
                    entities['unit'] = 'METERS'
                elif unit in ['cms', 'centimeters', 'centimetres']:
                    entities['unit'] = 'CENTIMETERS'
                
            except ValueError:
                pass # Handle non-numeric or unparseable distances

    # Intent: Pick Up (more complex, requires object recognition)
    elif re.search(r'\b(pick up|grab|grasp)\b', transcript):
        intent = 'PICK_UP'
        object_match = re.search(r'\b(the)\s+(red|blue|green|yellow)?\s*(block|cube|sphere)\b', transcript)
        if object_match:
            if object_match.group(2): # Color
                entities['color'] = object_match.group(2)
            entities['object'] = object_match.group(3)

    return {'intent': intent, 'entities': entities}

# Example Usage:
# transcript = "Robot, move forward by two meters."
# parsed_command = parse_command(transcript)
# print(parsed_command) 
# Output: {'intent': 'MOVE', 'entities': {'direction': 'FORWARD', 'distance': 2.0, 'unit': 'METERS'}}
```

This conceptual parser would run in a ROS 2 node, subscribing to the `/speech_to_text/transcript` topic and publishing a structured command message (e.g., a custom ROS 2 message defining `Intent` and `Entities`) to a new topic like `/robot/command`.

### Summary

Parsing natural language commands is a critical bridge between human intention and robot action. By employing techniques like intent recognition and entity extraction, we can translate the variability and ambiguity of human speech into a structured, machine-interpretable format. This lesson provided a foundation for building such a parser, which will now feed directly into the next stage of our VLA pipeline: mapping these structured commands to executable ROS 2 actions for our humanoid robot.

## Lesson 4.3: Mapping Parsed Commands to ROS 2 Actions

With the natural language command successfully parsed into a structured format (intent and entities), the final stage of our Voice-to-Action (VLA) pipeline is to translate this structured command into a sequence of executable robot behaviors using ROS 2 actions or service calls. This **mapping layer** is the bridge between the robot's high-level understanding and its low-level control.

### The Role of ROS 2 Actions and Services

As discussed in Module 1, ROS 2 provides two primary mechanisms for triggering robot behaviors:

*   **Services**: Ideal for short-duration, synchronous tasks that return a single result (e.g., "get current battery level").
*   **Actions**: Designed for long-running, asynchronous tasks that provide continuous feedback and can be preempted (e.g., "navigate to a goal," "perform a complex manipulation sequence"). Given the nature of most robot movements and tasks, **ROS 2 Actions are often the preferred choice for mapping parsed natural language commands.**

### Designing the Mapping Logic

The mapping logic will reside in a dedicated ROS 2 node, which subscribes to the structured command messages (e.g., `/robot/command`) and then, based on the `intent` and `entities`, calls the appropriate ROS 2 Action clients or Service clients.

#### 1. Defining Robot Capabilities (Action/Service Interfaces)

Before mapping, we need to know what our robot can actually do. This involves having well-defined ROS 2 Action/Service interfaces for common behaviors:

*   **Navigation**: `nav2_msgs/NavigateToPose` Action (for moving to a specific location).
*   **Manipulation**: `robotiq_gripper_msgs/GripperCommand` Action (for opening/closing a gripper).
*   **Locomotion**: Custom actions for specific humanoid movements (e.g., `walk_forward`, `turn_left`).
*   **Reporting**: Services like `robot_status_msgs/GetBatteryStatus`.

#### 2. Intent-to-Action Mapping

The core of the mapping layer is a logic that, for each `intent`, identifies the corresponding ROS 2 Action/Service and constructs the appropriate goal message using the extracted `entities`.

**Example: `MOVE` Intent**

If our parsed command is `{'intent': 'MOVE', 'entities': {'direction': 'FORWARD', 'distance': 2.0, 'unit': 'METERS'}}`, the mapping node would:

1.  Identify that `MOVE` intent corresponds to a `WalkForward` custom action (or potentially a `NavigateToPose` action if more sophisticated navigation is needed).
2.  Construct a `WalkForward.Goal` message.
3.  Populate the goal message with `distance: 2.0` and `direction: FORWARD` (after converting units if necessary).
4.  Send the goal to the `WalkForward` action server.

#### Conceptual Python Logic for Mapping Node

```python
import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from std_msgs.msg import String # For receiving parsed commands
from example_interfaces.action import FollowTargets # Example custom action

# Define custom messages for structured commands (not shown, but assumed)
# from my_robot_msgs.msg import StructuredCommand

class CommandMapperNode(Node):
    def __init__(self):
        super().__init__('command_mapper_node')
        self.subscription = self.create_subscription(
            String, # Assuming a String for simplicity, should be custom msg
            '/robot/command',
            self.command_callback,
            10
        )
        self.get_logger().info('Command Mapper Node initialized.')

        # Create action clients for various robot capabilities
        self._move_action_client = ActionClient(self, FollowTargets, 'follow_targets') # Example Move Action

    def command_callback(self, msg):
        # In a real scenario, msg.data would be a JSON string of intent/entities
        # For this example, let's just parse it directly.
        # This part should ideally use a custom structured message type
        parsed_command = self.parse_simple_string_command(msg.data) # A very simplified parser for demonstration
        
        intent = parsed_command.get('intent')
        entities = parsed_command.get('entities', {})

        if intent == 'MOVE':
            self.handle_move_command(entities)
        elif intent == 'PICK_UP':
            self.handle_pick_up_command(entities)
        # Add more intents and handlers here

    def parse_simple_string_command(self, text):
        # This is a highly simplified parser for demonstration purposes only.
        # In production, use the NLU system from Lesson 4.2.
        text = text.lower()
        if "move forward" in text:
            return {'intent': 'MOVE', 'entities': {'direction': 'FORWARD', 'distance': 1.0, 'unit': 'METERS'}}
        if "pick up block" in text:
            return {'intent': 'PICK_UP', 'entities': {'object': 'block'}}
        return {'intent': None, 'entities': {}}


    def handle_move_command(self, entities):
        direction = entities.get('direction', 'FORWARD')
        distance = entities.get('distance', 0.5) # Default to 0.5m if not specified

        # Assume 'FollowTargets' action can handle a simple move command
        goal_msg = FollowTargets.Goal()
        # Populate goal based on direction and distance
        # This is highly dependent on your specific action definition
        if direction == 'FORWARD':
            self.get_logger().info(f'Sending move forward goal: {distance} meters')
            # For example: goal_msg.target_x = distance, goal_msg.target_y = 0.0
            # Send goal to action server
            self._send_goal_future = self._move_action_client.send_goal_async(goal_msg)
            self._send_goal_future.add_done_callback(self.goal_response_callback)
        else:
            self.get_logger().warn(f'Move direction {direction} not fully implemented.')

    def goal_response_callback(self, future):
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().error('Goal rejected :(')
            return

        self.get_logger().info('Goal accepted :)')
        self._get_result_future = goal_handle.get_result_async()
        self._get_result_future.add_done_callback(self.get_result_callback)

    def get_result_callback(self, future):
        result = future.result().result
        self.get_logger().info(f'Result: {result.success}') # Assuming a 'success' field
        # Optionally, get feedback
        # feedback = future.result().feedback
        # self.get_logger().info(f'Feedback: {feedback.current_progress}')


    def handle_pick_up_command(self, entities):
        obj = entities.get('object', 'unknown')
        self.get_logger().info(f'Handling pick up command for: {obj}')
        # Logic to call a manipulation action client (e.g., with object pose)
        # ...

def main(args=None):
    rclpy.init(args=args)
    node = CommandMapperNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

#### 3. Handling Context and Ambiguity

Advanced mapping layers might also:

*   **Maintain State**: Remember previous commands to infer context (e.g., "now turn left" implies turning left from the current orientation).
*   **Query Perception**: If an entity is ambiguous ("pick up the block"), the robot might query its perception system (e.g., "Which block do you mean?") or ask the user for clarification.
*   **Error Handling**: Gracefully handle commands that cannot be mapped or executed, providing feedback to the user.

### Summary

The mapping layer is the operational heart of the Voice-to-Action pipeline, transforming human intentions into concrete robot actions. By subscribing to structured natural language commands and leveraging ROS 2 Actions and Services, our `CommandMapperNode` can orchestrate complex robot behaviors. This final stage completes the loop, allowing our humanoid robot to seamlessly transition from understanding speech to executing intelligent actions in its environment. With this, our VLA pipeline is complete, enabling intuitive and effective voice control for autonomous systems.

## Summary

This chapter successfully laid the groundwork for voice control by building a Voice-to-Action pipeline. We implemented speech-to-text capabilities using Whisper, developed methods for parsing natural language commands, and established a clear mapping to ROS 2 actions. This pipeline is a crucial step towards creating a truly interactive and intelligent humanoid robot.

## Key Takeaways

*   A Voice-to-Action (VLA) pipeline enables natural language control of robots.
*   Speech-to-text models like Whisper are essential for transcribing voice commands.
*   Parsing natural language involves extracting intent and key information.
*   Mapping parsed commands to ROS 2 actions facilitates robot execution.
*   VLA is key for intuitive human-robot interaction.
