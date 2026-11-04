"""Phase-one acceptance tests: deterministic, offline and never executable."""
import copy
import csv
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location('nl_request', ROOT/'tooling/nl_request.py')
nl = importlib.util.module_from_spec(spec)
spec.loader.exec_module(nl)


class NaturalLanguageTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.parser = nl.Parser(ROOT)

    def intent(self, sentence):
        return self.parser.parse(sentence)['intents'][0]

    def fixture(self, followers='mold_cut_depth:+1'):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        repo = Path(temp.name)
        for path in self.parser.hashes:
            dest = repo/path
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT/path, dest)
        path = repo/nl.TABLE
        rows = nl.read_csv(path)
        for row in rows:
            row['followers'] = followers if row['logical_name'] == 'die_thickness' else ''
        with path.open('w', encoding='utf-8', newline='') as stream:
            writer = csv.DictWriter(stream, fieldnames=list(rows[0]), lineterminator='\n')
            writer.writeheader()
            writer.writerows(rows)
        return repo

    def test_absolute_and_explicit_default(self):
        intent = self.intent('把芯片厚度改成 0.45')
        self.assertEqual(intent['value'], {'number': .45, 'unit': 'mm'})
        self.assertEqual(intent['entity'], 'ENT-BGA-BODY-25')
        self.assertIn('未写单位，按 mm', intent['assumptions'])

    def test_relative_with_table_followers(self):
        report = nl.Parser(self.fixture()).parse('芯片厚度加 0.1，塑封跟着变')
        intent = report['intents'][0]
        self.assertEqual(intent['operation'], 'relative')
        self.assertEqual(intent['value']['number'], .45)
        self.assertEqual(intent['delta'], .1)
        self.assertEqual(intent['followers'], ['mold_cut_depth'])
        self.assertEqual(intent['follower_previews'][0]['value']['number'], .5)
        self.assertFalse(any('U-PARAM-AMBIGUOUS' in u for u in report['unresolved']))

    def test_real_table_missing_followers_is_not_invented(self):
        report = self.parser.parse('芯片厚度加 0.1，塑封跟着变')
        self.assertEqual(report['intents'][0]['followers'], [])
        self.assertTrue(any('U-FOLLOWERS-UNAVAILABLE' in u for u in report['unresolved']))

    def test_longest_alias(self):
        self.assertEqual(self.intent('把塑封内腔深度改成 0.5')['parameter'], 'mold_cut_depth')

    def test_bare_chip_is_ambiguous(self):
        report = self.parser.parse('把芯片改成 0.5')
        self.assertFalse(report['intents'])
        self.assertTrue(any('U-PARAM-AMBIGUOUS' in u for u in report['unresolved']))

    def test_unknown_parameter(self):
        self.assertIn('U-PARAM-UNKNOWN', self.parser.parse('把温度改成 100')['unresolved'][0])

    def test_micrometers(self):
        for unit in ['微米', 'um', 'µm', 'μm']:
            with self.subTest(unit=unit):
                intent = self.intent('芯片厚度改成450 '+unit)
                self.assertEqual(intent['value']['number'], .45)
                self.assertTrue(any('换算' in s for s in intent['assumptions']))

    def test_generic_thickness_is_ambiguous(self):
        report = self.parser.parse('把厚度改成0.5')
        self.assertIn('U-PARAM-AMBIGUOUS', report['unresolved'][0])

    def test_nonpositive_value_rejected(self):
        for value in ['-1', '0']:
            with self.assertRaises(ValueError):
                self.parser.parse('芯片厚度改成'+value)

    def test_stable_reproducible_id_and_output(self):
        sentence = '芯片厚度改成0.45'
        self.assertEqual(self.parser.parse(sentence), self.parser.parse(sentence))

    def test_empty(self):
        with self.assertRaises(ValueError):
            self.parser.parse('  ')

    def test_multiple_targets(self):
        report = self.parser.parse('芯片厚度改成0.4 mm，焊球直径改成0.32')
        self.assertEqual([i['parameter'] for i in report['intents']], ['die_thickness', 'ball_diameter'])
        self.assertEqual([i['value']['number'] for i in report['intents']], [.4, .32])

    def test_unknown_bump_height_is_not_a_diameter(self):
        report = self.parser.parse('把凸点高度改小0.01')
        self.assertFalse(report['intents'])
        self.assertIn('U-PARAM-UNKNOWN', report['unresolved'][0])

    def test_relative_decrease(self):
        intent = self.intent('把芯片厚度改小0.01')
        self.assertEqual(intent['value']['number'], .34)
        self.assertEqual(intent['delta'], -.01)

    def test_relative_cannot_become_negative(self):
        with self.assertRaises(ValueError):
            self.parser.parse('芯片厚度减小1')

    def test_negation(self):
        report = self.parser.parse('不要把芯片厚度改成0.5')
        self.assertFalse(report['intents'])
        self.assertIn('U-NEGATION', report['unresolved'][0])

    def test_incompatible_units(self):
        with self.assertRaises(ValueError):
            self.parser.parse('芯片厚度改成30度')

    def test_multiple_numbers_are_not_silently_truncated(self):
        report = self.parser.parse('芯片厚度改成0.4到0.5')
        self.assertFalse(report['intents'])
        self.assertIn('U-UNSUPPORTED-EXPRESSION', report['unresolved'][0])

    def test_duplicate_target_is_conflict(self):
        report = self.parser.parse('芯片厚度改成0.4，芯片厚度改成0.5')
        self.assertTrue(any('U-CONFLICT' in u for u in report['unresolved']))

    def test_primary_follower_conflict(self):
        report = nl.Parser(self.fixture()).parse('芯片厚度加0.1，塑封跟着变，塑封内腔改成0.6')
        self.assertTrue(any('U-CONFLICT' in u for u in report['unresolved']))

    def test_runtime_registry_is_still_unresolved(self):
        report = self.parser.parse('芯片厚度改成0.45')
        self.assertEqual(report['status'], 'blocked')
        self.assertEqual(report['contract_requests'], [])
        self.assertTrue(any('U-ENTITY-RUNTIME' in u for u in report['unresolved']))
        self.assertTrue(any('U-CONTRACT-GEOMETRY' in u for u in report['unresolved']))

    def test_case_scope_cannot_silently_change(self):
        report = self.parser.parse('芯片厚度改成0.45')
        self.assertEqual(report['case_id'], 'bga-2024r2-unsolved')
        report['case_id'] = 'new-three-layer-model'
        with self.assertRaises(ValueError):
            nl.validate_report(report, self.parser.schema)

    def test_stale_or_invalid_alias_rejected(self):
        repo = self.fixture()
        p = repo/'tooling/nl_aliases.csv'
        p.write_text(p.read_text(encoding='utf-8')+'不存在,missing,missing.SLDPRT\n', encoding='utf-8')
        with self.assertRaises(ValueError):
            nl.Parser(repo)

    def test_invalid_entity_map_rejected(self):
        repo = self.fixture()
        p = repo/'tooling/nl_entity_map.csv'
        p.write_text(p.read_text(encoding='utf-8').replace('ENT-BGA-BODY-25', 'UNKNOWN'), encoding='utf-8')
        with self.assertRaises(ValueError):
            nl.Parser(repo)

    def test_recursive_follower_rejected(self):
        with self.assertRaises(ValueError):
            nl.Parser(self.fixture('die_thickness:+1')).parse('芯片厚度加0.1，塑封跟着变')

    def test_unknown_named_follower_is_not_accepted(self):
        report = nl.Parser(self.fixture()).parse('芯片厚度加0.1，外壳跟着变')
        self.assertTrue(any('U-FOLLOWER-UNKNOWN' in u for u in report['unresolved']))

    def test_snapshot_changes_fingerprint_not_sentence_id(self):
        first = nl.Parser(self.fixture()).parse('芯片厚度加0.1')
        second = nl.Parser(self.fixture('mold_cut_depth:+2')).parse('芯片厚度加0.1')
        self.assertEqual(first['request_id'], second['request_id'])
        self.assertNotEqual(first['input_fingerprint'], second['input_fingerprint'])

    def test_corrupt_csv_is_rejected(self):
        repo = self.fixture()
        with (repo/'tooling/nl_aliases.csv').open('a', encoding='utf-8') as stream:
            stream.write('broken,only-two-fields\n')
        with self.assertRaises(ValueError):
            nl.Parser(repo)

    def test_failed_primary_does_not_attach_followers_to_previous_intent(self):
        report = nl.Parser(self.fixture()).parse('芯片厚度改成0.4，温度改成100，塑封跟着变')
        self.assertEqual(report['intents'][0]['followers'], [])
        self.assertTrue(any('U-FOLLOWER-WITHOUT-PRIMARY' in u for u in report['unresolved']))

    def test_multiple_follow_clauses_are_not_silently_overwritten(self):
        report = nl.Parser(self.fixture()).parse('芯片厚度改成0.4，塑封内腔跟着变，底填同步')
        self.assertTrue(any('U-CONFLICT' in u for u in report['unresolved']))

    def test_missing_jsonschema_cannot_accept_contract_requests(self):
        report = self.parser.parse('芯片厚度改成0.45')
        report['contract_requests'] = [{}]
        with patch.dict(sys.modules, {'jsonschema': None}):
            with self.assertRaisesRegex(ValueError, 'jsonschema is required'):
                nl.validate_report(report, self.parser.schema)

    def test_no_contract_validation_is_skipped(self):
        report = self.parser.parse('芯片厚度改成0.45')
        report['contract_requests'] = [{'tool': 'fake'}]
        with self.assertRaises(Exception):
            nl.validate_report(report, self.parser.schema)

    def test_intent_validation_runs_without_asserts(self):
        report = self.parser.parse('芯片厚度改成0.45')
        report['intents'][0]['value']['number'] = -1
        with self.assertRaises(ValueError):
            nl.validate_report(report, self.parser.schema)

    def test_cli_exit_codes_and_stdout(self):
        for sentence, code in [('芯片厚度改成0.45', 0), ('把温度改成100', 0), ('芯片厚度改成-1', 2), ('', 2)]:
            run = subprocess.run([sys.executable, str(ROOT/'tooling/nl_request.py'), sentence], capture_output=True, encoding='utf-8')
            self.assertEqual(run.returncode, code, run.stderr)
            if code == 0:
                self.assertIsInstance(json.loads(run.stdout), dict)
                self.assertEqual(run.stderr, '')
            else:
                self.assertEqual(run.stdout, '')
                self.assertIn('Validation error', run.stderr)

    def test_stdin_matches_cli(self):
        run = subprocess.run([sys.executable, str(ROOT/'tooling/nl_request.py'), '--stdin'], input='芯片厚度改成0.45\n', capture_output=True, encoding='utf-8')
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertEqual(json.loads(run.stdout), self.parser.parse('芯片厚度改成0.45'))


if __name__ == '__main__':
    unittest.main()
