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
        self.assertIn('མ་ཡིག་མི་བསྒྱུར།', bo)
        jje = current_display('jje', KEY)
        self.assertIn('줄어들어', jje)
        self.assertNotIn('줄어들 수', jje)
        self.assertIn('다를 수', jje)
        self.assertIn('원본 파일은 그대로', jje)

if __name__ == '__main__': unittest.main()
