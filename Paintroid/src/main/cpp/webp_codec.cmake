# AN Paint codec integration, 2026-09-12. AGPL-3.0-or-later.
# libwebp source is pinned by tools/fetch_webp_sources.py.
foreach(feature ANIM_UTILS CWEBP DWEBP GIF2WEBP IMG2WEBP VWEBP WEBPINFO LIBWEBPMUX WEBPMUX EXTRAS WEBP_JS FUZZTEST)
  set(WEBP_BUILD_${feature} OFF CACHE BOOL "" FORCE)
endforeach()
set(WEBP_LINK_STATIC ON CACHE BOOL "" FORCE)
# All encoder allocations remain on the calling thread and share its budget.
set(WEBP_USE_THREAD OFF CACHE BOOL "" FORCE)
add_subdirectory(${CMAKE_CURRENT_LIST_DIR}/../../../build/webp-source webp EXCLUDE_FROM_ALL)
foreach(target webpdecode webpdspdecode webputilsdecode webpencode webpdsp webputils sharpyuv)
  target_compile_definitions(${target} PRIVATE
    malloc=AnPaintWebpMalloc calloc=AnPaintWebpCalloc
    realloc=AnPaintWebpRealloc free=AnPaintWebpFree)
endforeach()
add_library(anpaint_webp SHARED webp_bridge.cpp)
target_link_libraries(anpaint_webp PRIVATE webp jnigraphics)
target_link_options(anpaint_webp PRIVATE "-Wl,-z,max-page-size=16384")
