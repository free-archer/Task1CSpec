#!/usr/bin/env python3
"""Файловый помощник для Task1CSpec.

Скрипт намеренно не пишет финальные спецификации за агента.
Он управляет стабильной структурой задач для локального Codex-оркестратора.
"""

from __future__ import annotations

import argparse
import re
import shutil
import sys
from dataclasses import dataclass
from pathlib import Path


PROJECT_SPECS = "ProjectSpecs"
ARCHIVE_DIR = "Архив"
DOCS_DIR = "Документация"
ACTIVE_DIR = "Задачи в работе"

SPEC_ORDER: tuple[tuple[str, str, str], ...] = (
    ("Аналитик", "ТехЗадание.md", "Спецификация целей"),
    ("Архитектор", "Архитектура.md", "Архитектурная спецификация"),
    ("Разработчик", "Реализация.md", "Спецификация реализации"),
    ("Тестировщик", "Тест-кейсы.md", "Спецификация тестирования"),
    ("Технический писатель", "Документация по задаче.md", "Документация"),
)

ROLE_ALIASES = {
    "analyst": "Аналитик",
    "аналитик": "Аналитик",
    "architect": "Архитектор",
    "архитектор": "Архитектор",
    "developer": "Разработчик",
    "разработчик": "Разработчик",
    "tester": "Тестировщик",
    "тестировщик": "Тестировщик",
    "techwriter": "Технический писатель",
    "technical-writer": "Технический писатель",
    "техническийписатель": "Технический писатель",
    "технический-писатель": "Технический писатель",
    "технический писатель": "Технический писатель",
}


@dataclass(frozen=True)
class TaskInput:
    number: str
    title: str


def project_root(root: Path) -> Path:
    return root / PROJECT_SPECS


def active_root(root: Path) -> Path:
    return project_root(root) / ACTIVE_DIR


def archive_root(root: Path) -> Path:
    return project_root(root) / ARCHIVE_DIR


def docs_root(root: Path) -> Path:
    return project_root(root) / DOCS_DIR


def ensure_layout(root: Path) -> None:
    for path in (archive_root(root), docs_root(root), active_root(root)):
        path.mkdir(parents=True, exist_ok=True)


def parse_task(value: str) -> TaskInput:
    raw = value.strip()
    if not raw:
        raise ValueError("Задача не заполнена.")

    if ":" in raw:
        number, title = raw.split(":", 1)
    else:
        number, title = raw, ""

    number = number.strip()
    title = title.strip()
    if not number:
        raise ValueError("Номер задачи не заполнен.")
    return TaskInput(number=number, title=title)


def sanitize_part(value: str) -> str:
    cleaned = re.sub(r'[<>:"/\\|?*\x00-\x1f]', "-", value.strip())
    cleaned = re.sub(r"\s+", " ", cleaned)
    cleaned = re.sub(r"-{2,}", "-", cleaned)
    return cleaned.strip(" .-")


def task_folder_name(task: TaskInput) -> str:
    number = sanitize_part(task.number)
    title = sanitize_part(task.title)
    if title:
        return f"{number} - {title}"
    return number


def task_number_from_folder(path: Path) -> str:
    name = path.name
    if " - " in name:
        return name.split(" - ", 1)[0]
    return name


def find_task(root: Path, number: str) -> tuple[str, Path] | None:
    ensure_layout(root)
    wanted = number.strip().casefold()
    for state, base in (("active", active_root(root)), ("archive", archive_root(root))):
        for child in sorted(base.iterdir()):
            if child.is_dir() and task_number_from_folder(child).casefold() == wanted:
                return state, child
    return None


def spec_status(task_dir: Path) -> list[tuple[str, str, bool]]:
    return [
        (role, filename, (task_dir / filename).exists())
        for role, filename, _description in SPEC_ORDER
    ]


def next_stage(task_dir: Path) -> tuple[str, str, str] | None:
    for role, filename, description in SPEC_ORDER:
        if not (task_dir / filename).exists():
            return role, filename, description
    return None


