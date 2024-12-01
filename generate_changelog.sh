#!/bin/bash

# Получение последнего тега
last_tag=$(git describe --tags `git rev-list --tags --max-count=1`)

# Получение коммитов с момента последнего тега
commits=$(git log --pretty=format:"* %s [%h]" "$last_tag"..HEAD)

# Формирование даты
date=$(date +"%Y-%m-%d")

# Формирование заголовка
version=$(git describe --tags --always)
header="## ${version} - ${date}"

# Создание новой записи в changelog.md
echo "$header" >> changelog.md
echo "$commits" >> changelog.md
echo "" >> changelog.md
