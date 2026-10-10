#!/usr/bin/env bash
# Rebuilds the site for root-domain hosting and copies it into the WordPress
# plugin's site/ folder. Run from the repo root:  bash wordpress/sync-build-into-plugin.sh
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

# Root-domain build (empty base path): URLs are /california/..., assets /assets/...
SITE_BASE_PATH="" python3 build.py

PLUGIN_SITE="wordpress/dnm-california/site"
rm -rf "$PLUGIN_SITE"
mkdir -p "$PLUGIN_SITE"
cp -r public/* "$PLUGIN_SITE"/
[ -f public/.nojekyll ] && cp public/.nojekyll "$PLUGIN_SITE"/ || true

echo "Synced build into $PLUGIN_SITE"
echo "Now copy wordpress/dnm-california/ to wp-content/plugins/ and (re)activate."