def normalize_role(role: str) -> str:
    key = role.strip().casefold().replace("_", "-")
    normalized = ROLE_ALIASES.get(key)
    if normalized:
        return normalized
    for known, _filename, _description in SPEC_ORDER:
        if known.casefold() == key:
            return known
    raise ValueError(f"Неизвестная роль: {role}")


def role_spec_filename(role: str) -> str:
    normalized = normalize_role(role)
    for known, filename, _description in SPEC_ORDER:
        if known == normalized:
            return filename
    raise ValueError(f"Неизвестная роль: {role}")


def starter_content(role: str, task_dir: Path) -> str:
    task_number = task_number_from_folder(task_dir)
    title = task_dir.name.split(" - ", 1)[1] if " - " in task_dir.name else ""

    if role == "Аналитик":
        return f"""# ТехЗадание

## Задача

- Номер: {task_number}
- Название: {title}
- Инициатор:
- Контекст:

## Цель

## Как сейчас

## Как должно быть

## Как проверить результат

## Вопросы и допущения

"""

    if role == "Архитектор":
        return """# Архитектура

## Контекст

## Создаваемые объекты 1С

| Объект | Назначение |
|---|---|

## Изменяемые объекты 1С

| Объект | Что меняется |
|---|---|

## Удаляемые объекты 1С

| Объект | Причина |
|---|---|

## Новые функции и процедуры

| Имя | Модуль | Назначение |
|---|---|---|

## Размещение кода

| Модуль | Изменение |
|---|---|

## Проверки архитектуры

- Использованные MCP/источники анализа:
- Использованные правила и стандарты 1С:
- Риски:

"""

    if role == "Разработчик":
        return """# Реализация

## Контекст реализации

## Изменяемые модули

| Модуль | Изменение |
|---|---|

## Алгоритм

## Основные функции и процедуры

## Обработка ошибок и граничные случаи

## План изменения кода

## Вопросы и допущения

"""

    if role == "Тестировщик":
        return """# Тест-кейсы

## Область тестирования

## Ручные тест-кейсы

| ID | Предусловия | Шаги | Ожидаемый результат |
|---|---|---|---|

## Gherkin-сценарии

```gherkin
# language: ru
Функционал:

Сценарий:
  Дано
  Когда
  Тогда
```

## Регрессия

## Тестовые данные

"""

    return """# Документация по задаче

## Что сделано

## Для чего сделано

## Как работает

## Как проверено

## Результат

## Связанная проектная документация

"""


def print_task_status(state: str, task_dir: Path) -> None:
    state_label = "в работе" if state == "active" else "архив"
    print(f"Задача: {task_dir.name}")
    print(f"Статус: {state_label}")
    print(f"Путь: {task_dir}")
    print("Спецификации:")
    for role, filename, exists in spec_status(task_dir):
        marker = "есть" if exists else "нет"
        print(f"- {role}: {filename} [{marker}]")

    stage = next_stage(task_dir)
    if stage is None:
        print("Дальше: все спецификации есть. Используйте архивирование после проверки документации.")
    else:
        role, filename, description = stage
        print(f"Дальше: {role} -> {filename} ({description})")


def confirm(prompt: str) -> bool:
    answer = input(f"{prompt} [y/N] ").strip().casefold()
    return answer in {"y", "yes", "д", "да"}


def cmd_init(args: argparse.Namespace) -> int:
    root = Path(args.root).resolve()
    ensure_layout(root)
    print(f"Инициализировано: {project_root(root)}")
    return 0


def cmd_start(args: argparse.Namespace) -> int:
    root = Path(args.root).resolve()
    task = parse_task(args.task)
    found = find_task(root, task.number)
    if found:
        state, task_dir = found
        print_task_status(state, task_dir)
        return 0

    print(f"Папка задачи не найдена по номеру: {task.number}")
    if not args.yes and not confirm("Создать новую задачу?"):
        print("Отменено.")
        return 2

    task_dir = active_root(root) / task_folder_name(task)
    task_dir.mkdir(parents=False, exist_ok=False)
    print(f"Создана папка задачи: {task_dir}")
    print_task_status("active", task_dir)
    return 0


