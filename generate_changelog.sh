#!/bin/bash

# Get the latest tag
latest_tag=$(git describe --tags --abbrev=0)
current_date=$(date +'%Y-%m-%d')

# Get commits since the last tag
commits=$(git log ${latest_tag}..HEAD --oneline)

# Define changelog file
changelog_file="changelog.md"

# Add a new section to the changelog
{
  echo "## [v$(date +'%Y.%m.%d')] - $current_date"
  echo
  while IFS= read -r line; do
    commit_hash=$(echo $line | awk '{print $1}')
    commit_message=$(echo $line | sed -e "s/$commit_hash //")
    echo "- $commit_message [\`$commit_hash\`](https://github.com/<OWNER>/<REPO>/commit/$commit_hash)"
  done <<< "$commits"
  echo
} >> $changelog_file
