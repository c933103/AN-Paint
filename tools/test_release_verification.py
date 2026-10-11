import unittest
from publish_github_release import CERT, verify_jobs, verify_signer_identity


class ReleaseVerificationTest(unittest.TestCase):
    def setUp(self):
        self.workflow = {"head_sha": "a" * 40, "conclusion": "success", "event": "push",
                         "path": ".github/workflows/android.yml", "head_branch": "develop"}
        self.jobs = [{"name": name, "status": "completed", "conclusion": "success"} for name in
                     ("Regression tests and lint", "Build APK and corresponding source", "Emulator API 30", "Emulator API 35")]

    def test_completed_full_release_is_accepted(self):
        verify_jobs(self.workflow, self.jobs, "a" * 40)

    def test_pending_failed_missing_or_wrong_commit_cannot_publish(self):
        for status in ("failure", "skipped", None):
            jobs = [dict(job) for job in self.jobs]
            jobs[-1]["conclusion"] = status
            with self.assertRaises(ValueError):
                verify_jobs(self.workflow, jobs, "a" * 40)
        with self.assertRaises(ValueError):
            verify_jobs(self.workflow, self.jobs[1:], "a" * 40)
        with self.assertRaises(ValueError):
            verify_jobs(self.workflow, self.jobs, "b" * 40)


class ReleaseSignerVerificationTest(unittest.TestCase):
    def output(self, digest=CERT, count=1, extra=""):
        return ("Verifies\n"
                "Verified using v1 scheme (JAR signing): true\n"
                "Verified using v2 scheme (APK Signature Scheme v2): true\n"
                "Verified using v3 scheme (APK Signature Scheme v3): true\n"
                f"Number of signers: {count}\n"
                "Signer #1 certificate DN: CN=Existing release identity\n"
                f"Signer #1 certificate SHA-256 digest: {digest}\n" + extra)

    def test_single_existing_signer_is_accepted(self):
        verify_signer_identity(self.output())
        verify_signer_identity(self.output(digest=CERT.upper()))
        verify_signer_identity(self.output().replace("\n", "\r\n"))

    def test_other_signer_is_rejected_even_if_expected_digest_is_displayed_elsewhere(self):
        for extra in (f"Signer #1 certificate DN: CN={CERT}\n",
                      f"Source Stamp Signer certificate SHA-256 digest: {CERT}\n",
                      f"Signer #1 public key SHA-256 digest: {CERT}\n"):
            with self.subTest(extra=extra), self.assertRaises(ValueError):
                verify_signer_identity(self.output(digest="0" * 64, extra=extra))

    def test_multiple_duplicate_or_unexpected_signer_identities_are_rejected(self):
        outputs = [
            self.output(count=2, extra=f"Signer #2 certificate SHA-256 digest: {'0' * 64}\n"),
            self.output(extra=f"Signer #1 certificate SHA-256 digest: {CERT}\n"),
            self.output(extra="Signer #2 certificate SHA-256 digest: malformed\n"),
            self.output().replace("Signer #1 certificate SHA-256", "Signer #2 certificate SHA-256"),
        ]
        for output in outputs:
            with self.subTest(output=output), self.assertRaises(ValueError):
                verify_signer_identity(output)

    def test_missing_or_malformed_signer_digest_is_rejected(self):
        for digest in ("", CERT[:-1], CERT + "0", "g" * 64, CERT + " unrelated"):
            with self.subTest(digest=digest), self.assertRaises(ValueError):
                verify_signer_identity(self.output(digest=digest))
        with self.assertRaises(ValueError):
            verify_signer_identity(self.output().replace(
                f"Signer #1 certificate SHA-256 digest: {CERT}\n", ""))

    def test_missing_duplicate_or_invalid_signer_count_is_rejected(self):
        outputs = [self.output(count=n) for n in (0, 2, "unknown")]
        outputs += [self.output().replace("Number of signers: 1\n", ""),
                    self.output(extra="Number of signers: 1\n")]
        for output in outputs:
            with self.subTest(output=output), self.assertRaises(ValueError):
                verify_signer_identity(output)
