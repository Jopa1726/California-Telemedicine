<?php
/**
 * Plugin Name:       DNM California (Telemedicine Preview)
 * Description:        Mounts the "Doctors of Natural Medicine — California" static preview inside WordPress at /california/ and /careers/california-physicians/. Drop-in, no theme edits. Serves pre-built HTML/CSS/JS so your dev team can review and iterate under the real domain.
 * Version:           1.0.0
 * Requires at least: 5.8
 * Requires PHP:      7.4
 * Author:            Doctors of Natural Medicine
 * License:           GPL-2.0-or-later
 *
 * HOW IT WORKS
 * ------------
 * The California site is pre-built static HTML (no database, no PHP templating needed).
 * This plugin:
 *   1. Registers rewrite rules so WordPress hands /california/... and
 *      /careers/california-physicians/... to this plugin instead of 404ing.
 *   2. Serves the matching built file from this plugin's /site/ folder.
 *   3. Serves /california assets, sitemap, robots passthrough.
 *
 * It does NOT touch any existing Colorado pages, posts, or theme.
 *
 * INSTALL
 * -------
 *   1. Copy the whole `dnm-california/` folder into wp-content/plugins/.
 *   2. Put the built site inside this plugin at: dnm-california/site/
 *      (that folder should contain `california/`, `careers/`, `assets/`, `index.html`...)
 *      Build it with:  SITE_BASE_PATH="" python3 build.py   (root-domain build)
 *      then copy the generated `public/` contents into `site/`.
 *   3. Activate the plugin in wp-admin → Plugins.
 *   4. Go to Settings → Permalinks and click "Save" once (flushes rewrite rules).
 *   5. Visit https://YOURSITE/california/  — done.
 *
 * MOVING TO A NATIVE THEME LATER
 * ------------------------------
 * This plugin is the fast path (serve the built section as-is). To make the pages
 * natively editable in the block editor, migrate each page's copy into WordPress
 * pages/ACF fields per docs/INTEGRATION.md — this plugin can be deactivated at that point.
 */

if ( ! defined( 'ABSPATH' ) ) { exit; }

define( 'DNM_CA_DIR', plugin_dir_path( __FILE__ ) );
define( 'DNM_CA_SITE', DNM_CA_DIR . 'site' );

/** Paths (relative to site root) this plugin owns. */
function dnm_ca_prefixes() {
	return array( 'california', 'careers/california-physicians', 'assets', 'robots.txt' );
}

/** Register rewrite so WordPress routes our paths to this plugin. */
add_action( 'init', function () {
	add_rewrite_rule( '^(california|careers/california-physicians|assets)(/.*)?$', 'index.php?dnm_ca=1', 'top' );
	add_rewrite_tag( '%dnm_ca%', '([0-9]+)' );
} );

add_filter( 'query_vars', function ( $vars ) {
	$vars[] = 'dnm_ca';
	return $vars;
} );

/** On activation/deactivation, flush rewrites so URLs work immediately. */
register_activation_hook( __FILE__, function () {
	add_rewrite_rule( '^(california|careers/california-physicians|assets)(/.*)?$', 'index.php?dnm_ca=1', 'top' );
	flush_rewrite_rules();
} );
register_deactivation_hook( __FILE__, 'flush_rewrite_rules' );

/** Serve the matching built file. */
add_action( 'template_redirect', function () {
	if ( ! get_query_var( 'dnm_ca' ) ) {
		// Fallback: match by request path too (in case query var didn't attach).
		$path = trim( parse_url( $_SERVER['REQUEST_URI'] ?? '', PHP_URL_PATH ), '/' );
		$owned = false;
		foreach ( dnm_ca_prefixes() as $p ) {
			if ( $path === $p || strpos( $path . '/', $p . '/' ) === 0 ) { $owned = true; break; }
		}
		if ( ! $owned ) { return; }
	}

	$path = trim( parse_url( $_SERVER['REQUEST_URI'] ?? '', PHP_URL_PATH ), '/' );

	// Map URL -> file inside /site.
	$candidate = $path;
	$full = DNM_CA_SITE . '/' . $candidate;

	// Directory-style URL (e.g. california/ or california/faq/) -> index.html
	if ( $candidate === '' || is_dir( $full ) ) {
		$full = rtrim( $full, '/' ) . '/index.html';
	} elseif ( ! pathinfo( $candidate, PATHINFO_EXTENSION ) ) {
		// no extension -> treat as directory index
		$full = $full . '/index.html';
	}

	$full = realpath( $full );

	// Security: never serve outside the plugin's site folder.
	$base = realpath( DNM_CA_SITE );
	if ( ! $full || ! $base || strpos( $full, $base ) !== 0 || ! is_file( $full ) ) {
		return; // let WordPress 404 normally
	}

	// Content types.
	$ext = strtolower( pathinfo( $full, PATHINFO_EXTENSION ) );
	$types = array(
		'html' => 'text/html; charset=UTF-8',
		'css'  => 'text/css; charset=UTF-8',
		'js'   => 'application/javascript; charset=UTF-8',
		'svg'  => 'image/svg+xml',
		'xml'  => 'application/xml; charset=UTF-8',
		'txt'  => 'text/plain; charset=UTF-8',
		'png'  => 'image/png',
		'jpg'  => 'image/jpeg',
		'jpeg' => 'image/jpeg',
		'webp' => 'image/webp',
		'ico'  => 'image/x-icon',
		'woff2'=> 'font/woff2',
	);
	$ctype = isset( $types[ $ext ] ) ? $types[ $ext ] : 'application/octet-stream';

	status_header( 200 );
	header( 'Content-Type: ' . $ctype );
	// Cache static assets, but keep HTML fresh during review.
	if ( in_array( $ext, array( 'css', 'js', 'svg', 'png', 'jpg', 'jpeg', 'webp', 'woff2', 'ico' ), true ) ) {
		header( 'Cache-Control: public, max-age=86400' );
	} else {
		header( 'Cache-Control: no-cache' );
	}

	readfile( $full );
	exit;
} );
