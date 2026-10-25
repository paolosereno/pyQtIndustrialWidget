cmake_minimum_required(VERSION 3.20)
project(pyQtIndustrialWidget VERSION 0.1.0 LANGUAGES CXX)

# Standard C++ 17 and position independent code
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)
set(CMAKE_POSITION_INDEPENDENT_CODE ON)

# Configure RPATH for runtime resolution of PySide6 and bundled libraries
set(CMAKE_SKIP_BUILD_RPATH FALSE)
set(CMAKE_BUILD_WITH_INSTALL_RPATH TRUE)
set(CMAKE_INSTALL_RPATH_USE_LINK_PATH TRUE)

# Find Python interpreter and development module
find_package(Python 3.9 REQUIRED COMPONENTS Interpreter Development.Module)

# Dynamically locate PySide6 and Shiboken6 packages from Python environment
if(NOT PYSIDE6_DIR)
    execute_process(
        COMMAND ${Python_EXECUTABLE} -c "import PySide6; print(PySide6.__path__[0])"
        OUTPUT_VARIABLE _PYSIDE6_DIR
        OUTPUT_STRIP_TRAILING_WHITESPACE
    )
    set(PYSIDE6_DIR "${_PYSIDE6_DIR}" CACHE PATH "PySide6 package directory" FORCE)
endif()

if(NOT SHIBOKEN6_DIR)
    execute_process(
        COMMAND ${Python_EXECUTABLE} -c "import shiboken6; print(shiboken6.__path__[0])"
        OUTPUT_VARIABLE _SHIBOKEN6_DIR
        OUTPUT_STRIP_TRAILING_WHITESPACE
    )
    set(SHIBOKEN6_DIR "${_SHIBOKEN6_DIR}" CACHE PATH "shiboken6 package directory" FORCE)
endif()

if(NOT SHIBOKEN6_GENERATOR_DIR)
    execute_process(
        COMMAND ${Python_EXECUTABLE} -c "import shiboken6_generator; print(shiboken6_generator.__path__[0])"
        OUTPUT_VARIABLE _SHIBOKEN6_GENERATOR_DIR
        OUTPUT_STRIP_TRAILING_WHITESPACE
    )
    set(SHIBOKEN6_GENERATOR_DIR "${_SHIBOKEN6_GENERATOR_DIR}" CACHE PATH "shiboken6_generator package directory" FORCE)
endif()

if(PYSIDE6_DIR)
    list(APPEND CMAKE_PREFIX_PATH "${PYSIDE6_DIR}" "${PYSIDE6_DIR}/lib/cmake/PySide6")
endif()
if(SHIBOKEN6_DIR)
    list(APPEND CMAKE_PREFIX_PATH "${SHIBOKEN6_DIR}" "${SHIBOKEN6_DIR}/lib/cmake/Shiboken6")
endif()
if(SHIBOKEN6_GENERATOR_DIR)
    list(APPEND CMAKE_PREFIX_PATH "${SHIBOKEN6_GENERATOR_DIR}" "${SHIBOKEN6_GENERATOR_DIR}/lib/cmake/Shiboken6Tools")
endif()

# Prioritize local Qt if present (.venv/Qt or QT_ROOT_DIR)
if(DEFINED ENV{QT_ROOT_DIR} AND EXISTS "$ENV{QT_ROOT_DIR}/lib/cmake/Qt6")
    list(PREPEND CMAKE_PREFIX_PATH "$ENV{QT_ROOT_DIR}")
    message(STATUS "Using Qt6 from QT_ROOT_DIR: $ENV{QT_ROOT_DIR}")
elseif(EXISTS "${CMAKE_CURRENT_SOURCE_DIR}/.venv/Qt/lib/cmake/Qt6")
    list(PREPEND CMAKE_PREFIX_PATH "${CMAKE_CURRENT_SOURCE_DIR}/.venv/Qt")
    message(STATUS "Using local Qt 6.8 from .venv/Qt")
endif()

# Find Qt6
find_package(Qt6 6.2 REQUIRED COMPONENTS Core Gui Widgets)

