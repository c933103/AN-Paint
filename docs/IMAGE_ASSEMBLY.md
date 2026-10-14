# Image assembly

Add images, then hold a thumbnail and drag it into the workspace. Drop at a
highlighted edge to attach it to the right or bottom of another image. Drag placed
images to rearrange them. Attachments can form rows with different image counts.

Select an image and use **Exact position** to set its top-left X/Y coordinates in
whole pixels, starting at zero. Other images stay where they are. The output canvas
expands to include placed images, and intentional overlap is allowed. Later imports
are drawn over earlier ones; transparent source pixels reveal earlier images over
an opaque white background. Edge snapping continues to reject overlapping drops.

Placement changes are undoable and saved with the assembly. Original input files
stay unchanged. Images keep their original cropped dimensions unless you choose
**Same width** or **Same height**. **Restore original sizes** in either size dialog
removes normalization without removing crops. PNG output uses the assembled
dimensions unless you explicitly choose a smaller copy in the memory-budget dialog.

The new position-control captions and instructions currently use English fallback
where the selected language does not yet have translations.
