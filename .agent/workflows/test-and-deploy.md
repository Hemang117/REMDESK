---
description: Standard procedure for testing changes locally and deploying to Vercel
---

# Test & Deploy SOP

## 1. Local Testing (ALWAYS before deploy)

// turbo
### Start/Restart the dev server
```bash
lsof -ti:8000 | xargs kill -9 2>/dev/null; sleep 1; python3 manage.py runserver
```

### Verify in browser
- Open http://127.0.0.1:8000 and navigate to the changed pages
- Take screenshots of before/after if UI changes
- Test form submissions, edge cases, and error states
- Check terminal for any Django errors or warnings

### Report findings to user
- Summarize what works and what doesn't
- Include screenshots as evidence
- Note any issues found during testing

## 2. Deploy (ONLY after consulting with user)

> [!CAUTION]
> **NEVER push to Vercel without explicit user approval.**

### Pre-deploy checklist
- [ ] All changes tested locally
- [ ] User has reviewed and approved
- [ ] Decide what to include (use `git stash` for selective deploys)

### Selective deploy (when not all WIP should ship)
```bash
git stash push -m "wip-description" -- .
# Apply only the changes to deploy
git add <specific-files>
git commit -m "description"
git push origin main
git stash pop
```

### Full deploy
```bash
git add -A
git commit -m "description"
git push origin main
```

### Post-deploy verification
- Check Vercel dashboard for build status
- Test the live site at https://remdeskjobs.com
- Report deployment status to user
