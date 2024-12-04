#!/bin/bash

# Убедимся, что скрипт выполняется в корневой директории git-репозитория.
if [ ! -d ".git" ]; then
  echo "Этот скрипт должен быть выполнен в корневой директории git-репозитория."
  exit 1
fi

# Получаем последний тег (релиз)
LAST_TAG=$(git describe --tags --abbrev=0)
if [ -z "$LAST_TAG" ]; then
  echo "Не удалось найти последний тег (релиз)."
  exit 1
fi

# Получаем текущую дату
CURRENT_DATE=$(date +"%Y-%m-%d")

# Получаем список всех коммитов с момента последнего тега
COMMITS=$(git log "$LAST_TAG"..HEAD --pretty=format:"- %s [%h](https://github.com/your-username/your-repo/commit/%H)")

# Проверка, есть ли новые коммиты
if [ -z "$COMMITS" ]; then
  echo "Нет новых коммитов с момента последнего тега $LAST_TAG."
  exit 0
fi

# Новый номер версии (здесь можно настроить автоинкремент, если нужно)
VERSION="v$(echo $LAST_TAG | awk -F. -v OFS=. '{$NF++; print $0}')"

# Создаем новый раздел в changelog.md
echo "## $VERSION - $CURRENT_DATE" >> changelog.md
echo "$COMMITS" >> changelog.md

echo "Changelog обновлен с новой версией $VERSION."
