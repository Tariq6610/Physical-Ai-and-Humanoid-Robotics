/**
 * Creating a sidebar enables you to:
 - Create an ordered group of docs
 - Render a sidebar from the docs folder structure
 - Perform advanced filtering (e.g. adding a custom file only to a single sidebar)
 */

/** @type {import('@docusaurus/plugin-content-docs').SidebarsConfig} */
const sidebars = {
  // By default, Docusaurus generates a sidebar from the docs folder structure
  tutorialSidebar: [
    'intro', // Assumes intro.md is at the root of the docs folder
    {
      type: 'category',
      label: 'Module I: Core Robotics Foundations',
      items: [
        'module1-core-robotics/ch1-intro-ros',
        'module1-core-robotics/ch2-ros-nodes-topics',
        'module1-core-robotics/ch3-ros-services-actions',
        'module1-core-robotics/ch4-urdf-modeling',
      ],
    },
    {
      type: 'category',
      label: 'Module II: Simulation & Digital Twin',
      items: [
        'module2-simulation/ch5-gazebo-worlds',
        'module2-simulation/ch6-advanced-sensors',
        'module2-simulation/ch7-photorealistic-sim',
      ],
    },
    {
      type: 'category',
      label: 'Module III: The AI-Robot Brain',
      items: [
        'module3-ai-brain/ch8-isaac-ros-perception',
        'module3-ai-brain/ch9-bipedal-locomotion',
      ],
    },
    {
      type: 'category',
      label: 'Module IV: Vision-Language-Action (VLA)',
      items: [
        'module4-vla/ch10-voice-to-action',
        'module4-vla/ch11-cognitive-planning',
        'module4-vla/ch12-capstone-project',
      ],
    },
    {
      type: 'category',
      label: 'Module V: The RAG Chatbot Companion',
      items: [
        'module5-rag-chatbot/ch13-rag-architecture',
        'module5-rag-chatbot/ch14-building-chatbot',
      ],
    },
  ],
};

export default sidebars;
