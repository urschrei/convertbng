cmake_minimum_required(VERSION 3.21...3.31)
project(
  ${SKBUILD_PROJECT_NAME}
  VERSION ${SKBUILD_PROJECT_VERSION}
  LANGUAGES C)

# Define source directory
set(convertbng_SRC_DIR "${CMAKE_CURRENT_SOURCE_DIR}/src/convertbng")

# Find Python
# ${SKBUILD_SABI_COMPONENT} resolves to "Development.SABIModule" when
# scikit-build-core is targeting the Stable ABI (see wheel.py-api in
# pyproject.toml) and to an empty string otherwise (e.g. CPython 3.10, PyPy).
find_package(
  Python
  COMPONENTS Interpreter Development.Module NumPy ${SKBUILD_SABI_COMPONENT}
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

# Create the extension module.
# When targeting the Stable ABI, ${SKBUILD_SABI_VERSION} holds the minimum
# CPython version (e.g. "3.11"); passing it via USE_SABI makes FindPython define
# Py_LIMITED_API and name the module cutil.abi3.so. When it is empty (CPython
# 3.10, PyPy) we fall back to a regular, version-specific extension module.
if(NOT "${SKBUILD_SABI_VERSION}" STREQUAL "")
  message(STATUS "Building cutil against the Limited API for ${SKBUILD_SABI_VERSION}")
  python_add_library(cutil MODULE "${cutil}" WITH_SOABI USE_SABI ${SKBUILD_SABI_VERSION})
else()
  python_add_library(cutil MODULE "${cutil}" WITH_SOABI)
endif()

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
install(TARGETS cutil DESTINATION ${SKBUILD_PROJECT_NAME})

# Install the shared library
if(APPLE)
  set(LONLAT_BNG_LIB_NAME "liblonlat_bng.dylib")
elseif(UNIX)
  set(LONLAT_BNG_LIB_NAME "liblonlat_bng.so")
elseif(WIN32)
  set(LONLAT_BNG_LIB_NAME "lonlat_bng.dll")
else()
  message(FATAL_ERROR "Unsupported platform: cannot determine lonlat_bng library name")
endif()

install(FILES ${convertbng_SRC_DIR}/${LONLAT_BNG_LIB_NAME}
        DESTINATION ${SKBUILD_PROJECT_NAME})

# Install header file
install(FILES ${convertbng_SRC_DIR}/header.h
        DESTINATION ${SKBUILD_PROJECT_NAME})