# Create imported target for Shiboken6
if(NOT TARGET Shiboken6::libshiboken)
    message(STATUS "Creating imported target Shiboken6::libshiboken from Python environment...")
    add_library(Shiboken6::libshiboken SHARED IMPORTED)
    file(GLOB SHIBOKEN_LIB
        "${SHIBOKEN6_DIR}/libshiboken6.abi3*.so*"
        "${SHIBOKEN6_DIR}/libshiboken6*.so*"
        "${SHIBOKEN6_DIR}/libshiboken6*.dylib*"
        "${SHIBOKEN6_DIR}/shiboken6*.lib"
    )
    if(SHIBOKEN_LIB)
        list(GET SHIBOKEN_LIB 0 SHIBOKEN_LIB_FILE)
        set_target_properties(Shiboken6::libshiboken PROPERTIES
            IMPORTED_LOCATION "${SHIBOKEN_LIB_FILE}"
            INTERFACE_INCLUDE_DIRECTORIES "${SHIBOKEN6_GENERATOR_DIR}/include"
        )
        message(STATUS "Found Shiboken6 library: ${SHIBOKEN_LIB_FILE}")
    else()
        message(FATAL_ERROR "Could not find Shiboken6 shared library in ${SHIBOKEN6_DIR}")
    endif()
endif()

# Create imported target for PySide6
if(NOT TARGET PySide6::pyside6)
    message(STATUS "Creating imported target PySide6::pyside6 from Python environment...")
    add_library(PySide6::pyside6 SHARED IMPORTED)
    file(GLOB PYSIDE6_LIB
        "${PYSIDE6_DIR}/libpyside6.abi3*.so*"
        "${PYSIDE6_DIR}/libpyside6.so*"
        "${PYSIDE6_DIR}/libpyside6.abi3*.dylib*"
        "${PYSIDE6_DIR}/libpyside6.dylib*"
        "${PYSIDE6_DIR}/pyside6.lib"
    )
    if(PYSIDE6_LIB)
        list(GET PYSIDE6_LIB 0 PYSIDE6_LIB_FILE)
        set_target_properties(PySide6::pyside6 PROPERTIES
            IMPORTED_LOCATION "${PYSIDE6_LIB_FILE}"
            INTERFACE_INCLUDE_DIRECTORIES "${PYSIDE6_DIR}/include;${PYSIDE6_DIR}/include/PySide6"
        )
        message(STATUS "Found PySide6 library: ${PYSIDE6_LIB_FILE}")
    else()
        message(FATAL_ERROR "Could not find PySide6 shared library in ${PYSIDE6_DIR}")
    endif()
endif()

# Locate shiboken6 generator binary
find_program(SHIBOKEN_EXECUTABLE
    NAMES shiboken6 shiboken6-generator
    HINTS
        ${SHIBOKEN6_GENERATOR_DIR}
        ${SHIBOKEN6_DIR}
        ${Python_SITELIB}/shiboken6_generator
    REQUIRED
)

# Upstream C++ library via FetchContent
include(FetchContent)

set(BUILD_EXAMPLES OFF CACHE BOOL "Build gallery showcase application" FORCE)
set(BUILD_DESIGNER_PLUGIN OFF CACHE BOOL "Build the Qt Designer plugin" FORCE)
set(BUILD_TESTS OFF CACHE BOOL "Build unit test suite" FORCE)
set(BUILD_DOCS OFF CACHE BOOL "Build API documentation" FORCE)

FetchContent_Declare(
    QtIndustrialWidgets
    GIT_REPOSITORY https://github.com/paolosereno/QtIndustrialWidgets.git
    GIT_TAG main
    GIT_SHALLOW TRUE
)

FetchContent_MakeAvailable(QtIndustrialWidgets)

# Locate typesystem search path
if(NOT PYSIDE_TYPESYSTEMS)
    set(PYSIDE_TYPESYSTEMS "${PYSIDE6_DIR}/typesystems")
endif()

# Gather interface include paths
get_target_property(QT6_WIDGETS_INCLUDES Qt6::Widgets INTERFACE_INCLUDE_DIRECTORIES)
get_target_property(QT6_GUI_INCLUDES Qt6::Gui INTERFACE_INCLUDE_DIRECTORIES)
get_target_property(QT6_CORE_INCLUDES Qt6::Core INTERFACE_INCLUDE_DIRECTORIES)
get_target_property(PYSIDE6_INCLUDES PySide6::pyside6 INTERFACE_INCLUDE_DIRECTORIES)

# Compiler builtin include directory for Linux (resolves stddef.h/cstddef in shiboken parsing)
execute_process(
    COMMAND ${CMAKE_CXX_COMPILER} -print-file-name=include
    OUTPUT_VARIABLE COMPILER_BUILTIN_INCLUDE
    OUTPUT_STRIP_TRAILING_WHITESPACE
)

set(SHIBOKEN_INCLUDE_ARGS
    "-I${CMAKE_CURRENT_SOURCE_DIR}"
)

