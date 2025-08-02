#!/bin/bash

echo "🔁 Pulling latest changes with rebase..."
git pull origin main --rebase

echo "📦 Adding all changes..."
git add .

echo "📝 Enter commit message:"
read message

git commit -m "$message"

echo "🚀 Pushing to origin/main..."
git push origin main

echo "✅ Done! All changes pushed."