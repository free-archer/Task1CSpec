import contextlib
import importlib.util
import io
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TASK1CSPEC_PATH = ROOT / ".task1cspec" / "scripts" / "task1cspec.py"
SPEC = importlib.util.spec_from_file_location("task1cspec", TASK1CSPEC_PATH)
assert SPEC is not None
task1cspec = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
sys.modules[SPEC.name] = task1cspec
SPEC.loader.exec_module(task1cspec)


def run_cli(args: list[str]) -> int:
    with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
        return task1cspec.main(args)


class Task1CSpecTests(unittest.TestCase):
    def test_start_creates_project_layout_and_task(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)

            code = run_cli(
                [
                    "--root",
                    str(root),
                    "start",
                    "RTD-2343: Доработка переключения вызова",
                    "--yes",
                ]
            )

            self.assertEqual(code, 0)
            self.assertTrue((root / "ProjectSpecs" / "Архив").is_dir())
            self.assertTrue((root / "ProjectSpecs" / "Документация").is_dir())
            task_dir = (
                root
                / "ProjectSpecs"
                / "Задачи в работе"
                / "RTD-2343 - Доработка переключения вызова"
            )
            self.assertTrue(task_dir.is_dir())

    def test_find_task_by_number_ignores_title(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            run_cli(
                [
                    "--root",
                    str(root),
                    "start",
                    "RTD-2343: Старое название",
                    "--yes",
                ]
            )

            found = task1cspec.find_task(root, "RTD-2343")

            self.assertIsNotNone(found)
            state, task_dir = found
            self.assertEqual(state, "active")
            self.assertEqual(task_dir.name, "RTD-2343 - Старое название")

    def test_role_creates_expected_specification(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            run_cli(["--root", str(root), "start", "RTD-1: Test", "--yes"])

            code = run_cli(["--root", str(root), "role", "Аналитик", "RTD-1"])

            self.assertEqual(code, 0)
            spec = (
                root
                / "ProjectSpecs"
                / "Задачи в работе"
                / "RTD-1 - Test"
                / "ТехЗадание.md"
            )
            self.assertTrue(spec.exists())
            self.assertIn("## Как сейчас", spec.read_text(encoding="utf-8"))

    def test_archive_moves_active_task(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            run_cli(["--root", str(root), "start", "RTD-2: Test", "--yes"])

            code = run_cli(["--root", str(root), "archive", "RTD-2", "--yes"])

            self.assertEqual(code, 0)
            self.assertFalse(
                (root / "ProjectSpecs" / "Задачи в работе" / "RTD-2 - Test").exists()
            )
            self.assertTrue((root / "ProjectSpecs" / "Архив" / "RTD-2 - Test").is_dir())


if __name__ == "__main__":
    unittest.main()
