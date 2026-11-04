# AI Inventory Agent – CI/CD (EECE430 Assignment 6)

Django + Gemini inventory chat agent, with a GitHub Actions pipeline:

- **test** (GitHub's Ubuntu runner): install deps → `manage.py check` → `manage.py test` → build Docker image → push to GHCR
- **deploy** (self-hosted runner on my laptop, label `portfolio-deploy`): pull the image → replace the `inventory-agent` container → app at http://localhost:8000

## One-time setup

1. **Create the repo** on GitHub (public, no README), then from this folder:
   ```
   git init
   git add .
   git commit -m "AI Inventory Agent with CI/CD"
   git branch -M main
   git remote add origin https://github.com/<your-username>/<repo-name>.git
   git push -u origin main
   ```
2. **Add the Gemini key as a secret**: repo → Settings → Secrets and variables → Actions → New repository secret
   - Name: `GEMINI_API_KEY`
   - Value: your key (the one from your local `.env`)

   `.env` is in `.gitignore` on purpose. Never commit the key.
3. **Self-hosted runner**: Settings → Actions → Runners → New self-hosted runner (Windows or macOS, x64).
   Create the runner folder outside the project, run GitHub's Download and Configure commands, then:
   - name: `portfolio-local`
   - additional label: `portfolio-deploy`
   - run as service: `N`

   Start it with `.\run.cmd` (Windows PowerShell) or `./run.sh` (macOS).
4. **Collaborator**: Settings → Collaborators → Add people → `am38@aub.edu.lb`.

## Demo

1. Docker Desktop running, runner running (shows *Idle*).
2. Open http://localhost:8000 and ask: *what is the cost of 3 chocolate bars after adding 10% VAT?*
3. Change something visible (e.g. the `<h2>` in `chat/templates/chat.html`), then:
   ```
   git add .
   git commit -m "demo change"
   git push
   ```
4. Watch Actions: test → deploy go green, then refresh localhost:8000 to see the change.

## Run locally without Docker
```
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```
(needs a `.env` with `GEMINI_API_KEY=...`)
