import unittest
from publish_github_release import verify_jobs


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
