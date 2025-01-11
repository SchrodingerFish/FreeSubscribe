#!/bin/sh

# BSD shell
REPO_URL="https://github.com/SchrodingerFish/FreeSubscribe.git"
PROJECT_DIR="/usr/home/XXX/FreeSubscribe"
TARGET_DIR="/usr/home/XXX/domains/yourdomain/public_html"

if [ ! -d "$PROJECT_DIR" ]; then
    git clone "$REPO_URL" "$PROJECT_DIR"
fi

cd "$PROJECT_DIR" || exit
git pull origin master

cp -f "$PROJECT_DIR/html/index.html" "$TARGET_DIR"

echo "Update completed and index.html copied to $TARGET_DIR"

