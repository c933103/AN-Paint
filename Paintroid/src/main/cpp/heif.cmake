# AN Paint HEIF-family codecs. AGPL-3.0-or-later; library terms remain separate.
set(HEIF_SOURCES ${CMAKE_CURRENT_LIST_DIR}/../../../build/heif-source)

# libde265 and other siblings use unnamespaced HAVE_* cache entries. AOM's
# default setter preserves those entries, even for its generic CPU configuration.
# Isolate all CPU/SIMD flags while AOM configures its sources and RTCD headers,
# then restore the sibling cache so later reconfiguration does not disable their
# independently detected optimizations.
function(anpaint_add_generic_aom)
  set(aom_cpu_flags
      AOM_ARCH_AARCH64 AOM_ARCH_ARM AOM_ARCH_PPC AOM_ARCH_X86 AOM_ARCH_X86_64 AOM_ARCH_RISCV
      HAVE_NEON HAVE_ARM_CRC32 HAVE_NEON_DOTPROD HAVE_NEON_I8MM HAVE_SVE HAVE_SVE2
      HAVE_VSX HAVE_MMX HAVE_SSE HAVE_SSE2 HAVE_SSE3 HAVE_SSSE3 HAVE_SSE4_1 HAVE_SSE4_2
      HAVE_AVX HAVE_AVX2 HAVE_AVX512 HAVE_RVV)
  foreach(flag IN LISTS aom_cpu_flags)
    if(DEFINED CACHE{${flag}})
      set(${flag}_was_cached TRUE)
      get_property(${flag}_saved_value CACHE ${flag} PROPERTY VALUE)
      get_property(${flag}_saved_type CACHE ${flag} PROPERTY TYPE)
      get_property(${flag}_saved_help CACHE ${flag} PROPERTY HELPSTRING)
      get_property(${flag}_saved_advanced CACHE ${flag} PROPERTY ADVANCED)
    endif()
    set(${flag} 0 CACHE STRING "AN Paint: generic AOM CPU configuration" FORCE)
    set(${flag} 0)
  endforeach()
  set(AOM_TARGET_CPU generic CACHE STRING "" FORCE)
  set(AOM_TARGET_CPU generic)
  add_subdirectory(${HEIF_SOURCES}/aom aom EXCLUDE_FROM_ALL)
  foreach(flag IN LISTS aom_cpu_flags)
    if(${flag}_was_cached)
      set(${flag} "${${flag}_saved_value}" CACHE ${${flag}_saved_type} "${${flag}_saved_help}" FORCE)
      set_property(CACHE ${flag} PROPERTY ADVANCED "${${flag}_saved_advanced}")
    else()
      unset(${flag} CACHE)
    endif()
  endforeach()
endfunction()

