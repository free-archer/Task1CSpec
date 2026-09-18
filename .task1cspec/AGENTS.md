# Task1CSpec Local Orchestrator

This directory contains a local Task1CSpec orchestrator. Treat these instructions as active whenever the root `AGENTS.md` points here.

## Activation

Use Task1CSpec when the user asks to manage 1C task specifications or sends one of these local-mode commands:

- `Начни задачу`
- `Начни аналитику`
- `Начни архитектуру`
- `Начни разработку`
- `Начни тестирование`
- `Начни документацию`

Before doing Task1CSpec work, read `.task1cspec/skills/task1cspec/SKILL.md` completely and follow it as the workflow authority. If it references `references/templates.md`, read that index and the role-specific template file before creating or updating specifications.

## Local Files

The orchestrator is intentionally project-local and does not require Codex plugin installation.

- Keep task data in `ProjectSpecs/`.
- Do not rely on local helper scripts or Python. Perform `init`, `start`, `status`, `role`, and `archive` as direct agent file operations with shell commands such as `mkdir`, `find`, `mv`, and file reads/writes.

## Command Handling

Local-mode commands are plain text and do not start with `/`. Codex clients may intercept unknown slash commands before the agent can process them.

- `Начни задачу RTD-2343: Название` starts or continues a task.
- `Начни аналитику RTD-2343 <путь-к-файлу>` or `Начни аналитику RTD-2343 <текст требований>` runs the analyst stage.
- `Начни архитектуру RTD-2343` runs the architect stage.
- `Начни разработку RTD-2343` creates or updates `Реализация.md`; when the task is already waiting for implementation approval, the same command starts code changes and changes the task status to `В разработке`.
- `Начни тестирование RTD-2343` runs the tester stage.
- `Начни документацию RTD-2343` runs the technical writer stage.
- If the user sends a role command without a task number, for example `Начни документацию`, ask only for the task number and wait.

## Safety Rules

- Do not modify production code when `Начни разработку` creates or updates `Реализация.md`; after creating `Реализация.md`, wait for the user to approve it and repeat `Начни разработку`.
- On repeated `Начни разработку` after implementation approval, update `.task1cspec.json` so the task status becomes `В разработке`, then modify code according to the approved `Реализация.md`.
- Do not archive a task until the user explicitly confirms archiving.
- Do not create a new task folder when only a task number was supplied and no existing task folder was found; ask whether this is a new task first.
- `Начни задачу` only creates or finds the task folder and service files; do not create stage specifications at that step.
- During `Начни аналитику`, require either a source file path or a requirements prompt before creating `ТехЗадание.md`.
- Ask all missing-information questions interactively in chat. Do not leave questions, TODOs, or unresolved prompts inside specification files.
- Preserve unrelated project changes.
