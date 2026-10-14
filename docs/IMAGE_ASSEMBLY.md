# Image assembly

Add images, then use **Numeric layout** to arrange their numbered IDs:

```text
12
3
456
```

This places images 1 and 2 on the first row, image 3 on the second, and images
4, 5 and 6 on the third. Each row starts at the left edge; its tallest image
determines where the next row begins. Images keep their current crops and sizes.
**Restore original sizes** removes a previous Same width or Same height adjustment
without removing crops. PNG output uses the original assembled dimensions unless
you explicitly choose a smaller copy in the memory-budget dialog.

IDs follow import order, regardless of tray sorting. Removing an image renumbers
the remaining list. Use `[10]` through `[20]` for IDs above 9. Spaces add the selected
blank width, and empty lines add the selected empty-row height. Each ID can appear
once; omitted images are unplaced. Invalid layouts leave the assembly unchanged.

Select an image and use **Exact position** to set its top-left X/Y coordinates in
whole pixels, starting at zero. Other images stay where they are. The output canvas
expands to include placed images, and intentional overlap is allowed. Later imports
are drawn over earlier ones; transparent source pixels reveal earlier images over
an opaque white background. Edge snapping continues to reject overlapping drops.

Placement changes are undoable and saved with the assembly. Original input files
stay unchanged. New control captions and instructions currently use English fallback
where the selected language does not yet have translations.
