"""Protect personal notes and prevent misleading progress totals."""
from datetime import date, timedelta
import importlib.util
import re
import shutil
from pathlib import Path
import tempfile
import unittest

SOURCE = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('study', SOURCE / 'scripts/study.py')
study = importlib.util.module_from_spec(spec)
spec.loader.exec_module(study)


class StudyTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / 'repo'
        shutil.copytree(SOURCE, self.root, ignore=shutil.ignore_patterns(
            '.git', '__pycache__', '.venv', 'venv', 'data', 'datasets',
            'checkpoints', 'outputs', 'wandb', 'runs'))
        # Reset only the temporary fixture, so future real study progress
        # does not break these tests or get modified by them.
        for path in (self.root / 'logs').glob('????-??-??.md'):
            path.unlink()
        for path in (self.root / 'weeks').glob('W*.md'):
            text = path.read_text(encoding='utf-8')
            path.write_text(re.sub(r'^- \[[xX]\]', '- [ ]', text, flags=re.M), encoding='utf-8')

    def test_daily_never_overwrites_notes(self):
        day = date(2026, 9, 21)
        path, created = study.create_daily(self.root, day)
        self.assertTrue(created)
        original = path.read_text(encoding='utf-8') + '\n我的重要笔记\n'
        path.write_text(original, encoding='utf-8')
        self.assertFalse(study.create_daily(self.root, day)[1])
        self.assertEqual(path.read_text(encoding='utf-8'), original)

    def test_actual_minutes_and_future_exclusion(self):
        today = date.today()
        path, _ = study.create_daily(self.root, today)
        path.write_text(path.read_text(encoding='utf-8').replace('minutes: 0', 'minutes: 75').replace('completed: false', 'completed: true'), encoding='utf-8')
        future, _ = study.create_daily(self.root, today + timedelta(days=1))
        future.write_text(future.read_text(encoding='utf-8').replace('minutes: 0', 'minutes: 120').replace('completed: false', 'completed: true'), encoding='utf-8')
        text = study.dashboard(self.root).read_text(encoding='utf-8')
        self.assertIn('实际学习：1.2 h', text)
        self.assertIn('完成打卡：1 天', text)
        self.assertIn('未来日期日志 1 份', text)

    def test_blank_does_not_count_and_checks_separate(self):
        study.create_daily(self.root, date.today())
        path = self.root / 'weeks/W01.md'
        text = path.read_text(encoding='utf-8')
        text = text.replace('- [ ]', '- [x]', 3)
        path.write_text(text, encoding='utf-8')
        output = study.dashboard(self.root).read_text(encoding='utf-8')
        self.assertIn('必做任务：3/39', output)
        self.assertIn('验收项：0/26', output)
        self.assertIn('完成打卡：0 天', output)
        self.assertIn('| 待验收 |', output)

    def test_invalid_minutes_rejected(self):
        path, _ = study.create_daily(self.root, date.today())
        path.write_text(path.read_text(encoding='utf-8').replace('minutes: 0', 'minutes: -2'), encoding='utf-8')
        with self.assertRaises(ValueError):
            study.read_logs(self.root)

    def test_broken_link_is_reported(self):
        study.dashboard(self.root)
        self.assertEqual(study.check(self.root), [])
        (self.root / 'notes/broken.md').write_text('[bad](missing.md)', encoding='utf-8')
        self.assertTrue(any('missing.md' in x for x in study.check(self.root)))

    def test_week_date_boundaries(self):
        self.assertIsNone(study.for_date(self.root, date(2026, 9, 20)))
        self.assertEqual(study.for_date(self.root, date(2026, 9, 21))['week'], 1)
        self.assertEqual(study.for_date(self.root, date(2026, 12, 20))['week'], 13)
        self.assertIsNone(study.for_date(self.root, date(2026, 12, 21)))


if __name__ == '__main__':
    unittest.main()
