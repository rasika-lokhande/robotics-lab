
# Think of CMake as a recipe writer: you describe *what* to build here
# (sources, flags, program name), and CMake writes the step-by-step build
# instructions (e.g. a Makefile) for your system. You then run `make` to
# actually compile the code into a program.
#
#   CMakeLists.txt --(cmake)--> Makefile --(make)--> HelloWorld executable


# Minimum CMake version required to process this file
cmake_minimum_required(VERSION 3.16)

# Project name; also sets PROJECT_SOURCE_DIR to this directory
project (HelloWorld)

# Compiler flags
set (CMAKE_CXX_STANDARD 17) # Use C++17
set (CMAKE_CXX_STANDARD_REQUIRED ON)
set (CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Wall -Werror") # Enable all warnings, treat warnings as errors



# Directory containing the project's .cpp sources
set (source_dir "${PROJECT_SOURCE_DIR}/src/")

# Collect every .cpp file in the source directory
# (note: new files are only picked up when CMake is re-run)
file (GLOB source_files "${source_dir}/*.cpp")

# Build the HelloWorld executable from the collected sources
add_executable(HelloWorld ${source_files})

# Let the compiler find headers in include/, so `#include "my_header.h"` works
target_include_directories(HelloWorld PRIVATE "${PROJECT_SOURCE_DIR}/include")
