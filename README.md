# robotics-lab

Personal repository for robotics practise and exploration

- Implementations of robotics concepts from first principles
- learning theory underlying robotics
- learning tools and tech stack for robotics development
- best software development practices
- experimentation and trying out any ideas related to robotics

Topics:
- Theory
    - Spatial math
    - Kinematics
    - Control
    - Dynamics
    - State Estimation
    - Robot Learning
- Software development
    - Testing, Evaluations, Validations
    - ROS2 best practices
    - General C++ practice
    - Setting up environments (Docker, etc)

Uses MuJoCo for simulation, where required. May add other simulators in future.

## Setup

### Requirements

- Linux desktop session (X11)
- Docker
- NVIDIA GPU
- NVIDIA Container Toolkit
- Claude Code installed and logged in on the host

Optional
- VS Code Dev Containers Extension

### Build and Start

#### Option 1: Terminal

From repository root,

```bash
docker compose build
bash lab-bringup.sh # Starts container and opens shell
```

Note: The repository is mounted at `/workspace` in the container, so changes made on the host show up there immediately.

#### Option 2: Use VS Code Dev Containers

Open the repo in VS Code and run **Dev Containers: Reopen in Container**.

### Verify setup

Inside the container,

```bash
pytest -s tests/setup
```

