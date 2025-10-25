cmake_minimum_required(VERSION 3.15)
project(${SKBUILD_PROJECT_NAME} LANGUAGES C)

# Find Python
find_package(
  Python
  COMPONENTS Interpreter Development.Module NumPy
  REQUIRED)

# Get NumPy include directory
message(STATUS "NumPy include directory: ${Python_NumPy_INCLUDE_DIRS}")

# Cythonize the .pyx file to .c
add_custom_command(
  OUTPUT cutil.c
  COMMENT "Cythonizing ${CMAKE_CURRENT_SOURCE_DIR}/src/convertbng/cutil.pyx"
  COMMAND Python::Interpreter -m cython
          "${CMAKE_CURRENT_SOURCE_DIR}/src/convertbng/cutil.pyx"
          --output-file cutil.c
          -I "${CMAKE_CURRENT_SOURCE_DIR}/src/convertbng"
  DEPENDS src/convertbng/cutil.pyx src/convertbng/convertbng_p.pxd
  VERBATIM)

# Create the extension module
python_add_library(cutil MODULE cutil.c WITH_SOABI)

# Set include directories
target_include_directories(cutil PRIVATE
  ${CMAKE_CURRENT_SOURCE_DIR}/src/convertbng
  ${Python_NumPy_INCLUDE_DIRS}
)

# Link against the Rust library
# The library is pre-built and located in src/convertbng/
find_library(LONLAT_BNG_LIBRARY
  NAMES lonlat_bng liblonlat_bng
  PATHS ${CMAKE_CURRENT_SOURCE_DIR}/src/convertbng
  NO_DEFAULT_PATH
  REQUIRED
)
message(STATUS "Found lonlat_bng library: ${LONLAT_BNG_LIBRARY}")

target_link_libraries(cutil PRIVATE ${LONLAT_BNG_LIBRARY})

# Set RPATH for different platforms
if(APPLE)
  set_target_properties(cutil PROPERTIES
    INSTALL_RPATH "@loader_path"
    BUILD_WITH_INSTALL_RPATH TRUE
  )
elseif(UNIX)
  set_target_properties(cutil PROPERTIES
    INSTALL_RPATH "$ORIGIN"
    BUILD_WITH_INSTALL_RPATH TRUE
  )
endif()

# Install the extension module
install(TARGETS cutil DESTINATION convertbng)

# Install the shared library
if(APPLE)
  set(RDP_LIB_NAME "liblonlat_bng.dylib")
elseif(UNIX)
  set(RDP_LIB_NAME "liblonlat_bng.so")
elseif(WIN32)
  set(RDP_LIB_NAME "lonlat_bng.dll")
endif()

install(FILES ${CMAKE_CURRENT_SOURCE_DIR}/src/convertbng/${RDP_LIB_NAME}
        DESTINATION convertbng)

# Install header file
install(FILES ${CMAKE_CURRENT_SOURCE_DIR}/src/convertbng/header.h
        DESTINATION convertbng)
