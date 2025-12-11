---
sidebar_position: 1
title: Appendix A - Setup and Installation Guide
---

# Appendix A: Setup and Installation Guide

This guide provides detailed instructions for setting up the development environment required for the Physical AI and Humanoid Robotics project.

## System Requirements

- **Operating System**: Ubuntu 22.04 LTS (recommended) or other Linux distributions, macOS, or Windows with WSL2
- **RAM**: 8GB minimum, 16GB recommended
- **Storage**: 20GB free space
- **Processor**: Multi-core processor (Intel i5 or equivalent AMD)

## ROS 2 Installation (Humble Hawksbill)

### Ubuntu Installation

1. Set locale:
   ```bash
   locale  # check for UTF-8
   sudo apt update && sudo apt install locales
   sudo locale-gen en_US.UTF-8
   sudo update-locale LC_ALL=en_US.UTF-8 LANG=en_US.UTF-8
   export LANG=en_US.UTF-8
   ```

2. Add ROS 2 repository:
   ```bash
   sudo apt update && sudo apt install curl gnupg lsb-release
   curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key | sudo gpg --dearmor -o /usr/share/keyrings/ros-archive-keyring.gpg
   echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://packages.ros.org/ros2/ubuntu $(source /etc/os-release && echo $UBUNTU_CODENAME) main" | sudo tee /etc/apt/sources.list.d/ros2.list > /dev/null
   ```

3. Install ROS 2 Humble:
   ```bash
   sudo apt update
   sudo apt install ros-humble-desktop
   ```

4. Install colcon build tool:
   ```bash
   sudo apt install python3-colcon-common-extensions
   ```

5. Source the ROS 2 environment:
   ```bash
   source /opt/ros/humble/setup.bash
   ```

### macOS Installation

For macOS, use Docker to run ROS 2 containers:
```bash
# Install Docker Desktop for Mac
# Then pull the ROS 2 Humble Docker image
docker pull osrf/ros:humble-desktop
```

### Windows Installation

For Windows, use WSL2 with Ubuntu:
1. Install WSL2 with Ubuntu 22.04
2. Follow the Ubuntu installation instructions within WSL2

## Development Tools Installation

### Python Environment

1. Install Python 3.10+:
   ```bash
   sudo apt install python3.10-dev python3.10-venv
   ```

2. Create a virtual environment:
   ```bash
   python3 -m venv ~/ros2_env
   source ~/ros2_env/bin/activate
   pip install --upgrade pip
   ```

### Node.js and Docusaurus

1. Install Node.js (LTS version):
   ```bash
   curl -fsSL https://deb.nodesource.com/setup_lts.x | sudo -E bash -
   sudo apt-get install -y nodejs
   ```

2. Install Docusaurus globally:
   ```bash
   npm install -g @docusaurus/core @docusaurus/preset-classic
   ```

## Simulation Environment Setup

### Gazebo Installation

Gazebo is included with the ROS 2 desktop installation, but you can install the standalone version:
```bash
sudo apt install gazebo
```

### NVIDIA Isaac Sim Setup

1. Install NVIDIA Isaac Sim from the NVIDIA Developer website
2. Ensure your system has a compatible NVIDIA GPU with updated drivers
3. Install Isaac ROS packages:
   ```bash
   sudo apt install ros-humble-isaac-*
   ```

## Backend Services Setup

### FastAPI and Dependencies

1. Create a Python virtual environment for the backend:
   ```bash
   cd backend
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

### Qdrant Vector Database

1. Install Qdrant using Docker:
   ```bash
   docker pull qdrant/qdrant
   docker run -p 6333:6333 -p 6334:6334 qdrant/qdrant
   ```

2. Or install using pip:
   ```bash
   pip install qdrant-client
   ```

## Frontend Setup

1. Navigate to the docs directory:
   ```bash
   cd docs
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm start
   ```

## Environment Variables

Create a `.env` file in the backend directory with the following variables:

```bash
# Qdrant Configuration
QDRANT_URL=http://localhost:6333
QDRANT_API_KEY=your_api_key_here
QDRANT_COLLECTION_NAME=book_content

# OpenAI Configuration (if using OpenAI API)
OPENAI_API_KEY=your_openai_api_key_here

# Backend Configuration
BACKEND_CORS_ORIGINS=["http://localhost:3000", "http://localhost:8000"]
```

## Verification Steps

1. Test ROS 2 installation:
   ```bash
   source /opt/ros/humble/setup.bash
   ros2 topic list
   ```

2. Test Python environment:
   ```bash
   source ~/ros2_env/bin/activate
   python3 -c "import rclpy; print('ROS 2 Python environment OK')"
   ```

3. Test Docusaurus:
   ```bash
   cd docs
   npm run build
   ```

4. Test backend:
   ```bash
   cd backend
   source .venv/bin/activate
   python3 -m pytest tests/
   ```

## Troubleshooting

### Common Issues

- **ROS 2 not found**: Ensure you've sourced the ROS 2 environment (`source /opt/ros/humble/setup.bash`)
- **Python package issues**: Use the virtual environment and ensure all dependencies are installed
- **Docker permission denied**: Add your user to the docker group (`sudo usermod -aG docker $USER`)
- **Port conflicts**: Check if required ports (like 6333 for Qdrant) are already in use

### Getting Help

If you encounter issues during setup:
1. Check the ROS 2 documentation for your specific platform
2. Review the project's GitHub issues for similar problems
3. Create a new issue if your problem is not already documented