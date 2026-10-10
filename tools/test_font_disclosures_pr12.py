"""Keep custom UI font disclosures consistent with the bundle, including future fonts.

These are source/asset consistency checks, not a licence determination or a font
loader test. NativeCodecTest separately loads and hashes every inventoried font.
"""
import hashlib
import json
from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'Paintroid/src/main/assets'
LEGAL = ROOT / 'Paintroid/src/main/java/org/catrobat/paintroid/classic/LegalInfo.kt'
NOM_DISCLOSURE = (
    'AN Paint Nom UI is a renamed subset of Nom Na Tong (MIT) and Gothic Nguyen '
    '(SIL OFL 1.1), distributed under SIL OFL 1.1 with the original MIT notice retained.'
)
WU_DISCLOSURE = 'AN Paint Wu Fallback is a glyph-only subset of Nom Na Tong under MIT.'


def disclosure_errors(inventory, about, ci_section, asset_bytes):
    """Validate the current custom-family statements against actual declared files.

    Use injected bytes for fixtures so a future Wu bundle can be tested without
    adding a real font to production. No specific family is prohibited.
    """
    errors = []
    fonts = {row['name']: row for row in inventory if row['name'].startswith('AN Paint ')}
    paragraph = re.search(r'^\s*Fonts: (.+)$', about, re.MULTILINE)
    if paragraph is None:
        return ['About font paragraph missing']
    paragraph = paragraph.group(1)
    disclosed = set(re.findall(r'\b(AN Paint [A-Za-z][A-Za-z ]+?) is\b', paragraph))
    for name in sorted(disclosed - fonts.keys()):
        errors.append(f'{name}: disclosed without inventory entry')
    for name, row in fonts.items():
        if name not in disclosed:
            errors.append(f'{name}: inventory entry missing About disclosure')
        data = asset_bytes.get(row['asset'])
        if not data:
            errors.append(f'{name}: missing font asset')
        elif hashlib.sha256(data).hexdigest() != row['sha256']:
            errors.append(f'{name}: font hash mismatch')
        notice = asset_bytes.get(row['licence_file'], b'').decode('utf-8')
        if not notice.strip() or name not in notice:
            errors.append(f'{name}: missing corresponding notice')
        else:
            for aggregate in ('legal/FONT_NOTICES.txt', 'legal/THIRD_PARTY_NOTICES.txt'):
                text = asset_bytes.get(aggregate, b'').decode('utf-8')
                if notice.strip() not in text:
                    errors.append(f'{name}: notice absent from {aggregate}')
    if 'AN Paint Nom UI' in fonts and NOM_DISCLOSURE not in paragraph:
        errors.append('AN Paint Nom UI: source/licence summary changed')
    if 'AN Paint Wu Fallback' in fonts and WU_DISCLOSURE not in paragraph:
        errors.append('AN Paint Wu Fallback: source/licence summary missing')

    # The historical CI paragraph used a short name. It is valid only when that
    # inventoried family really has the UI-only role; a later bundle may add it.
    for alias, name in (('Nôm asset', 'AN Paint Nom UI'), ('Wu fallback', 'AN Paint Wu Fallback')):
        if alias.casefold() in ci_section.casefold():
            if name not in fonts or not fonts[name].get('ui_only'):
                errors.append(f'{name}: unsupported CI UI-only reference')
    return errors


