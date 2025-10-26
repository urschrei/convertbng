cmake_minimum_required(VERSION 3.21)
project(${SKBUILD_PROJECT_NAME} LANGUAGES C)

# Define source directory
set(convertbng_SRC_DIR "${CMAKE_CURRENT_SOURCE_DIR}/src/convertbng")

# Find Python
find_package(
  Python
  COMPONENTS Interpreter Development.Module NumPy
  REQUIRED)
include(UseCython)

# Get NumPy include directory
message(STATUS "NumPy include directory: ${Python_NumPy_INCLUDE_DIRS}")

cython_transpile(
  "${convertbng_SRC_DIR}/cutil.pyx"
  LANGUAGE C
  OUTPUT_VARIABLE cutil
  CYTHON_ARGS -I "${convertbng_SRC_DIR}"
)

# Create the extension module
python_add_library(cutil MODULE "${cutil}" WITH_SOABI)

# Set include directories
target_include_directories(cutil PRIVATE
  ${convertbng_SRC_DIR}
  ${Python_NumPy_INCLUDE_DIRS}
)

# Link against the Rust library
# The library is pre-built and located in src/convertbng/
find_library(LONLAT_BNG_LIBRARY
  NAMES lonlat_bng liblonlat_bng
  PATHS ${convertbng_SRC_DIR}
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
  set(LONLAT_BNG_LIB_NAME "liblonlat_bng.dylib")
elseif(UNIX)
  set(LONLAT_BNG_LIB_NAME "liblonlat_bng.so")
elseif(WIN32)
  set(LONLAT_BNG_LIB_NAME "lonlat_bng.dll")
endif()

install(FILES ${convertbng_SRC_DIR}/${LONLAT_BNG_LIB_NAME}
        DESTINATION convertbng)

# Install header file
install(FILES ${convertbng_SRC_DIR}/header.h
        DESTINATION convertbng)
