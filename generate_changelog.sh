#!/bin/bash

# Получаем последний тег
last_tag=$(git describe --tags --abbrev=0)

# Получаем коммиты с момента последнего тега
commits=$(git log --pretty=format:"* %s [%h]" $last_tag..HEAD)

# Генерируем заголовок для changelog
version=$(git describe --tags --always)
date=$(date +%Y-%m-%d)
echo "## $version - $date" >> changelog.md

# Добавляем коммиты в changelog
echo "$commits" >> changelog.md

# Добавляем ссылку на GitHub (адаптируйте под свой репозиторий)
echo "" >> changelog.md
echo "Полный лог изменений: [https://github.com/tooliebby/financial_subscriptions/commits/$version](https://github.com/tooliebby/financial_subscriptions/commits/$version)" >> changelog.md
