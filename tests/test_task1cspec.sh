#!/bin/sh
set -eu

ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)

fail() {
  printf '%s\n' "ОШИБКА: $*" >&2
  exit 1
}

assert_dir() {
  [ -d "$ROOT/$1" ] || fail "нет каталога: $1"
}

assert_file() {
  [ -f "$ROOT/$1" ] || fail "нет файла: $1"
}

assert_no_path() {
  [ ! -e "$ROOT/$1" ] || fail "неожиданный путь: $1"
}

assert_contains() {
  file=$1
  text=$2
  grep -F -- "$text" "$ROOT/$file" >/dev/null || fail "$file не содержит: $text"
}

assert_not_contains() {
  file=$1
  text=$2
  if grep -F -- "$text" "$ROOT/$file" >/dev/null; then
    fail "$file неожиданно содержит: $text"
  fi
}

assert_dir "ProjectSpecs/Архив"
assert_dir "ProjectSpecs/Документация"
assert_dir "ProjectSpecs/Задачи в работе"

assert_file "AGENTS.md"
assert_file ".task1cspec/AGENTS.md"
assert_file ".task1cspec/skills/task1cspec/SKILL.md"
assert_file ".task1cspec/skills/task1cspec/references/templates.md"
assert_file ".task1cspec/skills/task1cspec/references/templates/analyst.md"
assert_file ".task1cspec/skills/task1cspec/references/templates/architect.md"
assert_file ".task1cspec/skills/task1cspec/references/templates/developer.md"
assert_file ".task1cspec/skills/task1cspec/references/templates/tester.md"
assert_file ".task1cspec/skills/task1cspec/references/templates/techwriter.md"

assert_no_path ".task1cspec/scripts"

assert_contains ".task1cspec/AGENTS.md" "Не полагайся на локальные вспомогательные скрипты и Python."
assert_contains ".task1cspec/skills/task1cspec/SKILL.md" "Не используй локальные вспомогательные скрипты и не требуй Python."
assert_contains "README.md" "Task1CSpec не требует Python, Node.js или установки CLI-помощников."
assert_contains ".task1cspec/.codex-plugin/plugin.json" "Начни задачу RTD-2343"

assert_not_contains "README.md" "python3 .task1cspec/scripts/task1cspec.py"
assert_not_contains ".task1cspec/AGENTS.md" "task1cspec.py"
assert_not_contains ".task1cspec/skills/task1cspec/SKILL.md" "task1cspec.py"
assert_not_contains ".task1cspec/.codex-plugin/plugin.json" "/Task"

printf '%s\n' "ОК: Task1CSpec работает через файловые операции агента без вспомогательных скриптов на Python."