class FontDisclosureTest(unittest.TestCase):
    def test_current_custom_font_disclosures_match_inventory_assets_and_notices(self):
        inventory = json.loads((ASSETS / 'fonts/inventory.json').read_text())
        paths = {'legal/FONT_NOTICES.txt', 'legal/THIRD_PARTY_NOTICES.txt'}
        for row in inventory:
            if row['name'].startswith('AN Paint '):
                paths.update((row['asset'], row['licence_file']))
        assets = {path: (ASSETS / path).read_bytes() for path in paths if (ASSETS / path).is_file()}
        ci = (ROOT / 'CI.md').read_text().split('## Locale UI font inventory check', 1)[1]
        self.assertEqual([], disclosure_errors(inventory, LEGAL.read_text(), ci, assets))

    def fixture(self, with_wu=False):
        inventory, assets, statements = [], {}, []
        for font_id, name, disclosure, licence in (
                ('anpaintnomui', 'AN Paint Nom UI', NOM_DISCLOSURE, 'OFL-1.1; MIT source notice retained'),
                *([('anpaintwuufallback', 'AN Paint Wu Fallback', WU_DISCLOSURE, 'MIT')] if with_wu else [])):
            # Deliberately not font bytes: this fixture exercises bundle metadata,
            # while real font validity remains covered by the Android font tests.
            data = f'hypothetical {name} fixture'.encode()
            path, notice_path = f'fonts/{font_id}.ttf', f'legal/fonts/{font_id}-NOTICE.txt'
            inventory.append(dict(id=font_id, name=name, asset=path, licence=licence,
                                  licence_file=notice_path, sha256=hashlib.sha256(data).hexdigest(),
                                  modified=True, ui_only=True))
            assets[path] = data
            assets[notice_path] = f'{name}: hypothetical fixture notice, {licence}.\n'.encode()
            statements.append(disclosure)
        notices = b'\n'.join(assets[row['licence_file']] for row in inventory)
        assets.update({'legal/FONT_NOTICES.txt': notices, 'legal/THIRD_PARTY_NOTICES.txt': notices})
        ci = 'The Nôm asset has the `ui_only` role.'
        if with_wu:
            ci += ' The Wu fallback also has the `ui_only` role.'
        return inventory, 'Fonts: ' + ' '.join(statements), ci, assets

    def test_nom_only_bundle_passes(self):
        self.assertEqual([], disclosure_errors(*self.fixture()))

    def test_hypothetical_wu_bundle_requires_and_accepts_its_disclosure(self):
        fixture = self.fixture(with_wu=True)
        self.assertEqual([], disclosure_errors(*fixture))
        inventory, about, ci, assets = fixture
        errors = disclosure_errors(inventory, about.replace(WU_DISCLOSURE, ''), ci, assets)
        self.assertIn('AN Paint Wu Fallback: inventory entry missing About disclosure', errors)

    def test_phantom_about_disclosure_is_rejected(self):
        inventory, about, ci, assets = self.fixture()
        self.assertIn('AN Paint Wu Fallback: disclosed without inventory entry',
                      disclosure_errors(inventory, about + ' ' + WU_DISCLOSURE, ci, assets))

    def test_phantom_ci_role_is_rejected(self):
        inventory, about, ci, assets = self.fixture()
        self.assertIn('AN Paint Wu Fallback: unsupported CI UI-only reference',
                      disclosure_errors(inventory, about, ci + ' The Wu fallback is UI-only.', assets))

    def test_hypothetical_wu_bundle_rejects_missing_or_changed_asset(self):
        for change in ('missing', 'changed'):
            with self.subTest(change=change):
                inventory, about, ci, assets = self.fixture(with_wu=True)
                path = inventory[-1]['asset']
                if change == 'missing':
                    del assets[path]
                else:
                    assets[path] += b'changed'
                expected = 'missing font asset' if change == 'missing' else 'font hash mismatch'
                self.assertIn('AN Paint Wu Fallback: ' + expected,
                              disclosure_errors(inventory, about, ci, assets))

    def test_hypothetical_wu_bundle_rejects_missing_or_unrelated_notice(self):
        for data in (b'', b'Notice for an unrelated font'):
            with self.subTest(notice=data):
                inventory, about, ci, assets = self.fixture(with_wu=True)
                assets[inventory[-1]['licence_file']] = data
                self.assertIn('AN Paint Wu Fallback: missing corresponding notice',
                              disclosure_errors(inventory, about, ci, assets))

    def test_hypothetical_wu_notice_must_reach_both_displayed_aggregates(self):
        for path in ('legal/FONT_NOTICES.txt', 'legal/THIRD_PARTY_NOTICES.txt'):
            with self.subTest(aggregate=path):
                inventory, about, ci, assets = self.fixture(with_wu=True)
                assets[path] = assets[inventory[0]['licence_file']]
                self.assertIn('AN Paint Wu Fallback: notice absent from ' + path,
                              disclosure_errors(inventory, about, ci, assets))

    def test_hypothetical_wu_ci_role_must_match_inventory(self):
        inventory, about, ci, assets = self.fixture(with_wu=True)
        inventory[-1]['ui_only'] = False
        self.assertIn('AN Paint Wu Fallback: unsupported CI UI-only reference',
                      disclosure_errors(inventory, about, ci, assets))

    def test_nom_source_and_licence_summary_is_preserved(self):
        inventory, about, ci, assets = self.fixture()
        about = about.replace('with the original MIT notice retained', 'without source notices')
        self.assertIn('AN Paint Nom UI: source/licence summary changed',
                      disclosure_errors(inventory, about, ci, assets))

    def test_hypothetical_wu_source_and_licence_summary_is_preserved(self):
        inventory, about, ci, assets = self.fixture(with_wu=True)
        about = about.replace('a glyph-only subset of Nom Na Tong under MIT',
                              'an unrelated font under different terms')
        self.assertIn('AN Paint Wu Fallback: source/licence summary missing',
                      disclosure_errors(inventory, about, ci, assets))


if __name__ == '__main__':
    unittest.main()
