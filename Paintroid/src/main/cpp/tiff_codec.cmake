# AN Paint TIFF integration, 2026-09-13. AGPL-3.0-or-later.
# Unmodified official codec releases are hash-pinned by fetch_tiff_sources.py.
set(ANPAINT_TIFF_SOURCE ${CMAKE_CURRENT_LIST_DIR}/../../../build/tiff-source)

function(anpaint_add_tiff_dependencies)
  # libjpeg-turbo explicitly requires a standalone build. Use its supported
  # ExternalProject integration, retaining the Android ABI, NDK and compiler
  # launcher. Build only the static libjpeg API target, with no tools or tests.
  include(ExternalProject)
  set(jpeg_binary ${CMAKE_CURRENT_BINARY_DIR}/tiff-jpeg)
  file(MAKE_DIRECTORY ${jpeg_binary})
  set(jpeg_platform_args)
  foreach(variable CMAKE_TOOLCHAIN_FILE ANDROID_ABI ANDROID_PLATFORM ANDROID_STL
      CMAKE_C_COMPILER CMAKE_C_COMPILER_TARGET CMAKE_SYSROOT CMAKE_MAKE_PROGRAM
      CMAKE_C_COMPILER_LAUNCHER)
    if(DEFINED ${variable} AND NOT "${${variable}}" STREQUAL "")
      list(APPEND jpeg_platform_args "-D${variable}:STRING=${${variable}}")
    endif()
  endforeach()
  ExternalProject_Add(anpaint_tiff_jpeg_build
    SOURCE_DIR ${ANPAINT_TIFF_SOURCE}/libjpeg-turbo
    BINARY_DIR ${jpeg_binary}
    DOWNLOAD_COMMAND ""
    UPDATE_COMMAND ""
    CMAKE_ARGS ${jpeg_platform_args}
      -DCMAKE_BUILD_TYPE:STRING=${CMAKE_BUILD_TYPE}
      -DCMAKE_POSITION_INDEPENDENT_CODE:BOOL=ON
      -DBUILD:STRING=20260913
      -DENABLE_SHARED:BOOL=OFF -DENABLE_STATIC:BOOL=ON
      -DWITH_TURBOJPEG:BOOL=OFF -DWITH_TOOLS:BOOL=OFF -DWITH_TESTS:BOOL=OFF
      -DWITH_JNA:BOOL=OFF -DWITH_FUZZ:BOOL=OFF -DWITH_SIMD:BOOL=OFF
      -DWITH_ARITH_DEC:BOOL=ON -DWITH_ARITH_ENC:BOOL=ON
      "-DCMAKE_C_FLAGS:STRING=${CMAKE_C_FLAGS} -Dmalloc=AnPaintTiffMalloc -Dcalloc=AnPaintTiffCalloc -Drealloc=AnPaintTiffRealloc -Dfree=AnPaintTiffFree"
    BUILD_COMMAND ${CMAKE_COMMAND} --build <BINARY_DIR> --target jpeg-static --parallel 2
    INSTALL_COMMAND ""
    BUILD_BYPRODUCTS ${jpeg_binary}/libjpeg.a)
  add_library(anpaint_tiff_jpeg STATIC IMPORTED GLOBAL)
  set_target_properties(anpaint_tiff_jpeg PROPERTIES
    IMPORTED_LOCATION ${jpeg_binary}/libjpeg.a
    INTERFACE_INCLUDE_DIRECTORIES "${ANPAINT_TIFF_SOURCE}/libjpeg-turbo/src;${jpeg_binary}")
  add_dependencies(anpaint_tiff_jpeg anpaint_tiff_jpeg_build)
  add_library(JPEG::JPEG ALIAS anpaint_tiff_jpeg)
  set(JPEG_FOUND TRUE)
  set(JPEG_LIBRARIES anpaint_tiff_jpeg)
  set(jpeg-prefer-standard ON CACHE BOOL "Use the explicitly pinned libjpeg target" FORCE)
  # These APIs are part of the pinned 3.2.0 build. Avoid a configure-time link
  # probe against the archive, which is generated only during the build phase.
  set(HAVE_JPEGTURBO_DUAL_MODE_8 TRUE CACHE INTERNAL "Pinned libjpeg-turbo API" FORCE)
  set(HAVE_JPEGTURBO_DUAL_MODE_12 TRUE CACHE INTERNAL "Pinned libjpeg-turbo API" FORCE)

  set(BUILD_SHARED_LIBS OFF CACHE BOOL "" FORCE)
  set(tiff-static ON CACHE BOOL "" FORCE)
  foreach(feature tiff-tools tiff-tests tiff-contrib tiff-docs tiff-install
      tiff-cxx libdeflate jbig lerc lzma zstd webp pixarlog logluv thunder next mdi)
    set(${feature} OFF CACHE BOOL "" FORCE)
  endforeach()
  foreach(feature ccitt packbits lzw jpeg old-jpeg zlib)
    set(${feature} ON CACHE BOOL "" FORCE)
  endforeach()
  set(TIFF_MAX_DIR_COUNT 4096 CACHE STRING "Bound directory traversal" FORCE)
  add_subdirectory(${ANPAINT_TIFF_SOURCE}/libtiff tiff EXCLUDE_FROM_ALL)
  add_dependencies(tiff anpaint_tiff_jpeg_build)
  target_compile_definitions(tiff PRIVATE
    malloc=AnPaintTiffMalloc calloc=AnPaintTiffCalloc
    realloc=AnPaintTiffRealloc free=AnPaintTiffFree)
  file(READ ${CMAKE_CURRENT_BINARY_DIR}/tiff/libtiff/tiffconf.h tiff_config)
  foreach(feature ZIP_SUPPORT JPEG_SUPPORT LZW_SUPPORT PACKBITS_SUPPORT CCITT_SUPPORT)
    if(NOT tiff_config MATCHES "#define ${feature} 1")
      message(FATAL_ERROR "Required TIFF codec ${feature} was not configured")
    endif()
  endforeach()
endfunction()
anpaint_add_tiff_dependencies()

add_library(anpaint_tiff SHARED ${CMAKE_CURRENT_LIST_DIR}/tiff_bridge.cpp)
target_include_directories(anpaint_tiff PRIVATE
  ${CMAKE_CURRENT_LIST_DIR}/../../../build/jxl-source
  ${CMAKE_CURRENT_LIST_DIR}/../../../build/jxl-source/third_party/skcms)
target_link_libraries(anpaint_tiff PRIVATE tiff jxl_cms jnigraphics log)
target_link_options(anpaint_tiff PRIVATE "-Wl,-z,max-page-size=16384")
