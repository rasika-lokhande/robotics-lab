#!/bin/sh

# Generate Makefiles from CMakeLists.txt using the "debug" preset in
# CMakePresets.json (Unix Makefiles, Debug build, output folder build/).
# VS Code's CMake Tools (F7) uses the same preset, so both build the same way.
cmake --preset debug

# Compile: runs make inside build/, producing build/HelloWorld
cmake --build --preset debug



