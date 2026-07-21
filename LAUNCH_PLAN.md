# Sittr — Beginner's Path to Going Live

A checklist to work through in order. Check items off as you go.

## Phase 0 — Decide what to change first
- [ ] Write down the list of changes/fixes/content you want done before launch (keep it realistic — ship a solid v1, iterate after)
- [ ] Work through them one at a time with Claude Code in PyCharm: describe the change, review the diff, test with `python manage.py runserver`, commit

## Phase 1 — Production readiness (done for you already)
- [x] `SECRET_KEY`, `DEBUG`, `ALLOWED_HOSTS`, `CSRF_TRUSTED_ORIGINS` now read from environment variables instead of being hardcoded
- [x] WhiteNoise added for serving static files (no separate static host/CDN needed)
- [x] `gunicorn` (production web server), `dj-database-url`, `psycopg2-binary` added to `requirements.txt`
- [x] Production security hardening (HTTPS redirect, secure cookies) — only kicks in when `DEBUG=False`
- [x] Local `.env` updated with `DEBUG=True` so nothing breaks locally
- [ ] You: run `pip install -r requirements.txt` in your venv to pull in the new packages
- [ ] You: confirm the site still runs fine locally with `python manage.py runserver`

## Phase 2 — Test production settings locally (recommended, optional)
- [ ] Temporarily set `DEBUG=False` in `.env`
- [ ] Run `python manage.py collectstatic` and check it succeeds
- [ ] Run `python manage.py runserver` and click around — catches static file issues before they hit production
- [ ] Set `DEBUG=True` back in `.env` when done

## Phase 3 — Push to GitHub
- [ ] Commit all changes (settings, requirements, website edits)
- [ ] Push to the `main` branch of `borislavbog931/Sittr` — Render deploys straight from GitHub

## Phase 4 — Create hosting on Render
- [ ] Sign up at render.com (GitHub login works)
- [ ] Create a new **PostgreSQL** database (free tier)
- [ ] Create a new **Web Service**, connect the Sittr GitHub repo
  - Build command: `pip install -r requirements.txt && python manage.py tailwind build && python manage.py collectstatic --noinput`
  - Start command: `gunicorn Sittr.wsgi:application`
- [ ] Link the PostgreSQL database to the web service — Render auto-injects `DATABASE_URL`, no manual config needed

## Phase 5 — Environment variables on Render
Set these in the web service's **Environment** tab:
- [ ] `SECRET_KEY` — generate a fresh one for production, don't reuse your local one
- [ ] `DEBUG` — leave unset or set to `False`
- [ ] `ALLOWED_HOSTS` — `your-app-name.onrender.com` (add your custom domain here later)
- [ ] `CSRF_TRUSTED_ORIGINS` — `https://your-app-name.onrender.com`

## Phase 6 — Migrate database & create admin user
- [ ] Open the Shell tab on Render, run `python manage.py migrate`
- [ ] Run `python manage.py createsuperuser` and log into `/admin/` to confirm

## Phase 7 — Custom domain
- [ ] Buy a domain (Cloudflare Registrar or Namecheap are cheap, no markup)
- [ ] In Render, add the custom domain to your web service
- [ ] Add the DNS records Render gives you at your domain registrar
- [ ] Update `ALLOWED_HOSTS` and `CSRF_TRUSTED_ORIGINS` env vars to include the new domain
- [ ] Wait for DNS to propagate (can take a few hours) — Render auto-issues free SSL once it verifies

## Phase 8 — Final checks
- [ ] Visit the live domain and test: search/filter caretakers, submit a hire request, leave a review, admin login
- [ ] Check the browser console for errors
- [ ] Confirm CSS/JS/images all load correctly (this is where WhiteNoise issues would show up)
- [ ] Test on a phone
