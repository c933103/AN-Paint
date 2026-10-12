#!/usr/bin/env bash
# Portable host-only replay. Does not compile Android or execute its tests.
set -euo pipefail
if [ "$#" -ne 5 ]; then echo "Usage: $0 REPO ACCEPTED_VALUES FROZEN_PARTIAL FULL_SOURCE_FONT OUTPUT" >&2; exit 2; fi
repo=$(realpath "$1"); accepted=$(realpath "$2"); frozen=$(realpath "$3"); font=$(realpath "$4"); output=$(realpath -m "$5")
scripts=$(cd -- "$(dirname -- "$0")" && pwd)
mkdir -p "$output"
python "$scripts/audit_scope.py" --repo "$repo" --accepted "$accepted" --frozen "$frozen" --output "$output"
python "$scripts/audit_controls.py" --repo "$repo" --accepted "$accepted" --frozen "$frozen" --output "$output"
python "$scripts/audit_font.py" --repo "$repo" --source "$font" --output "$output"
cd "$repo"
python tools/extend_nom_m04_ui_font.py "$font" "$output/baseline-m03.ttf" "$output/rebuilt-m04.ttf" > "$output/font-rebuild.json"
cmp Paintroid/src/main/assets/fonts/anpaintnomui.ttf "$output/rebuilt-m04.ttf"
python tools/verify_nom_m04_renderer.py "$font" "$output/raster" > "$output/font-raster.log"
python tools/translation_catalogues.py > "$output/catalogue-structure.log" 2>&1
PYTHONPATH=tools python -m unittest -v test_commons_metadata_m04 test_commons_metadata_m04_font test_commons_metadata_m03 test_commons_metadata_m03_font test_locale_font_coverage test_commons_copy_credit_errors test_svg_error_translations test_tiff_c023_wording > "$output/focused-contracts.log" 2>&1
PYTHONPATH=tools python -m unittest -v test_translations > "$output/translation-contracts.log" 2>&1
git diff --check
python -m py_compile tools/commons_metadata_m04_scope.py tools/commons_metadata_m04_font_scope.py tools/test_commons_metadata_m04.py tools/test_commons_metadata_m04_font.py tools/extend_nom_m04_ui_font.py tools/verify_nom_m04_renderer.py
printf 'Host checks passed; actual raster image inspection and Android verification remain separate.\n'