if(EXISTS "${CMAKE_CURRENT_SOURCE_DIR}/compat" AND IS_DIRECTORY "${CMAKE_CURRENT_SOURCE_DIR}/compat")
    list(APPEND SHIBOKEN_INCLUDE_ARGS "-I${CMAKE_CURRENT_SOURCE_DIR}/compat")
endif()

if(COMPILER_BUILTIN_INCLUDE AND IS_DIRECTORY "${COMPILER_BUILTIN_INCLUDE}")
    list(APPEND SHIBOKEN_INCLUDE_ARGS "-I${COMPILER_BUILTIN_INCLUDE}")
endif()

# Add upstream QtIndustrialWidgets source include directory
if(DEFINED qtindustrialwidgets_SOURCE_DIR AND IS_DIRECTORY "${qtindustrialwidgets_SOURCE_DIR}/include")
    list(APPEND SHIBOKEN_INCLUDE_ARGS "-I${qtindustrialwidgets_SOURCE_DIR}/include")
endif()

# Add PySide6 include directories
if(PYSIDE6_DIR)
    foreach(_sub "" "/QtCore" "/QtGui" "/QtWidgets" "/PySide6" "/PySide6/QtCore" "/PySide6/QtGui" "/PySide6/QtWidgets")
        if(IS_DIRECTORY "${PYSIDE6_DIR}/include${_sub}")
            list(APPEND SHIBOKEN_INCLUDE_ARGS "-I${PYSIDE6_DIR}/include${_sub}")
        endif()
    endforeach()
endif()

# Gather interface include paths safely (filtering out raw generator expressions like $<INSTALL_INTERFACE:...>)
set(_CANDIDATE_INCLUDES
    ${QT6_WIDGETS_INCLUDES}
    ${QT6_GUI_INCLUDES}
    ${QT6_CORE_INCLUDES}
    ${PYSIDE6_INCLUDES}
)

foreach(inc IN LISTS _CANDIDATE_INCLUDES)
    if(inc AND NOT inc MATCHES "^\\$<" AND IS_DIRECTORY "${inc}")
        list(APPEND SHIBOKEN_INCLUDE_ARGS "-I${inc}")
    endif()
endforeach()

# Clean up empty items and duplicates
list(REMOVE_ITEM SHIBOKEN_INCLUDE_ARGS "" "-I" "-I\"\"")
list(REMOVE_DUPLICATES SHIBOKEN_INCLUDE_ARGS)
message(STATUS "Shiboken include flags: ${SHIBOKEN_INCLUDE_ARGS}")

# Generated binding C++ sources list
set(GENERATED_SOURCES
    ${CMAKE_CURRENT_BINARY_DIR}/pyQtIndustrialWidget/pyqtindustrialwidget_module_wrapper.cpp
    ${CMAKE_CURRENT_BINARY_DIR}/pyQtIndustrialWidget/qtindustrialwidgets_analysischart_wrapper.cpp
    ${CMAKE_CURRENT_BINARY_DIR}/pyQtIndustrialWidget/qtindustrialwidgets_annunciatorpanel_wrapper.cpp
    ${CMAKE_CURRENT_BINARY_DIR}/pyQtIndustrialWidget/qtindustrialwidgets_circularbargraph_wrapper.cpp
    ${CMAKE_CURRENT_BINARY_DIR}/pyQtIndustrialWidget/qtindustrialwidgets_compass_wrapper.cpp
    ${CMAKE_CURRENT_BINARY_DIR}/pyQtIndustrialWidget/qtindustrialwidgets_industrialknob_wrapper.cpp
    ${CMAKE_CURRENT_BINARY_DIR}/pyQtIndustrialWidget/qtindustrialwidgets_industrialswitch_wrapper.cpp
    ${CMAKE_CURRENT_BINARY_DIR}/pyQtIndustrialWidget/qtindustrialwidgets_ledindicator_wrapper.cpp
    ${CMAKE_CURRENT_BINARY_DIR}/pyQtIndustrialWidget/qtindustrialwidgets_levelmeter_wrapper.cpp
    ${CMAKE_CURRENT_BINARY_DIR}/pyQtIndustrialWidget/qtindustrialwidgets_lineargauge_wrapper.cpp
    ${CMAKE_CURRENT_BINARY_DIR}/pyQtIndustrialWidget/qtindustrialwidgets_radialgauge_wrapper.cpp
    ${CMAKE_CURRENT_BINARY_DIR}/pyQtIndustrialWidget/qtindustrialwidgets_sevensegmentdisplay_wrapper.cpp
    ${CMAKE_CURRENT_BINARY_DIR}/pyQtIndustrialWidget/qtindustrialwidgets_stripchart_wrapper.cpp
)

