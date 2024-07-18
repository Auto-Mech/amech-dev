project(PAC99 Fortran)
cmake_minimum_required(VERSION 2.8)

# These three settings are needed for a static executable
# Linker flags:
#   - Fortran:  -static -static-libgfortran
#   - C:        -static -static-libgcc
#   - C++:      -static -static-libstdc++
set(CMAKE_Fortran_COMPILER "gfortran")
set(CMAKE_FIND_LIBRARY_SUFFIXES ".a")
set(BUILD_SHARED_LIBS OFF)
set(CMAKE_EXE_LINKER_FLAGS "-static -static-libgfortran")

add_executable(pac99 ${PROJECT_SOURCE_DIR}/src/pac99.f)

install(TARGETS pac99 DESTINATION bin)

file(COPY share/new.groups DESTINATION ${CMAKE_INSTALL_PREFIX}/share/pac99)

