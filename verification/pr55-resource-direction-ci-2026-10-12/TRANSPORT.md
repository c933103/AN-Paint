# Lossless replay transport

The unchanged 18,791,932-byte regression replay ZIP is stored in three ordered parts solely to fit the publication transport limit. Run `python3 reconstruct_replay.py` in this directory before the frozen README replay instructions. The script verifies the frozen delivery manifest, every part, and the exact reconstructed original ZIP hash; it refuses to replace a differing existing file.

The original independent DELIVERY-FILES.json and all its other files remain unchanged. This checkpoint preserves the exact failed da4 run (902/906 JVM passes, four assertions failed), alongside successful 95/95 and 104/104 installed gates. It is not a successor pass claim. No APK or full source ZIP is duplicated here.