def cmd_status(args: argparse.Namespace) -> int:
    root = Path(args.root).resolve()
    ensure_layout(root)
    if args.task:
        task = parse_task(args.task)
        found = find_task(root, task.number)
        if not found:
            print(f"Папка задачи не найдена по номеру: {task.number}", file=sys.stderr)
            return 1
        state, task_dir = found
        print_task_status(state, task_dir)
        return 0

    print(f"ProjectSpecs: {project_root(root)}")
    for label, base in (("В работе", active_root(root)), ("Архив", archive_root(root))):
        tasks = [path.name for path in sorted(base.iterdir()) if path.is_dir()]
        print(f"{label}: {len(tasks)}")
        for task_name in tasks:
            print(f"- {task_name}")
    return 0


def cmd_role(args: argparse.Namespace) -> int:
    root = Path(args.root).resolve()
    role = normalize_role(args.role)
    task = parse_task(args.task)
    found = find_task(root, task.number)
    if not found:
        print(f"Папка задачи не найдена по номеру: {task.number}", file=sys.stderr)
        return 1

    state, task_dir = found
    if state != "active":
        print(f"Задача в архиве и не может быть изменена: {task_dir}", file=sys.stderr)
        return 1

    filename = role_spec_filename(role)
    target = task_dir / filename
    if target.exists() and not args.force:
        print(f"Спецификация уже существует: {target}")
    else:
        target.write_text(starter_content(role, task_dir), encoding="utf-8")
        print(f"Создан стартовый файл спецификации: {target}")

    print_task_status(state, task_dir)
    return 0


def cmd_archive(args: argparse.Namespace) -> int:
    root = Path(args.root).resolve()
    task = parse_task(args.task)
    found = find_task(root, task.number)
    if not found:
        print(f"Папка задачи не найдена по номеру: {task.number}", file=sys.stderr)
        return 1

    state, task_dir = found
    if state == "archive":
        print(f"Задача уже в архиве: {task_dir}")
        return 0

    if not args.yes and not confirm("Перенести эту задачу в ProjectSpecs/Архив?"):
        print("Отменено.")
        return 2

    destination = archive_root(root) / task_dir.name
    if destination.exists():
        print(f"Папка в архиве уже существует: {destination}", file=sys.stderr)
        return 1

    shutil.move(str(task_dir), str(destination))
    print(f"Задача перенесена в архив: {destination}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Файловый помощник Task1CSpec")
    parser.add_argument(
        "--root",
        default=".",
        help="Корень проекта, где находится или должна быть создана папка ProjectSpecs.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("init", help="Создать папки ProjectSpecs").set_defaults(func=cmd_init)

    start = subparsers.add_parser("start", help="Найти или создать папку задачи")
    start.add_argument("task", help='Задача, например "RTD-2343: Название задачи"')
    start.add_argument("--yes", action="store_true", help="Создать отсутствующую задачу без вопроса")
    start.set_defaults(func=cmd_start)

    status = subparsers.add_parser("status", help="Показать статус задачи или проекта")
    status.add_argument("task", nargs="?", help="Необязательный номер задачи")
    status.set_defaults(func=cmd_status)

    role = subparsers.add_parser("role", help="Создать стартовую спецификацию для роли")
    role.add_argument("role", help="Название роли или алиас")
    role.add_argument("task", help="Номер задачи")
    role.add_argument("--force", action="store_true", help="Перезаписать спецификацию роли")
    role.set_defaults(func=cmd_role)

    archive = subparsers.add_parser("archive", help="Перенести активную задачу в архив")
    archive.add_argument("task", help="Номер задачи")
    archive.add_argument("--yes", action="store_true", help="Архивировать без вопроса")
    archive.set_defaults(func=cmd_archive)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return args.func(args)
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
