project(THERMP Fortran)
cmake_minimum_required(VERSION 2.8)

# These three settings are needed for a static executable
# Linker flags:
#   - Fortran:  -static -static-libgfortran
#   - C:        -static -static-libgcc
#   - C++:      -static -static-libstdc++
set(CMAKE_FIND_LIBRARY_SUFFIXES ".a")
set(BUILD_SHARED_LIBS OFF)
set(CMAKE_EXE_LINKER_FLAGS "-static -static-libgfortran")

add_executable(thermp ${PROJECT_SOURCE_DIR}/src/Thermp.f)

install(TARGETS thermp DESTINATION bin)
