set(CBOR_HEADERS
    ${PROJECT_BINARY_DIR}/cbor/configuration.h
    cbor/data.h
    cbor/common.h
    cbor/arrays.h
    cbor/maps.h
    cbor/strings.h
    cbor/ints.h
    cbor/tags.h
    cbor/floats_ctrls.h
    cbor/bytestrings.h
    cbor/encoding.h
    cbor/serialization.h
    cbor/callbacks.h
    cbor/streaming.h
    cbor.h)

set(CBOR_INTERNAL_HEADERS
    cbor/internal/builder_callbacks.h
    cbor/internal/encoders.h
    cbor/internal/memory_utils.h
    cbor/internal/loaders.h
    cbor/internal/stack.h
    cbor/internal/unicode.h)

set(CBOR_SOURCES
    cbor.c
    cbor/internal/builder_callbacks.c
    cbor/internal/encoders.c
    cbor/internal/memory_utils.c
    cbor/internal/loaders.c
    cbor/internal/stack.c
    cbor/internal/unicode.c
    cbor/streaming.c
    cbor/common.c
    cbor/callbacks.c
    cbor/encoding.c
    cbor/serialization.c
    cbor/arrays.c
    cbor/floats_ctrls.c
    cbor/bytestrings.c
    cbor/strings.c
    cbor/maps.c
    cbor/tags.c
    cbor/ints.c)

if(CBOR_CUSTOM_ALLOC)
    list(APPEND CBOR_SOURCES allocators.c)
endif()

configure_file(cbor/configuration.h.in ${PROJECT_BINARY_DIR}/cbor/configuration.h)

if(CBOR_AMALGAMATION)
    find_package(PythonInterp REQUIRED)
    add_custom_command(OUTPUT ${PROJECT_BINARY_DIR}/cbor.h
                       PRE_BUILD
                       COMMAND ${PYTHON_EXECUTABLE}
                               ${CMAKE_CURRENT_SOURCE_DIR}/amalgamate.py
                               ${PROJECT_BINARY_DIR}/cbor.h
                               ${CBOR_HEADERS}
                       DEPENDS ${CMAKE_CURRENT_SOURCE_DIR}/amalgamate.py
                               ${CBOR_HEADERS}
                       WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR})
    add_custom_command(OUTPUT ${PROJECT_BINARY_DIR}/cbor.c
                       PRE_BUILD
                       COMMAND ${PYTHON_EXECUTABLE}
                               ${CMAKE_CURRENT_SOURCE_DIR}/amalgamate.py
                               ${PROJECT_BINARY_DIR}/cbor.c
                               ${CBOR_INTERNAL_HEADERS}
                               ${CBOR_SOURCES}
                       WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
                       DEPENDS ${CMAKE_CURRENT_SOURCE_DIR}/amalgamate.py
                               ${CBOR_INTERNAL_HEADERS}
                               ${CBOR_SOURCES}
                       WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR})
    add_library(cbor ${PROJECT_BINARY_DIR}/cbor.c ${PROJECT_BINARY_DIR}/cbor.h)
    add_library(cbor_shared SHARED ${PROJECT_BINARY_DIR}/cbor.c ${PROJECT_BINARY_DIR}/cbor.h)
else()
    add_library(cbor ${CBOR_SOURCES} ${CBOR_INTERNAL_HEADERS} ${CBOR_HEADERS})
    add_library(cbor_shared SHARED ${CBOR_SOURCES} ${CBOR_INTERNAL_HEADERS} ${CBOR_HEADERS})
endif()

include(GNUInstallDirs)
set(CMAKE_SKIP_BUILD_RPATH FALSE)

if (NOT DEFINED CMAKE_MACOSX_RPATH)
    set(CMAKE_MACOSX_RPATH 0)
endif()

set_target_properties(cbor_shared PROPERTIES OUTPUT_NAME cbor VERSION "0.0.0" SOVERSION 0)

configure_file(libcbor.pc.in libcbor.pc @ONLY)

#http://www.cmake.org/Wiki/CMake:Install_Commands

install(TARGETS cbor cbor_shared
        ARCHIVE DESTINATION ${CMAKE_INSTALL_LIBDIR}
        LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}
        RUNTIME DESTINATION bin)

install(DIRECTORY cbor
        DESTINATION include
        FILES_MATCHING PATTERN "*.h")

install(FILES cbor.h
        DESTINATION include)

install(FILES ${PROJECT_BINARY_DIR}/cbor/configuration.h
        DESTINATION include/cbor)

install(FILES "${CMAKE_CURRENT_BINARY_DIR}/libcbor.pc"
        DESTINATION "${CMAKE_INSTALL_PREFIX}/${CMAKE_INSTALL_LIBDIR}/pkgconfig")
