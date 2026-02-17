#!/bin/bash
# Commit analysis results to GitHub

cd /Users/antonklaus/.openclaw/sandboxes/agent-main-main-6d9217fe/rochester-property-scout

echo "📦 Staging files..."
git add .

echo "💾 Committing analysis report..."
git commit -m "Add investment analysis: 898 South Clinton Ave

- Investment Score: 72/100 (STRONG BUY)
- Asking: \$3.0M | Suggested Counter: \$2.76M
- 4 comparable properties analyzed
- Full analysis summary and JSON report included"

echo "🚀 Pushing to GitHub..."
git push origin main

echo "✅ Analysis committed and pushed successfully!"
echo ""
echo "View at: https://github.com/$(gh repo view --json owner,name -q '.owner.login + "/" + .name')"
