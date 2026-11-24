"""Detail-loss modality and original ownership; linguistic review remains open."""
import unittest
from current_localization_contracts import current_display

KEY = 'ui_sampled_resize_memory_explanation'

class SampledMemoryModalityTests(unittest.TestCase):
    def test_definite_detail_loss_preserves_variable_actual_usage_and_original(self):
        bo = current_display('bo', KEY)
        self.assertIn('ཞིབ་ཆ་ཉམས།', bo)
        self.assertNotIn('ཞིབ་ཆ་ཉམས་སྲིད།', bo)
        self.assertIn('ཚད་མི་འདྲ་བ་', bo)
        # Guard original-file identity and no-change polarity separately.
        original = next(part for part in bo.split('།') if 'མ་རིས་ཀྱི་ཡིག་ཆ་' in part)
        self.assertIn('མི་བསྒྱུར', original)
        self.assertNotIn('སྲིད', original)
        jje = current_display('jje', KEY)
        # This statement is definite, unlike the actual-memory sentence.
        loss = next(part for part in jje.split('.') if '작은 사본' in part)
        self.assertRegex(loss, r'세밀헌 부분.{0,10}(?:덜 남|줄어들)')
        self.assertNotRegex(loss, r'(?:남을|줄어들)\s*수')
        self.assertNotRegex(loss, r'덜 남지|줄어들지|안 줄어')
        self.assertIn('다를 수', jje)
        self.assertIn('원본 파일은 그대로', jje)

if __name__ == '__main__': unittest.main()
