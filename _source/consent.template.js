/* =====================================================================
   Consentement cookies (RGPD / recommandations CNIL) + Google Consent Mode v2
   ---------------------------------------------------------------------
   - Aucun script Google (GTM, GA4) n'est chargé avant l'accord du visiteur.
   - Le choix (accepter / refuser) est mémorisé 6 mois, puis redemandé.
   - Un élément [data-cookie-settings] (ex. lien « Gestion des cookies »)
     rouvre le bandeau pour changer d'avis à tout moment.
   ===================================================================== */
(function () {
    'use strict';

    var GTM_ID = '__GTM_ID__';
    var GA_ID = '__GA_ID__';
    var STORAGE_KEY = 'cookie_consent';          // 'accept' | 'decline'
    var STORAGE_DATE_KEY = 'cookie_consent_at';  // horodatage du choix (ms)
    var MAX_AGE_MS = 1000 * 60 * 60 * 24 * 182;  // ~6 mois

    window.dataLayer = window.dataLayer || [];
    function gtag() { window.dataLayer.push(arguments); }
    window.gtag = window.gtag || gtag;

    // Consent Mode v2 : tout est refusé par défaut
    gtag('consent', 'default', {
        ad_storage: 'denied',
        ad_user_data: 'denied',
        ad_personalization: 'denied',
        analytics_storage: 'denied'
    });

    /* ─── Stockage du choix ─── */
    function readChoice() {
        try {
            var choice = localStorage.getItem(STORAGE_KEY);
            if (choice !== 'accept' && choice !== 'decline') return null;
            var at = parseInt(localStorage.getItem(STORAGE_DATE_KEY), 10);
            if (!at) {
                // Choix enregistré par l'ancien bandeau (sans date) : on le conserve à partir d'aujourd'hui
                localStorage.setItem(STORAGE_DATE_KEY, String(Date.now()));
                return choice;
            }
            return Date.now() - at > MAX_AGE_MS ? null : choice;
        } catch (e) {
            return null;
        }
    }

    function saveChoice(choice) {
        try {
            localStorage.setItem(STORAGE_KEY, choice);
            localStorage.setItem(STORAGE_DATE_KEY, String(Date.now()));
        } catch (e) { /* navigation privée : le choix vaut pour cette page */ }
    }

    /* ─── Chargement des balises Google (uniquement après accord) ─── */
    var tagsLoaded = false;

    function loadScript(src) {
        var s = document.createElement('script');
        s.async = true;
        s.src = src;
        document.head.appendChild(s);
    }

    function loadGoogleTags() {
        if (tagsLoaded) return;
        tagsLoaded = true;
        window.dataLayer.push({ 'gtm.start': new Date().getTime(), event: 'gtm.js' });
        loadScript('https://www.googletagmanager.com/gtm.js?id=' + GTM_ID);
        loadScript('https://www.googletagmanager.com/gtag/js?id=' + GA_ID);
        gtag('js', new Date());
        // Durée de vie des cookies GA limitée à 13 mois (recommandation CNIL ; 2 ans par défaut)
        gtag('config', GA_ID, { cookie_expires: 60 * 60 * 24 * 395 });
    }

    // Supprime les cookies Google Analytics déjà déposés (retrait du consentement)
    function deleteAnalyticsCookies() {
        var parts = location.hostname.split('.');
        var domains = [''];
        for (var i = 0; i < parts.length - 1; i++) {
            domains.push('; domain=.' + parts.slice(i).join('.'));
        }
        document.cookie.split(';').forEach(function (cookie) {
            var name = cookie.split('=')[0].trim();
            if (name.indexOf('_ga') !== 0 && name.indexOf('_gid') !== 0) return;
            domains.forEach(function (domain) {
                document.cookie = name + '=; Max-Age=0; path=/' + domain;
            });
        });
    }

    function applyChoice(choice) {
        if (choice === 'accept') {
            gtag('consent', 'update', { analytics_storage: 'granted' });
            loadGoogleTags();
        } else {
            gtag('consent', 'update', { analytics_storage: 'denied' });
            deleteAnalyticsCookies();
        }
    }

    /* ─── Bandeau ─── */
    var banner = null;

    function injectStyles() {
        var css =
            '#cookie-banner{position:fixed;bottom:0;left:0;right:0;z-index:9999;background:#1B2A4A;border-top:3px solid #C0392B;padding:20px 32px;box-shadow:0 -4px 24px rgba(0,0,0,.3);font-family:inherit}' +
            '#cookie-banner .vc-inner{max-width:1200px;margin:auto;display:flex;flex-wrap:wrap;align-items:center;gap:16px;justify-content:space-between}' +
            '#cookie-banner p{color:#e2e8f0;font-size:.875rem;margin:0;flex:1;min-width:260px;line-height:1.6}' +
            '#cookie-banner a{color:#fca5a5;text-decoration:underline;margin-left:4px}' +
            '#cookie-banner a:hover{color:#fff}' +
            '#cookie-banner .vc-actions{display:flex;gap:12px;flex-shrink:0}' +
            '#cookie-banner button{padding:10px 22px;border-radius:40px;font-family:inherit;font-size:.875rem;font-weight:600;cursor:pointer;transition:all .2s}' +
            '#cookie-banner .vc-decline{background:transparent;border:2px solid #64748b;color:#cbd5e1}' +
            '#cookie-banner .vc-decline:hover{border-color:#94a3b8;color:#fff}' +
            '#cookie-banner .vc-accept{background:#C0392B;border:2px solid #C0392B;color:#fff}' +
            '#cookie-banner .vc-accept:hover{background:#a93226;border-color:#a93226}' +
            '#cookie-banner button:focus-visible,#cookie-banner a:focus-visible{outline:2px solid #fff;outline-offset:2px}';
        var style = document.createElement('style');
        style.textContent = css;
        document.head.appendChild(style);
    }

    function buildBanner() {
        injectStyles();
        banner = document.createElement('div');
        banner.id = 'cookie-banner';
        banner.setAttribute('role', 'region');
        banner.setAttribute('aria-label', 'Gestion des cookies');
        banner.innerHTML =
            '<div class="vc-inner">' +
                '<p>🍪 Avec votre accord, nous utilisons des cookies de mesure d\'audience (Google Analytics) pour analyser le trafic et améliorer le site. Aucune donnée personnelle n\'est vendue. Vous pouvez modifier votre choix à tout moment.' +
                    '<a href="/mentions-legales.html#politique-cookies">En savoir plus</a></p>' +
                '<div class="vc-actions">' +
                    '<button type="button" class="vc-decline" data-choice="decline">Refuser</button>' +
                    '<button type="button" class="vc-accept" data-choice="accept">Accepter</button>' +
                '</div>' +
            '</div>';
        banner.addEventListener('click', function (e) {
            var btn = e.target.closest('button[data-choice]');
            if (!btn) return;
            var choice = btn.getAttribute('data-choice');
            saveChoice(choice);
            applyChoice(choice);
            hideBanner();
        });
        document.body.appendChild(banner);
    }

    function showBanner(focus) {
        if (!banner) buildBanner();
        banner.hidden = false;
        if (focus) banner.querySelector('button').focus();
    }

    function hideBanner() {
        if (banner) banner.hidden = true;
    }

    /* ─── Initialisation ─── */
    var choice = readChoice();
    if (choice) applyChoice(choice);

    function init() {
        if (!choice) showBanner(false);
        document.addEventListener('click', function (e) {
            if (!e.target.closest('[data-cookie-settings]')) return;
            e.preventDefault();
            showBanner(true);
        });
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();
