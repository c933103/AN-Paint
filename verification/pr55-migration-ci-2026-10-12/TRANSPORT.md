# Lossless replay ZIP transport

The frozen review and its original DELIVERY-FILES.json are unchanged. The connector cannot submit this18.8MB ZIP as one base64 request because its request-body cap is16MiB. Only regression-replay-inputs.zip is represented by three ordered parts under parts/.

Run python3 reconstruct_replay.py from this directory, then use replay_regression.py as documented by the independent review. The reconstruction verifies every part and the complete ZIP against both TRANSPORT.json and the original frozen DELIVERY-FILES.json. It refuses to replace an existing different ZIP. The original review remains a failed overall checkpoint because API30 has one failed test.

No APK or source ZIP is duplicated. This transport adaptation changes no source, image pixel, result or acceptance criterion.
