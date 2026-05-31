# FitLife HTML Frontend

The frontend is **pure HTML + Bootstrap 5 + CSS + JavaScript**, rendered by Flask (Jinja2 templates).

## Folder: `fitlife/app/templates/`

| File | URL | Description |
|------|-----|-------------|
| `index.html` | `/` | Landing / home page |
| `login.html` | `/auth/login` | Full-page login form |
| `register.html` | `/auth/register` | Full-page registration form |
| `dashboard.html` | `/dashboard` | Main app (6 tabs) |
| `base.html` | — | Layout wrapper (navbar, flashes, assets) |
| `emails/welcome.html` | — | HTML welcome email template |
| `partials/site_nav.html` | — | Home page navbar |
| `partials/site_footer.html` | — | Site footer |
| `partials/dashboard_nav.html` | — | Dashboard tab navbar |

## Static assets: `fitlife/app/static/`

| File | Purpose |
|------|---------|
| `css/style.css` | Dark theme, cards, auth pages, dashboard |
| `js/main.js` | Navbar scroll, weight chart, CSRF for API |

## Edit the UI

1. Change layout/content → edit the `.html` files in `templates/`
2. Change colors/spacing → edit `static/css/style.css`
3. Change chart / AJAX → edit `static/js/main.js`

Restart Flask after template/CSS changes (debug mode auto-reloads).
