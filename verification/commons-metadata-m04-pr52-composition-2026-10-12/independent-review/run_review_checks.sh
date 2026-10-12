#!/usr/bin/env bash
# Host-only replay, ordinary Python required for the independent assertion-based audit.
set -euo pipefail
if [ "$#" -ne 4 ]; then echo "Usage: $0 COMPOSED_REPO M04_CHECKPOINT_REPO FULL_SOURCE_FONT OUTPUT" >&2; exit 2; fi
repo=$(realpath "$1"); m04=$(realpath "$2"); font=$(realpath "$3"); output=$(realpath -m "$4")
scripts=$(cd -- "$(dirname -- "$0")" && pwd); mkdir -p "$output"
python "$scripts/audit_composition.py" --repo "$repo" --m04-repo "$m04" --output "$output"
python "$scripts/audit_font.py" --repo "$repo" --source "$font" --output "$output"
cd "$repo"
python tools/extend_nom_m04_ui_font.py "$font" "$output/baseline-m03.ttf" "$output/rebuilt-m04.ttf" > "$output/font-rebuild.json"
cmp Paintroid/src/main/assets/fonts/anpaintnomui.ttf "$output/rebuilt-m04.ttf"
python tools/verify_nom_m04_renderer.py "$font" "$output/raster" > "$output/font-raster.log"
PYTHONPATH=tools python -m unittest -v test_commons_metadata_m04_composition test_commons_metadata_m04 test_commons_metadata_m04_font test_commons_metadata_m02 test_commons_metadata_m03 test_commons_metadata_m03_font test_commons_metadata_composition test_hungarian_attribution_c05 test_localized_dialog_composition test_commons_copy_credit_errors test_svg_error_translations test_tiff_c023_wording test_locale_font_coverage > "$output/independent-focused.log" 2>&1
PYTHONPATH=tools python -m unittest -v test_translations > "$output/translation-contracts.log" 2>&1
python tools/translation_catalogues.py > "$output/catalogue-structure.log" 2>&1
git diff --check 71f4d288669858e7975ec4c094b7f47a9a1ff145
printf 'Host checks pass; image inspection and Android verification remain separate.\n'
