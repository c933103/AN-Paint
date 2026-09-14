import io
import unittest
import zipfile
from apk_release_patch import apply, create


def apk(signature, payload=b"unchanged app code" * 10000):
    stream = io.BytesIO()
    with zipfile.ZipFile(stream, "w") as archive:
        archive.writestr("META-INF/CERT.RSA", signature)
        archive.writestr("classes.dex", payload)
        archive.writestr("assets/source.zip", b"corresponding source" * 10000)
    return stream.getvalue()


class ReleasePatchTest(unittest.TestCase):
    def test_signing_size_and_offset_changes_preserve_exact_apk(self):
        before, after = apk(b"CI signature"), apk(b"public final signature" * 100)
        patch = create(before, after)
        self.assertEqual(after, apply(before, patch))
        self.assertLess(len(str(patch)), len(after) // 10)

    def test_changed_payload_or_wrong_original_is_rejected(self):
        before, after = apk(b"CI"), apk(b"final")
        with self.assertRaisesRegex(ValueError, "payload"):
            create(before, apk(b"final", b"changed code"))
        with self.assertRaisesRegex(ValueError, "original"):
            apply(apk(b"another build"), create(before, after))

    def test_corrupt_public_signature_bytes_are_rejected(self):
        before, after = apk(b"CI"), apk(b"final")
        patch = create(before, after)
        patch["output_sha256"] = "0" * 64
        with self.assertRaisesRegex(ValueError, "hash mismatch"):
            apply(before, patch)
