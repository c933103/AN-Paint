"""Content-based parse reuse must not change fresh binding or mutation behavior."""
import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch
import current_localization_contracts as c


class ResidualParseReuseTests(unittest.TestCase):
    def test_result_rows_and_attributes_never_alias_the_cached_oracle(self):
        first=c.residual_rows(); identity=next(iter(first)); original=dict(first[identity])
        first[identity]['target']='forged'
        first[identity]['attributes']['name']='forged'
        second=c.residual_rows()
        self.assertNotEqual('forged',second[identity]['target'])
        self.assertEqual(identity[1],second[identity]['attributes']['name'])
        self.assertIsNot(first[identity],second[identity])
        self.assertIsNot(first[identity]['attributes'],second[identity]['attributes'])

    def test_changed_content_is_observed_even_when_size_and_mtime_are_restored(self):
        text=(c.FIXTURES/'reviewed_residuals_20261030.json').read_text()
        with TemporaryDirectory() as folder:
            path=Path(folder)/'reviewed_residuals_20261030.json';path.write_text(text)
            with patch.object(c,'FIXTURES',Path(folder)):
                baseline=c.residual_rows();identity=next(iter(baseline));target=baseline[identity]['target']
                old=path.stat();changed=text.replace(target,target[:-1]+('x' if target[-1]!='x' else 'y'),1)
                self.assertEqual(len(changed.encode()),len(text.encode()));path.write_text(changed)
                import os
                os.utime(path,ns=(old.st_atime_ns,old.st_mtime_ns))
                self.assertNotEqual(target,c.residual_rows()[identity]['target'])
                path.write_text(text)
                self.assertEqual(target,c.residual_rows()[identity]['target'])
                path.write_text(text.replace('"schema_version": 1,','"schema_version": 1, "schema_version": 1,',1))
                with self.assertRaisesRegex(ValueError,'Duplicate fixture key'):c.residual_rows()

    def test_mocked_loader_and_malformed_rows_are_not_hidden_by_cache(self):
        c.residual_rows()
        data=c.fixture('reviewed_residuals_20261030.json')
        original=data['decisions'][0]['target'];data['decisions'][0]['target']='mocked target'
        with patch.object(c,'fixture',return_value=data) as mocked:
            self.assertEqual('mocked target',next(iter(c.residual_rows().values()))['target'])
            mocked.assert_called_once_with('reviewed_residuals_20261030.json')
        self.assertEqual(original,next(iter(c.residual_rows().values()))['target'])
        for field,value in [('target',{}),('attributes',{'name':[]}),('review',[]),('extra',{})]:
            bad=c.fixture('reviewed_residuals_20261030.json');bad['decisions'][0][field]=value
            with patch.object(c,'fixture',return_value=bad),self.assertRaises(ValueError):c.residual_rows()


if __name__=='__main__':unittest.main()