# Custom command to invoke shiboken6
add_custom_command(
    OUTPUT ${GENERATED_SOURCES}
    COMMAND ${SHIBOKEN_EXECUTABLE}
        --generator-set=shiboken
        --enable-parent-ctor-heuristic
        --enable-return-value-heuristic
        --use-isnull-as-nb_nonzero
        --enable-pyside-extensions
        ${SHIBOKEN_INCLUDE_ARGS}
        -T${PYSIDE_TYPESYSTEMS}
        -T${CMAKE_CURRENT_SOURCE_DIR}
        --output-directory=${CMAKE_CURRENT_BINARY_DIR}
        ${CMAKE_CURRENT_SOURCE_DIR}/bindings.h
        ${CMAKE_CURRENT_SOURCE_DIR}/typesystem.xml
    DEPENDS
        ${CMAKE_CURRENT_SOURCE_DIR}/bindings.h
        ${CMAKE_CURRENT_SOURCE_DIR}/typesystem.xml
    WORKING_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}
    COMMENT "Generating Shiboken6 bindings for pyQtIndustrialWidget"
)

# Build Python module library
Python_add_library(pyQtIndustrialWidget MODULE ${GENERATED_SOURCES})

# Platform-specific RPATH origin
if(APPLE)
    set(_ORIGIN "@loader_path")
else()
    set(_ORIGIN "$ORIGIN")
endif()

# Target properties
set_target_properties(pyQtIndustrialWidget PROPERTIES
    CXX_STANDARD 17
    CXX_STANDARD_REQUIRED ON
    POSITION_INDEPENDENT_CODE ON
    BUILD_WITH_INSTALL_RPATH TRUE
    INSTALL_RPATH "${_ORIGIN};${_ORIGIN}/../lib;${_ORIGIN}/../PySide6;${_ORIGIN}/../PySide6/Qt/lib;${_ORIGIN}/../shiboken6"
)

if(TARGET QtIndustrialWidgets)
    set_target_properties(QtIndustrialWidgets PROPERTIES
        BUILD_WITH_INSTALL_RPATH TRUE
        INSTALL_RPATH "${_ORIGIN};${_ORIGIN}/../PySide6/Qt/lib;${_ORIGIN}/../../PySide6/Qt/lib"
    )
endif()

# Link targets as requested
target_link_libraries(pyQtIndustrialWidget PRIVATE
    QtIndustrialWidgets::QtIndustrialWidgets
    Qt6::Widgets
    PySide6::pyside6
    Shiboken6::libshiboken
)

# Target include directories
target_include_directories(pyQtIndustrialWidget PRIVATE
    ${CMAKE_CURRENT_BINARY_DIR}
    ${CMAKE_CURRENT_BINARY_DIR}/pyQtIndustrialWidget
    ${CMAKE_CURRENT_SOURCE_DIR}
    ${SHIBOKEN6_GENERATOR_DIR}/include
    ${PYSIDE6_DIR}/include
    ${PYSIDE6_DIR}/include/QtCore
    ${PYSIDE6_DIR}/include/QtGui
    ${PYSIDE6_DIR}/include/QtWidgets
    ${PYSIDE6_DIR}/include/PySide6
    ${PYSIDE6_DIR}/include/PySide6/QtCore
    ${PYSIDE6_DIR}/include/PySide6/QtGui
    ${PYSIDE6_DIR}/include/PySide6/QtWidgets
)

if(EXISTS "${CMAKE_CURRENT_SOURCE_DIR}/compat")
    target_include_directories(pyQtIndustrialWidget PRIVATE ${CMAKE_CURRENT_SOURCE_DIR}/compat)
endif()

# Installation for packaging
install(TARGETS pyQtIndustrialWidget DESTINATION pyQtIndustrialWidget)

if(TARGET QtIndustrialWidgets)
    install(TARGETS QtIndustrialWidgets DESTINATION pyQtIndustrialWidget)
endif()

if(EXISTS "${CMAKE_CURRENT_SOURCE_DIR}/pyQtIndustrialWidget/__init__.py")
    install(FILES "${CMAKE_CURRENT_SOURCE_DIR}/pyQtIndustrialWidget/__init__.py" DESTINATION pyQtIndustrialWidget)
endif()
