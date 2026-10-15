import os
import shutil
import subprocess
import time

import numpy as np
import pytest
import mujoco
import mujoco.viewer


MODEL_XML = """
<mujoco model="GPU Test">
  <worldbody>
    <light pos="0 0 3" dir="0 0 -1"/>
    <geom name="floor" type="plane" size="2 2 0.1"
          rgba="0.8 0.8 0.8 1"/>
    <body name="box" pos="0 0 0.5">
      <freejoint/>
      <geom type="box" size="0.15 0.15 0.15"
            mass="1" rgba="0.1 0.5 1 1"/>
    </body>
  </worldbody>
</mujoco>
"""


def test_nvidia_gpu_visibility():
    """Check that NVIDIA is accessible inside the container."""
    if not shutil.which("nvidia-smi"):
        pytest.fail("nvidia-smi is missing from the container")

    result = subprocess.run(
        ["nvidia-smi", "--query-gpu=name", "--format=csv,noheader"],
        capture_output=True,
        text=True,
        timeout=15,
    )

    assert result.returncode == 0, result.stderr
    assert result.stdout.strip(), "No NVIDIA GPU detected"

    print(f"\nDetected GPU:\n{result.stdout.strip()}")


def test_mujoco_installed():
    """Verify MuJoCo is installed."""
    assert mujoco.__version__
    print(f"\nMuJoCo version: {mujoco.__version__}")


def test_mujoco_rendering_uses_nvidia():
    """
    Create a MuJoCo OpenGL context, render a scene,
    and inspect the active context's vendor and renderer.
    """
    from OpenGL.GL import glGetString, GL_VENDOR, GL_RENDERER

    width, height = 128, 128
    model = mujoco.MjModel.from_xml_string(MODEL_XML)
    data = mujoco.MjData(model)
    mujoco.mj_forward(model, data)

    gl_context = None
    mjr_context = None

    try:
        # Uses the MuJoCo OpenGL backend selected by the environment.
        gl_context = mujoco.GLContext(width, height)
        gl_context.make_current()

        vendor_raw = glGetString(GL_VENDOR)
        renderer_raw = glGetString(GL_RENDERER)

        assert vendor_raw is not None, "OpenGL vendor unavailable"
        assert renderer_raw is not None, "OpenGL renderer unavailable"

        vendor = vendor_raw.decode(errors="replace")
        renderer_name = renderer_raw.decode(errors="replace")

        print(f"\nMuJoCo OpenGL vendor: {vendor}")
        print(f"MuJoCo OpenGL renderer: {renderer_name}")

        # Build and render an actual MuJoCo scene.
        mjr_context = mujoco.MjrContext(
            model,
            mujoco.mjtFontScale.mjFONTSCALE_100.value,
        )

        scene = mujoco.MjvScene(model, maxgeom=1000)
        camera = mujoco.MjvCamera()
        option = mujoco.MjvOption()

        mujoco.mjv_defaultCamera(camera)
        mujoco.mjv_defaultOption(option)

        camera.lookat[:] = [0, 0, 0.5]
        camera.distance = 3
        camera.azimuth = 90
        camera.elevation = -20

        mujoco.mjv_updateScene(
            model,
            data,
            option,
            None,
            camera,
            mujoco.mjtCatBit.mjCAT_ALL,
            scene,
        )

        viewport = mujoco.MjrRect(0, 0, width, height)
        mujoco.mjr_render(viewport, scene, mjr_context)

        pixels = np.empty((height, width, 3), dtype=np.uint8)
        depth = np.empty((height, width), dtype=np.float32)

        mujoco.mjr_readPixels(
            pixels,
            depth,
            viewport,
            mjr_context,
        )

        assert np.ptp(pixels) > 0, "Rendered image appears uniform"

 
        assert "nvidia" in vendor.lower(), (
            "MuJoCo rendered a frame, but its OpenGL vendor "
            f"is not NVIDIA: {vendor} / {renderer_name}"
        )

        print("PASS: MuJoCo rendered a frame using an NVIDIA-backed context.")

    finally:
        # Free MuJoCo GL resources while their context is still current.
        if mjr_context is not None:
            mjr_context.free()
        if gl_context is not None:
            gl_context.free()


def test_mujoco_viewer_opens_and_runs():
    """Verify the interactive viewer stays alive while physics advances."""
    if not os.environ.get("DISPLAY"):
        pytest.skip("No desktop DISPLAY available")

    model = mujoco.MjModel.from_xml_string(MODEL_XML)
    data = mujoco.MjData(model)

    with mujoco.viewer.launch_passive(model, data) as viewer:
        assert viewer.is_running(), "MuJoCo viewer failed to start"

        for _ in range(50):
            if not viewer.is_running():
                break

            mujoco.mj_step(model, data)
            viewer.sync()
            time.sleep(0.01)

        assert viewer.is_running(), "Viewer closed unexpectedly"
        assert data.time > 0, "Simulation did not advance"

