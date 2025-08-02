#!/bin/bash

echo "🔁 Pulling latest changes with rebase..."
git pull origin main --rebase

echo "📦 Adding all changes..."
git add .

echo "🔒 Committing with auto message..."
git commit -am "fix: auto deploy" 2>/dev/null || echo "ℹ️ Nothing to commit"

echo "🚀 Pushing to origin/main..."
git push origin main

echo "✅ Done! All changes pushed."
