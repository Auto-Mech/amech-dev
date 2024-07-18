project(ProjRot C)
cmake_minimum_required(VERSION 2.8)

# These three settings are needed for a static executable
# Linker flags:
#   - Fortran:  -static -static-libgfortran
#   - C:        -static -static-libgcc
#   - C++:      -static -static-libstdc++
set(CMAKE_C_COMPILER "gcc")
set(CMAKE_FIND_LIBRARY_SUFFIXES ".a")
set(BUILD_SHARED_LIBS OFF)
set(CMAKE_EXE_LINKER_FLAGS "-static -static-libgcc")

add_library(ProjRotLibs
    ${PROJECT_SOURCE_DIR}/src/eigen2.c
    ${PROJECT_SOURCE_DIR}/src/eigen.c
    ${PROJECT_SOURCE_DIR}/src/nrutil.c
    ${PROJECT_SOURCE_DIR}/src/spline.c
    ${PROJECT_SOURCE_DIR}/src/invert_matrix3.c)

add_executable(RPHt.exe
    ${PROJECT_SOURCE_DIR}/src/main.c)

target_link_libraries(RPHt.exe ProjRotLibs m)

install(TARGETS RPHt.exe DESTINATION bin)
