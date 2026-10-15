# robotics-lab

Implementations of robotics concepts from first principles.

Uses Mujoco for simulation, where required

## Setup

### Requirements

- Linux desktop session (X11)
- Docker
- NVIDIA GPU
- NVIDIA Container Toolkit

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

