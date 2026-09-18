---
description: Начать или продолжить задачу Task1CSpec.
argument-hint: "<номер-задачи>: <название-задачи>"
allowed-tools: [Read, Glob, Grep, Bash, Write, Edit]
---

# TaskStart

Пользователь вызвал `/TaskStart` с аргументами: `$ARGUMENTS`

Прочитай `.task1cspec/skills/task1cspec/SKILL.md` и выполни процедуру TaskStart точно по инструкции.

Если номер и название задачи не переданы, запроси задачу в таком формате:

```text
RTD-2343: Доработка переключения вызова из ОМ ВнешниеДанные. ТоварныеОперации
```

Используй `.task1cspec/scripts/task1cspec.py start "$ARGUMENTS"`, если скрипт доступен в текущем проекте. Если скрипт недоступен, выполни те же файловые проверки вручную.
