# Task1CSpec Local Orchestrator

This directory contains a local Task1CSpec orchestrator. Treat these instructions as active whenever the root `AGENTS.md` points here.

## Activation

Use Task1CSpec when the user asks to manage 1C task specifications or sends one of these commands, with or without a leading slash:

- `TaskStart` or `/TaskStart`
- `TaskAnalyst` or `/TaskAnalyst`
- `TaskArchitect` or `/TaskArchitect`
- `TaskDeveloper` or `/TaskDeveloper`
- `TaskTester` or `/TaskTester`
- `TaskTechWriter` or `/TaskTechWriter`
- `TaskАналитик` or `/TaskАналитик`
- `TaskАрхитектор` or `/TaskАрхитектор`
- `TaskРазработчик` or `/TaskРазработчик`
- `TaskТестировщик` or `/TaskТестировщик`
- `TaskТехническийПисатель` or `/TaskТехническийПисатель`

Before doing Task1CSpec work, read `.task1cspec/skills/task1cspec/SKILL.md` completely and follow it as the workflow authority. If it references `references/templates.md`, read that index and the role-specific template file before creating or updating specifications.

## Local Files

The orchestrator is intentionally project-local and does not require Codex plugin installation.

- Keep task data in `ProjectSpecs/`.
- Use `.task1cspec/scripts/task1cspec.py` for `init`, `start`, `status`, `role`, and `archive` when the script exists.
- The `.task1cspec/commands/` directory is compatibility documentation for plugin/custom-command use. Do not require it to be installed for the local workflow.

## Command Handling

If a Task1CSpec command is received as plain text, parse it exactly like the slash command:

- `TaskStart RTD-2343: Название` starts or continues a task.
- `TaskAnalyst RTD-2343` runs the analyst stage.
- `TaskArchitect RTD-2343` runs the architect stage.
- `TaskDeveloper RTD-2343` runs the developer stage.
- `TaskTester RTD-2343` runs the tester stage.
- `TaskTechWriter RTD-2343` runs the technical writer stage.

If the Codex client does not accept unknown slash commands, tell the user to send the same command without the leading slash.

## Safety Rules

- Do not modify production code during `TaskDeveloper` until the user has explicitly approved `Реализация.md`.
- Do not archive a task until the user explicitly confirms archiving.
- Do not create a new task folder when only a task number was supplied and no existing task folder was found; ask whether this is a new task first.
- Preserve unrelated project changes.
