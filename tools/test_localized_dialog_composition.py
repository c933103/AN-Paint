"""Current source-derived installed phase union and operational deadlines."""
from pathlib import Path
import unittest
from app_instrumentation_matrix import app_partition, PHASE_TIMEOUTS
from run_android_instrumentation import declared_tests, RESTART_SEED, RESTART_VERIFY
ROOT=Path(__file__).resolve().parents[1]

class InstalledPhaseContracts(unittest.TestCase):
    def test_phase_union_is_disjoint_and_covers_current_sdk_eligible_source(self):
        for sdk in (30,35):
            with self.subTest(sdk=sdk):
                eligible=declared_tests(ROOT/'app/src/androidTest',sdk_level=sdk)
                parts=app_partition(eligible,sdk)
                scheduled=set().union(*parts.values())
                excluded={item for item in eligible if sdk<35 and item[0] in (RESTART_SEED,RESTART_VERIFY)}
                self.assertEqual(eligible-excluded,scheduled)
                self.assertEqual(len(scheduled),sum(map(len,parts.values())))
                self.assertTrue(all(parts.values()))
                self.assertTrue(declared_tests(ROOT/'Paintroid/src/androidTest',sdk_level=sdk))
                self.assertFalse(scheduled & (declared_tests(ROOT/'app/src/androidTest')-eligible))

    def test_new_ordinary_methods_join_the_schedule_without_a_historical_count_update(self):
        future=('paint.anpaint.android.FutureBehaviorTest','checksNewBehavior')
        for sdk in (30,35):
            eligible=declared_tests(ROOT/'app/src/androidTest',sdk_level=sdk)
            self.assertNotIn(future,eligible)
            before=app_partition(eligible,sdk)
            after=app_partition(eligible|{future},sdk)
            self.assertEqual(before['ordinary']|{future},after['ordinary'])
            self.assertEqual(set().union(*before.values())|{future},set().union(*after.values()))

    def test_current_operational_phase_deadlines(self):
        self.assertEqual({'ordinary':180,'gallery-draft':90,'dialog':300,
            'vertical-english-manchu':180,'vertical-literary-chinese-emoji':180,
            'seed':60,'verify':60},PHASE_TIMEOUTS)