# Group the HEIF family in a normal-variable scope. Vendor cache writes still
# need explicit isolation or target overrides, as documented below.
function(anpaint_add_heif)
  set(BUILD_SHARED_LIBS OFF CACHE BOOL "" FORCE)
  set(BUILD_TESTING OFF CACHE BOOL "" FORCE)
  foreach(flag ENABLE_SDL ENABLE_DECODER ENABLE_ENCODER ENABLE_SHERLOCK265 ENABLE_INTERNAL_DEVELOPMENT_TOOLS ENABLE_AVX512)
    set(${flag} OFF CACHE BOOL "" FORCE)
  endforeach()
  add_subdirectory(${HEIF_SOURCES}/libde265 de265 EXCLUDE_FROM_ALL)

  # The upstream Kvazaar CMake writes version files into its source directory,
  # which races across Android ABIs. Build its library sources with an ABI-local
  # version header and portable strategies instead. The fetch script also fixes
  # its optional RD logging mutex lifetime on Android.
  set(KVZ_ROOT ${HEIF_SOURCES}/kvazaar)
  file(GLOB kvz_sources ${KVZ_ROOT}/src/*.c)
  list(REMOVE_ITEM kvz_sources ${KVZ_ROOT}/src/encmain.c ${KVZ_ROOT}/src/cli.c ${KVZ_ROOT}/src/yuv_io.c)
  file(GLOB_RECURSE kvz_strategies ${KVZ_ROOT}/src/strategies/*.c)
  set(PROJECT_VERSION 2.3.2)
  set(KVZ_COMPILER_STRING "${CMAKE_C_COMPILER_ID} ${CMAKE_C_COMPILER_VERSION}")
  set(CMAKE_BUILD_DATE "2026-09-12")
  configure_file(${KVZ_ROOT}/src/version.h.in ${CMAKE_CURRENT_BINARY_DIR}/kvazaar-generated/version.h @ONLY)
  add_library(anpaint_kvazaar STATIC ${kvz_sources} ${kvz_strategies} ${KVZ_ROOT}/src/extras/libmd5.c)
  # Kvazaar's x86 CPU feature detection uses GNU inline asm. Request its
  # dialect explicitly; AOM otherwise leaves strict C11 flags in the CMake cache.
  set_target_properties(anpaint_kvazaar PROPERTIES C_STANDARD 11 C_STANDARD_REQUIRED YES C_EXTENSIONS ON)
  target_compile_definitions(anpaint_kvazaar PRIVATE CMAKE_BUILD KVZ_DLL_EXPORTS)
  target_include_directories(anpaint_kvazaar PUBLIC ${KVZ_ROOT}/src PRIVATE ${KVZ_ROOT}/src/extras ${KVZ_ROOT}/src/strategies ${CMAKE_CURRENT_BINARY_DIR}/kvazaar-generated)
  target_link_libraries(anpaint_kvazaar PUBLIC m)

  foreach(flag ENABLE_APPS ENABLE_DOCS ENABLE_EXAMPLES ENABLE_TESTDATA ENABLE_TESTS ENABLE_TOOLS)
    set(${flag} OFF CACHE BOOL "" FORCE)
  endforeach()
  set(CONFIG_AV1_ENCODER 1 CACHE STRING "" FORCE)
  set(CONFIG_AV1_DECODER 1 CACHE STRING "" FORCE)
  foreach(flag CONFIG_HIGHWAY CONFIG_LIBYUV CONFIG_WEBM_IO CONFIG_TUNE_BUTTERAUGLI)
    set(${flag} 0 CACHE STRING "" FORCE)
  endforeach()
  # Portable baseline on every ABI: no assembler executable or CPU detection
  # assumptions at installation time. SIMD can be enabled after ARM profiling.
  anpaint_add_generic_aom()

  # Give libheif real in-tree targets through its normal Find modules.
  set(LIBDE265_INCLUDE_DIR ${HEIF_SOURCES}/libde265 CACHE PATH "" FORCE)
  set(LIBDE265_LIBRARY de265 CACHE STRING "" FORCE)
  set(KVAZAAR_INCLUDE_DIR ${KVZ_ROOT}/src CACHE PATH "" FORCE)
  # Kvazaar is private to this Android build. Keep it out of libheif's unrelated
  # install/export package, which otherwise rejects this unexported app target.
  set(KVAZAAR_LIBRARY "$<BUILD_INTERFACE:anpaint_kvazaar>" CACHE STRING "" FORCE)
  set(HAVE_KVAZAAR_ENABLE_LOGGING 1 CACHE INTERNAL "" FORCE)
  set(HAVE_KVAZAAR_VERSION_STRING 0 CACHE INTERNAL "" FORCE)
  set(AOM_INCLUDE_DIR ${HEIF_SOURCES}/aom CACHE PATH "" FORCE)
  set(AOM_LIBRARY aom CACHE STRING "" FORCE)
  set(aom_usage_flag_exists 1 CACHE INTERNAL "" FORCE)
  foreach(codec X265 X264 OpenH264_DECODER OpenH264_ENCODER DAV1D SvtEnc RAV1E JPEG_DECODER JPEG_ENCODER OpenJPEG_DECODER OpenJPEG_ENCODER FFMPEG_DECODER OPENJPH_ENCODER UVG266 VVDEC VVENC WEBCODECS UNCOMPRESSED_CODEC LIBSHARPYUV)
    set(WITH_${codec} OFF CACHE BOOL "" FORCE)
  endforeach()
  foreach(codec LIBDE265 KVAZAAR AOM_DECODER AOM_ENCODER)
    set(WITH_${codec} ON CACHE BOOL "" FORCE)
    set(WITH_${codec}_PLUGIN OFF CACHE BOOL "" FORCE)
  endforeach()
  foreach(flag ENABLE_PLUGIN_LOADING ENABLE_PARALLEL_TILE_DECODING WITH_EXAMPLES WITH_GDK_PIXBUF BUILD_DEVELOPMENT_TOOLS BUILD_DOCUMENTATION WITH_HEADER_COMPRESSION)
    set(${flag} OFF CACHE BOOL "" FORCE)
  endforeach()
  # Single codec worker keeps image memory estimates independent of CPU count.
  set(ENABLE_MULTITHREADING_SUPPORT OFF CACHE BOOL "" FORCE)
  add_subdirectory(${HEIF_SOURCES}/libheif heif EXCLUDE_FROM_ALL)
  target_include_directories(heif PRIVATE ${CMAKE_CURRENT_BINARY_DIR}/de265)
  # AOM adds _FILE_OFFSET_BITS=64 to CMake's shared release flags. Android's
  # 32-bit stdio replacements require API 24; the app supports API 21. Use
  # the platform's default file offsets in libheif's C++ stream implementation.
  # AN Paint itself passes bounded image buffers to libheif's memory API.
  if(ANDROID AND CMAKE_SIZEOF_VOID_P EQUAL 4 AND CMAKE_SYSTEM_VERSION LESS 24)
    target_compile_options(heif PRIVATE -U_FILE_OFFSET_BITS)
  endif()

  add_library(anpaint_heif SHARED ${CMAKE_CURRENT_LIST_DIR}/heif_bridge.cpp)
  target_include_directories(anpaint_heif PRIVATE ${HEIF_SOURCES}/libheif/libheif/api ${CMAKE_CURRENT_BINARY_DIR}/heif)
  target_include_directories(anpaint_heif PRIVATE ${CMAKE_CURRENT_LIST_DIR}/../../../build/jxl-source ${CMAKE_CURRENT_LIST_DIR}/../../../build/jxl-source/third_party/skcms)
  target_link_libraries(anpaint_heif PRIVATE heif jxl_cms jnigraphics log)
  target_link_options(anpaint_heif PRIVATE "-Wl,-z,max-page-size=16384")
endfunction()
anpaint_add_heif()
