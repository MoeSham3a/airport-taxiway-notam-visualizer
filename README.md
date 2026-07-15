# GND/NOTAM Chart Viewer

A browser-based tool for visualizing taxiway closure NOTAMs on an airport ground chart. Paste NOTAM text (or an arrival time window), and active/future/expired taxiway closures get parsed out and highlighted directly on the chart.

Live: https://moesham3a.github.io/airport-taxiway-notam-visualizer/

**Not for navigation.** This is an illustration tool for cross-checking NOTAMs against a chart, not an official source.

## Features

- Parses pasted NOTAM text (or a manual arrival window) and highlights closed/partially-closed taxiways on the chart, color-coded by status (active / future / expired).
- Multi-airport support via the Airport Manager (⊞ button) — switch between built-in airports or add your own (ICAO, name, chart image, taxiway JSON).
- Installable as a PWA (works offline once an airport has been loaded once) with a service worker caching the app shell and per-airport data separately.
- Taxiway position editor (⊕ Calibrate) for placing/repositioning/tracing taxiway markers on a chart, with intersection auto-detection. Edits persist per-device in IndexedDB, so they survive reloads.

## Running locally

This is a static site with no build step, but it uses `fetch()` for its airport data, which browsers block under `file://`. You need to serve it over HTTP:

```
python -m http.server 8000
```

then open `http://localhost:8000/`.

## Repo layout

```
index.html              app shell (HTML/CSS/JS, no framework, no build step)
sw.js                    service worker (offline caching)
manifest.json            PWA manifest
airports/
  registry.json          list of built-in airports + metadata (name, viewBox, file paths)
  <ICAO>/chart.jpg        ground chart image
  <ICAO>/taxiways.json    taxiway positions: { "NAME": { "x", "y", "label" } | { "points": [[x,y],...], "label" } }
.github/workflows/       GitHub Actions workflow that deploys to GitHub Pages on push to main
_archive/                one-off scripts used during the original data migration (not part of the running app)
```

## Adding or updating an airport's baseline data

Taxiway edits made in the app persist locally (IndexedDB), but since this is a static site with no backend, making an edit the new *shipped* baseline for everyone requires a manual step:

1. In the Taxiway Editor, click **⬇ Export JSON** — this downloads the current taxiway map in the same flat shape as `airports/<ICAO>/taxiways.json`.
2. Replace `airports/<ICAO>/taxiways.json` with the downloaded file.
3. Commit and push to `main` — the GitHub Actions workflow redeploys automatically.

To add a brand-new built-in airport, add an entry to `airports/registry.json` (with `viewBox` matching the chart image's pixel dimensions) and drop the chart image + a `taxiways.json` (can start as `{}`) under `airports/<ICAO>/`.

## Deployment

Every push to `main` triggers `.github/workflows/pages.yml`, which uploads the repo root as the Pages artifact — no build step. GitHub Pages must have **Settings → Pages → Build and deployment → Source** set to **GitHub Actions**.
