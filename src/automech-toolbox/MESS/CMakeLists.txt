project(MESS)
cmake_minimum_required(VERSION 2.8)

set(all_permissions OWNER_READ OWNER_WRITE OWNER_EXECUTE GROUP_READ GROUP_EXECUTE WORLD_READ WORLD_EXECUTE)

file(DOWNLOAD http://github.com/Auto-Mech/MESS/raw/master/static/mess mess)
file(DOWNLOAD http://github.com/Auto-Mech/MESS/raw/master/static/partition_function messpf)
file(COPY ${CMAKE_BINARY_DIR}/mess
     DESTINATION ${CMAKE_INSTALL_PREFIX}/bin
     FILE_PERMISSIONS ${all_permissions})
file(COPY ${CMAKE_BINARY_DIR}/messpf
     DESTINATION ${CMAKE_INSTALL_PREFIX}/bin
     FILE_PERMISSIONS ${all_permissions})

