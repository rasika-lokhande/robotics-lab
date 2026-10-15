
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/workspace \
    MUJOCO_GL=egl

RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    openssh-client \
    build-essential \
    cmake \
    gdb \
    libgl1 \
    libegl1 \
    libglfw3 \
    libglew2.2 \
    mesa-utils \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /workspace

COPY requirements.txt .
RUN pip install -r requirements.txt

CMD ["bash"]
