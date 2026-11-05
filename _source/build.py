# -*- coding: utf-8 -*-
"""Génère le site du Cabinet Valorys à la racine du dépôt  —  lancer :  python3 _source/build.py
Visuel repris à l'identique du site actuel (site.css = feuille de style d'origine).
Les informations légales à compléter sont regroupées dans CONFIG.
"""
import hashlib, html, json, os, sys
from datetime import date

SRC = os.path.dirname(os.path.abspath(__file__))      # dossier _source
ROOT = os.path.dirname(SRC)                           # racine du dépôt = racine du site
sys.path.insert(0, SRC)
from contenu import PAGES  # textes des pages services

OUT = ROOT
BASE = "https://www.cabinet-valorys.com"
YEAR = date.today().year

CONFIG = {
    "raison_sociale": "Cabinet Puxeddu",
    "nom_commercial": "Cabinet Valorys",
    "forme": "SARL",
    "capital": "10 000 €",
    "siren": "SIREN 848 361 853 – RCS Toulouse",
    "orias": "19001972",
    "page_cabinet": False,         # True = réactive l'onglet « Le cabinet » (page le-cabinet.html)
    "rcp": "AIG Europe SA, succursale pour la France, Tour CBX, 1 passerelle des Reflets, 92400 Courbevoie",
    "garantie_fi": "Non requise : le cabinet n'encaisse aucun fonds pour le compte de ses clients ou des entreprises d'assurance",
    "mediateur": "SAS CNPM – Médiation – Consommation, 27 avenue de la Libération, 42400 Saint-Chamond — cnpm-mediation-consommation.eu",
    "liens_capitalistiques": "Aucun lien capitalistique avec une entreprise d'assurance (aucune ne détient 10 % ou plus du capital du cabinet, et le cabinet ne détient aucune participation dans une entreprise d'assurance)",
    # Mesure d'audience : identifiants de TES comptes Google. Vides = aucun cookie, aucun bandeau.
    "gtm_id": None,                # ex. "GTM-XXXXXXX"
    "ga_id": None,                 # ex. "G-XXXXXXXXXX"
    "remuneration": "Commissions versées par les entreprises d'assurance et incluses dans la prime d'assurance",
}

def v(key, label):
    val = CONFIG.get(key)
    return html.escape(val) if val else f'<span class="v-todo">[À compléter : {label}]</span>'

HEAD_STYLE = open(os.path.join(SRC, "head_style.css"), encoding="utf-8").read()
LOGO = "/public/Valorys_vectoriser.webp"

# Lien de chaque carte d'expertise vers sa page
URL = {p["path"]: "/" + p["path"] for p in PAGES}

# ------------------------------------------------------------------ communs
def ver(rel):
    """Numéro de version d'un fichier (empreinte de son contenu) : force les navigateurs à recharger la nouvelle version."""
    with open(os.path.join(ROOT, rel.lstrip("/")), "rb") as f:
        return rel + "?v=" + hashlib.md5(f.read()).hexdigest()[:8]

TRACKING = bool(CONFIG["gtm_id"] or CONFIG["ga_id"])
CONSENT = ('<!-- Google Tag Manager + GA4 : chargés uniquement après consentement -->\n<script src="/public/js/consent.js" defer></script>' if TRACKING else "")

def head(title, desc, path, ld=None, noindex=False, preload_hero=False):
    url = BASE + "/" + ("" if path == "index.html" else path)
    robots = "noindex, follow" if noindex else "index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1"
    lds = "".join(f'\n<script type="application/ld+json">{json.dumps(x, ensure_ascii=False, indent=1)}</script>' for x in (ld or []))
    hero = '<link rel="preload" as="image" href="/public/Hero-Valo.avif" type="image/avif" fetchpriority="high" media="(min-width: 1024px)">\n' if preload_hero else ""
    t, d = html.escape(title), html.escape(desc)
    return f"""<!DOCTYPE html>
<html class="scroll-smooth" lang="fr-FR">
<head>
<meta charset="utf-8">
<meta content="width=device-width, initial-scale=1.0" name="viewport">
<script>document.documentElement.classList.add('js');</script>
{CONSENT}
<title>{t}</title>
<meta name="description" content="{d}">
<meta name="robots" content="{robots}">
<meta name="author" content="Cabinet Valorys">
<meta name="geo.region" content="FR-31">
<meta name="geo.placename" content="Toulouse">
<meta name="geo.position" content="43.598;1.449">
<meta name="ICBM" content="43.598, 1.449">
<meta name="theme-color" content="#041534">
<meta name="format-detection" content="telephone=yes">
<link rel="canonical" href="{url}">
<link rel="icon" href="/favicon.ico" sizes="48x48">
<link rel="icon" type="image/png" sizes="192x192" href="/public/icons/icon-192.png">
<link rel="apple-touch-icon" href="/public/icons/apple-touch-icon.png">
<link rel="manifest" href="/public/site.webmanifest">
<meta property="og:type" content="website">
<meta property="og:locale" content="fr_FR">
<meta property="og:site_name" content="Cabinet Valorys">
<meta property="og:title" content="{t}">
<meta property="og:description" content="{d}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{BASE}/public/valorys_og_image_1200x630.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{t}">
<meta name="twitter:description" content="{d}">
<meta name="twitter:image" content="{BASE}/public/valorys_og_image_1200x630.jpg">
{hero}<link rel="preload" as="font" type="font/woff2" href="/public/fonts/manrope-latin.woff2?v=101877a7" crossorigin>
<link rel="preload" as="font" type="font/woff2" href="/public/fonts/dm-serif-display-latin.woff2?v=436ae2f1" crossorigin>
<style>{HEAD_STYLE}</style>
<link rel="stylesheet" href="{ver('/public/css/site.css')}">
<link rel="stylesheet" href="{ver('/public/css/extra.css')}">{lds}
</head>
<body class="bg-background text-on-surface font-body selection:bg-secondary selection:text-white">
"""

NAV_SVC = [(q["path"], q["name"]) for q in PAGES] + [("assurance-emprunteur.html", "Assurance emprunteur")]
# Menu « Notre expertise » : mêmes titres et mêmes contrats que les cartes de l'accueil
NAV_CARTES = {
    "protection-entreprise.html": ("Sécuriser votre entreprise", "RC Pro · Multirisque · Décennale · Protection juridique"),
    "epargne-entreprise.html": ("Fidéliser vos salariés", "PEE · PEI · PERECO · IFC"),
    "prevoyance-sante.html": ("Protéger votre famille", "Prévoyance · Santé · Individuelle &amp; collective"),
    "epargne-retraite.html": ("Valoriser votre épargne", "Assurance vie · PER · Capitalisation"),
    "bilan-retraite.html": ("Préparer votre avenir", "Bilan retraite · Audit patrimonial"),
    "assurance-emprunteur.html": ("Assurer votre prêt immobilier", "Assurance emprunteur · Loi Lemoine"),
}
def nav_item(path, extra=""):
    t, c = NAV_CARTES[path]
    return f'<a{extra} href="/{path}"><span class="v-nav-t">{t}</span><span class="v-nav-c">{c}</span></a>'

def nav(home=True):
    p = "" if home else "/"
    acc = "#" if home else "/"
    link = lambda href, lab: f'''            <a class="nav-link text-white font-body font-medium hover:text-secondary transition-colors duration-200 relative group" href="{href}">
                {lab}
                <span class="absolute -bottom-1 left-0 w-0 h-0.5 bg-secondary transition-all duration-300 group-hover:w-full"></span>
            </a>'''
    mob = lambda href, lab: f'<a class="text-white font-body text-lg hover:text-secondary transition-colors" href="{href}" onclick="closeMenu()">{lab}</a>'
    return f"""
<!-- ===== TOP NAV ===== -->
<nav id="navbar" class="fixed top-0 w-full z-50 bg-slate-950/85 backdrop-blur-xl px-8 py-6 max-w-full mx-auto">
    <div class="flex justify-between items-center">
        <a href="/" class="flex items-center">
            <img src="{LOGO}" alt="Cabinet Valorys - Courtier en assurance à Toulouse" width="221" height="55" fetchpriority="high" decoding="async" class="h-[55px] w-auto" style="filter: brightness(0) invert(1);">
        </a>
        <div class="hidden md:flex items-center gap-8">
{link(acc, "Accueil")}
            <div class="v-dd">
{link(p + "#solutions", "Notre expertise")}
                <div class="v-dd-panel" role="menu">{"".join(nav_item(x[0], ' role="menuitem"') for x in NAV_SVC)}</div>
            </div>
{link("/le-cabinet.html", "Le cabinet") if CONFIG["page_cabinet"] else link(p + "#about", "Qui sommes-nous")}
{link(p + "#pourquoi", "Pourquoi nous")}
            <a href="{p}#contact" class="bg-secondary text-on-secondary px-6 py-3 font-headline font-bold rounded-[40px] hover:scale-95 transition-all duration-200 ease-in-out">
                Contact
            </a>
        </div>
        <div class="flex items-center gap-4">
            <button id="hamburger" type="button" class="md:hidden text-white p-2 focus:outline-none" aria-label="Menu" aria-controls="mobile-menu" aria-expanded="false">
                <span id="hamburger-icon" class="material-symbols-outlined text-3xl" aria-hidden="true">menu</span>
            </button>
        </div>
    </div>
    <div id="mobile-menu">
        <div class="flex flex-col gap-5 pt-6 pb-4 border-t border-white/10 mt-4">
            {mob(acc, "Accueil")}
            {mob(p + "#solutions", "Notre expertise")}
            <div class="v-mob-sub">{"".join(nav_item(x[0], ' onclick="closeMenu()"') for x in NAV_SVC)}</div>
            {mob("/le-cabinet.html", "Le cabinet") if CONFIG["page_cabinet"] else mob(p + "#about", "Qui sommes-nous")}
            {mob(p + "#pourquoi", "Pourquoi nous")}
            <a href="{p}#contact" onclick="closeMenu()" class="bg-secondary text-white px-6 py-3 font-body font-bold rounded-[40px] hover:scale-95 transition-all duration-200 w-full mt-2 text-center">
                Contact
            </a>
        </div>
    </div>
</nav>
"""

OPTIONS = [
    ("Protection de l'entreprise", ["Responsabilité Civile Professionnelle", "Multirisque Professionnelle", "RC Décennale", "Protection du dirigeant"]),
    ("Protection des personnes", ["Prévoyance individuelle", "Santé individuelle", "Prévoyance & santé collective"]),
    ("Épargne salariale & engagements sociaux", ["Épargne salariale (PEE, PEI, PERECO)", "Intéressement & participation", "PER d'entreprise", "IFC (Indemnités de Fin de Carrière)"]),
    ("Épargne & retraite", ["Assurance vie", "Plan d'épargne retraite (PER)"]),
    ("Bilan & conseil", ["Bilan retraite & audit patrimonial"]),
    ("Financement", ["Assurance emprunteur", "Changer mon assurance de prêt en cours"]),
    ("", ["Autre / consultation générale"]),
]

def contact(selected=""):
    groups = ""
    for g, opts in OPTIONS:
        o = "".join(f'<option{" selected" if x == selected else ""}>{html.escape(x)}</option>' for x in opts)
        groups += f'<optgroup label="• {html.escape(g)} •">{o}</optgroup>' if g else f'<optgroup label="•">{o}</optgroup>'
    sel_default = "" if selected else ' selected="selected"'
    return f"""
<!-- ===== CONTACT ===== -->
<section class="bg-primary pt-24 pb-32" id="contact">
    <div class="container mx-auto px-8">
        <div class="bg-white rounded-none flex flex-col lg:flex-row overflow-hidden shadow-2xl reveal">
            <div class="lg:w-1/3 bg-secondary p-12 lg:p-16 flex flex-col justify-between">
                <div>
                    <h2 class="font-headline font-black text-3xl md:text-4xl text-white mb-8 uppercase leading-none">Parlons de votre projet.</h2>
                    <div class="space-y-8 mt-12">
                        <div class="flex items-start gap-4">
                            <span class="material-symbols-outlined text-white" aria-hidden="true">location_on</span>
                            <div>
                                <p class="text-white font-bold uppercase tracking-widest text-xs mb-1">Bureau</p>
                                <p class="text-white/80">13 Port Saint-Étienne<br>31000 TOULOUSE</p>
                            </div>
                        </div>
                        <div class="flex items-start gap-4">
                            <span class="material-symbols-outlined text-white" aria-hidden="true">phone_in_talk</span>
                            <div>
                                <p class="text-white font-bold uppercase tracking-widest text-xs mb-1">Ligne directe</p>
                                <p class="text-white/80"><a href="tel:+33669945608" class="hover:text-white hover:underline underline-offset-4">06 69 94 56 08</a></p>
                            </div>
                        </div>
                        <div class="flex items-start gap-4">
                            <span class="material-symbols-outlined text-white" aria-hidden="true">mail</span>
                            <div>
                                <p class="text-white font-bold uppercase tracking-widest text-xs mb-1">Email</p>
                                <p class="text-white/80"><a href="mailto:contact@cabinet-valorys.com" class="hover:text-white hover:underline underline-offset-4">contact@cabinet-valorys.com</a></p>
                            </div>
                        </div>
                        <div class="flex items-start gap-4">
                            <span class="material-symbols-outlined text-white" aria-hidden="true">schedule</span>
                            <div>
                                <p class="text-white font-bold uppercase tracking-widest text-xs mb-1">Horaires</p>
                                <p class="text-white/80">Lun – Ven : 9h00 – 20h00<br>Sam : 9h00 – 13h00</p>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="pt-12">
                    <div class="flex gap-4">
                        <a href="https://www.linkedin.com/in/michael-puxeddu-17773918a/" target="_blank" rel="noopener" aria-label="LinkedIn de Michaël Puxeddu" class="w-10 h-10 border border-white/30 rounded-full flex items-center justify-center text-white hover:bg-white hover:text-secondary transition-all cursor-pointer">
                            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433a2.062 2.062 0 0 1-2.063-2.065 2.064 2.064 0 1 1 2.063 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"></path></svg>
                        </a>
                    </div>
                </div>
            </div>
            <div class="lg:w-2/3 p-12 lg:p-16 bg-white">
                <div class="v-tabs" role="tablist" aria-label="Type de contact">
                    <button type="button" role="tab" id="tab-rappel" aria-controls="panel-rappel" aria-selected="true" data-tab="rappel">Être rappelé</button>
                    <button type="button" role="tab" id="tab-message" aria-controls="panel-message" aria-selected="false" data-tab="message">Écrire un message</button>
                </div>
                <form id="callback-form" class="space-y-8" novalidate role="tabpanel" aria-labelledby="tab-rappel" data-panel="rappel">
                    <p class="v-tab-intro">Laissez votre numéro : nous vous rappelons dans la journée ouvrée, au moment qui vous arrange.</p>
                    <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
                        <div class="relative group">
                            <label for="cb-name" class="block text-primary font-headline font-extrabold uppercase text-xs tracking-widest mb-2">Prénom <span class="text-secondary">*</span></label>
                            <input id="cb-name" name="firstname" required maxlength="60" autocomplete="given-name" class="w-full bg-surface-container-highest border-none p-4 font-body focus:ring-2 focus:ring-primary/40 transition-all rounded-[20px]" placeholder="Votre prénom" type="text">
                        </div>
                        <div class="relative group">
                            <label for="cb-lastname" class="block text-primary font-headline font-extrabold uppercase text-xs tracking-widest mb-2">Nom <span class="text-secondary">*</span></label>
                            <input id="cb-lastname" name="lastname" required maxlength="60" autocomplete="family-name" class="w-full bg-surface-container-highest border-none p-4 font-body focus:ring-2 focus:ring-primary/40 transition-all rounded-[20px]" placeholder="Votre nom" type="text">
                        </div>
                    </div>
                    <div class="grid grid-cols-1 gap-8">
                        <div class="relative group">
                            <label for="cb-phone" class="block text-primary font-headline font-extrabold uppercase text-xs tracking-widest mb-2">Téléphone <span class="text-secondary">*</span></label>
                            <input id="cb-phone" name="phone" required autocomplete="tel" inputmode="tel" class="w-full bg-surface-container-highest border-none p-4 font-body focus:ring-2 focus:ring-primary/40 transition-all rounded-[20px]" placeholder="06 00 00 00 00" type="tel">
                        </div>
                    </div>
                    <fieldset class="v-slots"><legend class="block text-primary font-headline font-extrabold uppercase text-xs tracking-widest mb-2">Créneau préféré</legend>
                        <label><input type="radio" name="slot" value="Matin (9h – 12h)" checked> Matin</label>
                        <label><input type="radio" name="slot" value="Midi (12h – 14h)"> Midi</label>
                        <label><input type="radio" name="slot" value="Après-midi (14h – 18h)"> Après-midi</label>
                        <label><input type="radio" name="slot" value="Soir (18h – 20h)"> Soir</label>
                    </fieldset>
                    <input type="hidden" id="cb-type" value="{html.escape(selected or "Demande de rappel")}">
                    <div class="sr-only" aria-hidden="true"><label for="cb-website">Ne pas remplir ce champ</label><input id="cb-website" type="text" tabindex="-1" autocomplete="off"></div>
                    <label class="v-consent" for="cb-consent"><input id="cb-consent" type="checkbox" required> <span>J'accepte d'être rappelé par le Cabinet Valorys au sujet de ma demande. <span class="text-secondary">*</span></span></label>
                    <div id="cb-feedback" class="hidden rounded-[20px] p-4 text-sm font-body font-semibold" role="status" aria-live="polite"></div>
                    <button id="cb-submit" type="submit" class="bg-primary text-white font-headline font-black text-xl py-6 px-12 uppercase tracking-tighter hover:bg-secondary transition-colors duration-300 w-full md:w-auto rounded-[40px] flex items-center justify-center gap-3 disabled:opacity-60 disabled:cursor-not-allowed">
                        <span id="cb-btn-label">Me faire rappeler</span>
                    </button>
                    <p class="v-form-legal">Votre numéro sert uniquement à vous rappeler au sujet de votre demande. <a href="/mentions-legales.html#politique-confidentialite">Politique de confidentialité</a>.</p>
                </form>
                <form id="contact-form" class="space-y-8" novalidate role="tabpanel" aria-labelledby="tab-message" data-panel="message" hidden>
                    <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
                        <div class="relative group">
                            <label for="cf-name" class="block text-primary font-headline font-extrabold uppercase text-xs tracking-widest mb-2">Nom complet <span class="text-secondary">*</span></label>
                            <input id="cf-name" name="name" required minlength="2" maxlength="100" autocomplete="name" class="w-full bg-surface-container-highest border-none p-4 font-body focus:ring-2 focus:ring-primary/40 transition-all rounded-[20px]" placeholder="Prénom Nom" type="text">
                        </div>
                        <div class="relative group">
                            <label for="cf-email" class="block text-primary font-headline font-extrabold uppercase text-xs tracking-widest mb-2">Adresse e-mail <span class="text-secondary">*</span></label>
                            <input id="cf-email" name="email" required maxlength="150" autocomplete="email" inputmode="email" class="w-full bg-surface-container-highest border-none p-4 font-body focus:ring-2 focus:ring-primary/40 transition-all rounded-[20px]" placeholder="contact@entreprise.fr" type="email">
                        </div>
                    </div>
                    <div class="relative group">
                        <label for="cf-phone" class="block text-primary font-headline font-extrabold uppercase text-xs tracking-widest mb-2">Téléphone</label>
                        <input id="cf-phone" name="phone" autocomplete="tel" inputmode="tel" class="w-full bg-surface-container-highest border-none p-4 font-body focus:ring-2 focus:ring-primary/40 transition-all rounded-[20px]" placeholder="+33 6 00 00 00 00" type="tel">
                    </div>
                    <div class="relative group">
                        <label for="cf-type" class="block text-primary font-headline font-extrabold uppercase text-xs tracking-widest mb-2">Type de demande</label>
                        <select id="cf-type" name="request_type" class="w-full bg-surface-container-highest border-none p-4 font-body focus:ring-2 focus:ring-primary/40 transition-all rounded-[20px]">
                            <option value=""{sel_default}>• Sélectionnez votre besoin •</option>{groups}
                        </select>
                    </div>
                    <div class="relative group">
                        <label for="cf-message" class="block text-primary font-headline font-extrabold uppercase text-xs tracking-widest mb-2">Message</label>
                        <textarea id="cf-message" name="message" maxlength="2000" class="w-full bg-surface-container-highest border-none p-4 font-body focus:ring-2 focus:ring-primary/40 transition-all rounded-[20px]" placeholder="Décrivez votre situation et vos besoins en assurance..." rows="4"></textarea>
                    </div>
                    <div class="sr-only" aria-hidden="true">
                        <label for="cf-website">Ne pas remplir ce champ</label>
                        <input id="cf-website" name="website" type="text" tabindex="-1" autocomplete="off">
                    </div>
                    <label class="v-consent" for="cf-consent"><input id="cf-consent" type="checkbox" required> <span>J'accepte que mes données soient utilisées par le Cabinet Valorys pour me recontacter au sujet de ma demande. <span class="text-secondary">*</span></span></label>
                    <div id="cf-feedback" class="hidden rounded-[20px] p-4 text-sm font-body font-semibold" role="status" aria-live="polite"></div>
                    <button id="cf-submit" type="submit" class="bg-primary text-white font-headline font-black text-xl py-6 px-12 uppercase tracking-tighter hover:bg-secondary transition-colors duration-300 w-full md:w-auto rounded-[40px] flex items-center justify-center gap-3 disabled:opacity-60 disabled:cursor-not-allowed">
                        <span id="cf-btn-label">Envoyer la demande</span>
                        <svg id="cf-spinner" class="hidden animate-spin w-5 h-5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8z"></path></svg>
                    </button>
                    <p class="v-form-legal">Vos données sont destinées au seul Cabinet Valorys pour traiter votre demande, et conservées 3 ans au plus si aucune suite n'y est donnée. Vous pouvez y accéder, les rectifier ou les faire effacer en écrivant à contact@cabinet-valorys.com. <a href="/mentions-legales.html#politique-confidentialite">Politique de confidentialité</a>.</p>
                </form>
            </div>
        </div>
    </div>
</section>
"""

def footer():
    svc = "".join(f'<a href="/{p["path"]}">{html.escape(p["name"])}</a>' for p in PAGES) + '<a href="/assurance-emprunteur.html">Assurance emprunteur</a>'
    foot_link = "text-slate-400 font-body text-sm uppercase tracking-widest hover:text-secondary underline decoration-2 underline-offset-4 transition-all opacity-80 hover:opacity-100"
    return f"""
<!-- ===== FOOTER ===== -->
<footer class="bg-slate-950 flex flex-col px-12 py-16 w-full border-t-4 border-secondary">
    <div class="flex flex-col md:flex-row justify-between items-center w-full">
        <div class="mb-8 md:mb-0">
            <img src="{LOGO}" alt="Cabinet Valorys" width="129" height="32" loading="lazy" decoding="async" class="h-8 w-auto" style="filter: brightness(0) invert(1);">
            <p class="text-slate-400 font-body text-sm uppercase tracking-widest mt-2">© {YEAR} Cabinet Valorys.</p>
        </div>
        <div class="flex flex-wrap justify-center gap-8">
            <a class="{foot_link}" href="/mentions-legales.html#politique-confidentialite">Politique de confidentialité</a>
            <a class="{foot_link}" href="/mentions-legales.html">Mentions légales</a>
            <a class="{foot_link}" href="/mentions-legales.html#reclamations">Réclamations</a>
            {'<button type="button" data-cookie-settings class="' + foot_link + '">Gestion des cookies</button>' if TRACKING else ''}
        </div>
    </div>
    <nav class="v-foot-services" aria-label="Nos expertises">{svc}</nav>
    <div class="w-full mt-10 pt-6 border-t border-slate-800/60">
        <p class="text-slate-400 font-body text-xs leading-relaxed max-w-5xl mx-auto text-center">
            {CONFIG["nom_commercial"]} — Courtier d'assurance immatriculé à l'ORIAS sous le n° <a href="https://www.orias.fr/" target="_blank" rel="noopener noreferrer" class="underline hover:text-secondary">{CONFIG["orias"]}</a> (www.orias.fr) — Membre de la CNCEF Assurance. Activité soumise au contrôle de l'Autorité de Contrôle Prudentiel et de Résolution (ACPR) — 4 Place de Budapest, CS 92459, 75436 Paris Cedex 09. <a href="/mentions-legales.html#reclamations" class="underline hover:text-secondary">Réclamations et médiation</a>.
        </p>
    </div>
</footer>

<div class="v-actionbar" role="navigation" aria-label="Contact rapide">
    <a href="tel:+33669945608"><span class="material-symbols-outlined" aria-hidden="true">call</span>Appeler</a>
    <a href="#contact" data-open-tab="rappel" class="v-ab-main"><span class="material-symbols-outlined" aria-hidden="true">schedule</span>Être rappelé</a>
</div>
<a href="tel:+33669945608" class="v-fab fixed bottom-6 right-6 z-50 bg-secondary text-white w-14 h-14 rounded-[30px] shadow-lg shadow-secondary/40 flex items-center justify-center hover:scale-110 active:scale-95 transition-transform duration-200" aria-label="Appeler Valorys">
    <span class="material-symbols-outlined text-2xl" aria-hidden="true">call</span>
</a>
<script src="{ver('/public/js/site.js')}"></script>
</body>
</html>
"""

def more(label="En savoir plus"):
    return f'<span class="v-more">{label} <span class="material-symbols-outlined" aria-hidden="true">arrow_forward</span></span>'

# ------------------------------------------------------------------ accueil
REASSURE = f'''<ul class="v-reassure hero-cta">
                <li><span class="material-symbols-outlined" aria-hidden="true">verified_user</span>Courtier ORIAS n° {CONFIG["orias"]}</li>
                <li><span class="material-symbols-outlined" aria-hidden="true">compare_arrows</span>60+ compagnies comparées</li>
                <li><span class="material-symbols-outlined" aria-hidden="true">phone_in_talk</span>Ligne directe 06 69 94 56 08</li>
            </ul>'''

LD_HOME = {
  "@context": "https://schema.org",
  "@graph": [
    {"@type": "InsuranceAgency", "@id": BASE + "/#organization", "name": "Cabinet Valorys", "alternateName": "Valorys",
     "legalName": CONFIG["raison_sociale"], "url": BASE + "/",
     "logo": {"@type": "ImageObject", "url": BASE + LOGO, "width": 1001, "height": 249},
     "image": BASE + "/public/Hero-Valo.png", "telephone": "+33669945608", "email": "contact@cabinet-valorys.com", "priceRange": "€€",
     "identifier": [{"@type": "PropertyValue", "name": "ORIAS", "value": CONFIG["orias"], "url": "https://www.orias.fr/"}],
     "address": {"@type": "PostalAddress", "streetAddress": "13 Port Saint-Étienne", "postalCode": "31000", "addressLocality": "Toulouse", "addressRegion": "Occitanie", "addressCountry": "FR"},
     "geo": {"@type": "GeoCoordinates", "latitude": 43.598, "longitude": 1.449},
     "openingHoursSpecification": [
        {"@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"], "opens": "09:00", "closes": "20:00"},
        {"@type": "OpeningHoursSpecification", "dayOfWeek": "Saturday", "opens": "09:00", "closes": "13:00"}],
     "areaServed": [{"@type": "City", "name": "Toulouse"}, {"@type": "AdministrativeArea", "name": "Haute-Garonne"}, {"@type": "AdministrativeArea", "name": "Occitanie"}],
     "knowsAbout": ["Assurance professionnelle", "Responsabilité civile professionnelle", "RC décennale", "Prévoyance", "Mutuelle santé",
                    "Plan d'épargne retraite", "Assurance vie", "Indemnités de fin de carrière", "PER d'entreprise", "Bilan retraite", "Assurance emprunteur"],
     "sameAs": ["https://www.linkedin.com/in/michael-puxeddu-17773918a/"],
     "founder": {"@id": BASE + "/#founder"}},
    {"@type": "Person", "@id": BASE + "/#founder", "name": "Michaël Puxeddu", "jobTitle": "Courtier en assurances, fondateur du Cabinet Valorys",
     "image": BASE + "/public/PUXEDDU-Michael.webp", "worksFor": {"@id": BASE + "/#organization"},
     "sameAs": ["https://www.linkedin.com/in/michael-puxeddu-17773918a/"]},
    {"@type": "WebSite", "@id": BASE + "/#website", "url": BASE + "/", "name": "Cabinet Valorys", "inLanguage": "fr-FR", "publisher": {"@id": BASE + "/#organization"}}
  ]
}

def index():
    return head("Courtier en assurance et gestion de patrimoine à Toulouse | Cabinet Valorys",
                "Cabinet Valorys, courtier indépendant à Toulouse : prévoyance, mutuelle santé, retraite et assurance des professionnels. Plus de 60 compagnies comparées pour votre sérénité.",
                "index.html", [LD_HOME], preload_hero=True) + nav(True) + f"""
<!-- ===== HERO ===== -->
<section class="relative h-screen overflow-hidden bg-architectural">
    <div class="absolute inset-0 z-[3] opacity-20 pointer-events-none" aria-hidden="true">
        <img alt="" role="presentation" width="512" height="512" decoding="async" loading="eager" class="w-full h-full object-cover" src="/public/hero-texture.webp">
    </div>
    <div class="v-hero-mob" aria-hidden="true"><img src="/public/Hero-Valo-mobile.webp" alt="" width="800" height="835" decoding="async" loading="eager"></div>
    <div class="hidden lg:block absolute inset-0 z-[1]">
        <picture>
            <source type="image/avif" srcset="/public/Hero-Valo.avif 1x">
            <source type="image/webp" srcset="/public/Hero-Valo.webp 1x">
            <img src="/public/Hero-Valo.png" alt="" role="presentation" width="1376" height="768" fetchpriority="high" loading="eager" decoding="async" class="absolute inset-0 w-full h-full object-cover object-right">
        </picture>
        <div class="absolute inset-0" style="background: linear-gradient(to right, #041534 0%, #041534 20%, rgba(4,21,52,0.95) 35%, rgba(4,21,52,0.7) 50%, rgba(4,21,52,0.2) 70%, transparent 100%);"></div>
        <div class="absolute inset-0" style="background: linear-gradient(to bottom, rgba(4,21,52,0.5) 0%, transparent 20%, transparent 80%, rgba(4,21,52,0.4) 100%);"></div>
    </div>
    <div class="relative z-10 h-full flex items-center pt-24 pb-16 px-8 md:pl-[8%] lg:pl-[12%]">
        <div>
            <div class="hero-badge flex items-center gap-3 mb-6">
                <span class="block w-8 h-px bg-secondary"></span>
                <span class="text-secondary font-body uppercase tracking-widest text-xs">Courtier en assurance &amp; gestion de patrimoine à Toulouse</span>
            </div>
            <h1 class="hero-title text-5xl lg:text-6xl text-white leading-tight mb-6 drop-shadow-2xl" style="font-family:'DM Serif Display',serif;">
                Votre avenir mérite<br>
                <span class="text-transparent bg-clip-text bg-gradient-to-r from-[#C0392B] to-red-400">les meilleures solutions.</span>
            </h1>
            <p class="hero-subtitle text-slate-300 text-base md:text-lg max-w-lg font-medium leading-relaxed mb-10">
                Nous accompagnons particuliers, professionnels et entreprises avec une approche indépendante : protection sociale, épargne, retraite et gestion de patrimoine.
            </p>
            <div class="hero-cta flex flex-col sm:flex-row items-start gap-6">
                <a href="#contact" class="bg-secondary text-white px-8 py-4 font-body font-semibold text-base rounded-[40px] hover:brightness-110 hover:scale-[1.02] transition-all duration-200">Demander une étude gratuite</a>
                <a href="#solutions" class="text-white font-body font-medium text-base border border-transparent px-8 py-4 rounded-[40px] bg-transparent hover:bg-white/15 hover:border-white/50 transition-all duration-300">Découvrir nos solutions</a>
            </div>
        </div>
    </div>
</section>

<!-- ===== EXPERTISES ===== -->
<section class="py-24 bg-surface" id="solutions">
    <div class="container mx-auto px-8">
        <div class="flex flex-col md:flex-row justify-between items-end mb-16 gap-8 reveal">
            <div class="max-w-2xl">
                <h2 class="font-headline font-black text-3xl md:text-5xl tracking-tight text-primary uppercase mb-4">Notre expertise</h2>
                <div class="h-1.5 w-24 bg-secondary"></div>
            </div>
            <p class="font-body text-on-surface-variant max-w-md text-lg">
                Parce que chaque situation est unique, nous concevons des solutions sur mesure, comparées et optimisées auprès de plus de 60 partenaires assureurs.
            </p>
        </div>
        <div class="grid grid-cols-1 md:grid-cols-12 gap-6 v-bento">

            <a href="{URL['protection-entreprise.html']}" class="v-card-link md:col-span-8 group relative overflow-hidden bg-primary-container rounded-xl reveal stagger-1 v-card-hero">
                <img alt="" role="presentation" width="512" height="512" loading="lazy" decoding="async" class="absolute inset-0 w-full h-full object-cover opacity-50 group-hover:scale-105 transition-transform duration-700" src="/public/conseil-entreprise.webp">
                <div class="absolute inset-0 bg-gradient-to-t from-primary via-transparent to-transparent"></div>
                <div class="absolute bottom-0 left-0 p-10">
                    <span class="v-card-ico v-ico-dark"><span class="material-symbols-outlined" aria-hidden="true">domain</span></span>
                    <span class="v-card-tag v-card-tag-dark">RC Pro · Multirisque · Décennale · Protection juridique</span>
                    <h3 class="font-headline font-extrabold text-3xl text-white mb-4">Sécuriser votre entreprise</h3>
                    <p class="text-slate-300 max-w-md font-medium">Un sinistre, un litige client ou votre absence ne doivent pas mettre votre activité en péril. Nous adaptons chaque garantie à votre métier : professions libérales, artisans, commerçants et entreprises.</p>
                    {more()}
                </div>
            </a>

            <a href="{URL['epargne-entreprise.html']}" class="v-card-link v-card-light md:col-span-4 group relative overflow-hidden bg-white rounded-xl border-l-8 border-secondary reveal stagger-2">
                <div class="p-10 flex flex-col h-full justify-between">
                    <div>
                        <span class="v-card-ico"><span class="material-symbols-outlined" aria-hidden="true">group</span></span>
                        <span class="v-card-tag">PEE · PEI · PERECO · IFC</span>
                    <h3 class="font-headline font-extrabold text-2xl text-primary mb-4">Fidéliser vos salariés</h3>
                        <p class="text-on-surface-variant">Partager la valeur créée, attirer et fidéliser vos collaborateurs, anticiper le coût des départs à la retraite : dans un cadre social et fiscal avantageux pour l'entreprise comme pour les salariés.</p>
                        {more()}
                    </div>
                </div>
                <div class="v-card-mark" aria-hidden="true"><span class="material-symbols-outlined">group</span></div>
            </a>

            <a href="{URL['prevoyance-sante.html']}" class="v-card-link md:col-span-4 group relative overflow-hidden bg-primary rounded-xl reveal stagger-3">
                <div class="p-10 relative z-10">
                    <span class="v-card-ico v-ico-dark"><span class="material-symbols-outlined" aria-hidden="true">health_and_safety</span></span>
                    <span class="v-card-tag v-card-tag-dark">Prévoyance · Santé · Individuelle &amp; collective</span>
                    <h3 class="font-headline font-extrabold text-2xl text-white mb-4">Protéger votre famille</h3>
                    <p class="text-slate-400">Maintenir votre niveau de vie face aux aléas, assurer l'avenir de vos proches et bénéficier d'une couverture santé adaptée, pour votre famille comme pour vos salariés.</p>
                    {more()}
                </div>
                <div class="absolute -bottom-10 -right-10 opacity-10 scale-100 md:scale-150 text-white" aria-hidden="true">
                    <span class="material-symbols-outlined text-[100px] md:text-[200px]">favorite</span>
                </div>
            </a>

            <a href="{URL['epargne-retraite.html']}" class="v-card-link v-card-light md:col-span-4 group relative overflow-hidden bg-white rounded-xl reveal stagger-4">
                <div class="p-10">
                    <span class="v-card-ico"><span class="material-symbols-outlined" aria-hidden="true">savings</span></span>
                    <span class="v-card-tag">Assurance vie · PER · Capitalisation</span>
                    <h3 class="font-headline font-extrabold text-2xl text-primary mb-4">Valoriser votre épargne</h3>
                    <p class="text-on-surface-variant">Faire travailler votre épargne, alléger votre fiscalité et transmettre à vos proches dans les meilleures conditions.</p>
                    {more()}
                </div>
                <div class="v-card-mark" aria-hidden="true"><span class="material-symbols-outlined">savings</span></div>
            </a>

            <a href="{URL['bilan-retraite.html']}" class="v-card-link v-card-light md:col-span-4 group relative overflow-hidden bg-white rounded-xl reveal stagger-4">
                <div class="p-10">
                    <span class="v-card-ico"><span class="material-symbols-outlined" aria-hidden="true">account_balance</span></span>
                    <span class="v-card-tag">Bilan retraite · Audit patrimonial</span>
                    <h3 class="font-headline font-extrabold text-2xl text-primary mb-4">Préparer votre avenir</h3>
                    <p class="text-on-surface-variant">Anticiper votre retraite et vos revenus futurs, développer votre patrimoine à partir d'un bilan complet et d'une stratégie sur mesure.</p>
                    {more()}
                </div>
                <div class="v-card-mark" aria-hidden="true"><span class="material-symbols-outlined">account_balance</span></div>
            </a>

            <a href="/assurance-emprunteur.html" class="v-card-link v-emp-card group relative overflow-hidden bg-primary rounded-xl border-l-8 border-secondary reveal">
                <div class="v-emp-inner relative z-10">
                    <div class="v-emp-text">
                        <span class="v-card-ico v-ico-dark"><span class="material-symbols-outlined" aria-hidden="true">real_estate_agent</span></span>
                        <span class="v-card-tag v-card-tag-dark">Assurance emprunteur · Loi Lemoine</span>
                    <h3 class="font-headline font-extrabold text-2xl text-white mb-4">Assurer votre prêt immobilier</h3>
                        <p class="text-slate-300">Nouveau crédit ou prêt en cours : vous pouvez changer d'assurance à tout moment, sans frais. Nous comparons les garanties à niveau équivalent et gérons toutes les démarches avec votre banque, jusqu'à son accord.</p>
                        {more()}
                    </div>
                    <ul class="v-emp-points">
                        <li><strong>À tout moment</strong><span>dès la signature ou en cours de prêt</span></li>
                        <li><strong>Mêmes garanties</strong><span>équivalentes à celles exigées par votre banque</span></li>
                        <li><strong>Sans frais</strong><span>étude et démarches offertes</span></li>
                    </ul>
                </div>
                <div class="absolute -bottom-10 -right-10 opacity-10 scale-100 md:scale-150 text-white" aria-hidden="true">
                    <span class="material-symbols-outlined text-[100px] md:text-[200px]">key</span>
                </div>
            </a>
        </div>
    </div>
</section>

<!-- ===== QUI SOMMES-NOUS ===== -->
<section class="py-32 bg-primary relative overflow-hidden" id="about">
    <div class="container mx-auto px-8 relative z-10">
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-20 items-center">
            <div class="relative reveal-left">
                <div class="absolute -top-12 -left-12 w-48 h-48 border-t-8 border-l-8 border-secondary opacity-50"></div>
                <img alt="Michaël Puxeddu, fondateur du Cabinet Valorys à Toulouse" width="341" height="512" loading="lazy" decoding="async" class="rounded-none shadow-2xl relative z-10 grayscale hover:grayscale-0 transition-all duration-700 w-4/5 object-cover mx-auto block" src="/public/PUXEDDU-Michael.webp">
            </div>
            <div class="reveal-right">
                <h2 class="font-headline font-black text-3xl md:text-5xl lg:text-6xl text-white mb-8 leading-tight tracking-tighter">
                    Une expertise de proximité.<br>
                    <span class="text-secondary">Une vision globale.</span>
                </h2>
                <p class="text-slate-300 text-xl font-medium mb-12 leading-relaxed">
                    Depuis plus de 15 ans, nous accompagnons nos clients avec une conviction : chaque situation mérite une attention particulière et des solutions à la hauteur de ses enjeux.<br>Notre indépendance et notre accès à plus de 60 partenaires nous permettent de sélectionner, en toute objectivité, des solutions sur mesure, pensées pour répondre à vos exigences et préserver vos intérêts.
                </p>
                <div class="grid grid-cols-2 gap-8">
                    <div class="border-l-4 border-secondary pl-6">
                        <span class="block text-4xl font-headline font-black text-white mb-2"><span class="counter" data-target="15" data-suffix="+">15+</span></span>
                        <span class="text-slate-400 font-bold uppercase tracking-widest text-sm">Années d'expertise</span>
                    </div>
                    <div class="border-l-4 border-secondary pl-6">
                        <span class="block text-4xl font-headline font-black text-white mb-2"><span class="counter" data-target="60" data-suffix="+">60+</span></span>
                        <span class="text-slate-400 font-bold uppercase tracking-widest text-sm">Partenaires</span>
                    </div>
                    <div class="border-l-4 border-secondary pl-6">
                        <span class="block text-4xl font-headline font-black text-white mb-2"><span class="counter" data-target="100" data-suffix="%">100%</span></span>
                        <span class="text-slate-400 font-bold uppercase tracking-widest text-sm">À vos côtés, en toute indépendance</span>
                    </div>
                    <div class="border-l-4 border-secondary pl-6">
                        <span class="v-stat">1</span>
                        <span class="text-slate-400 font-bold uppercase tracking-widest text-sm">Relation privilégiée avec une vision 360°</span>
                    </div>
                </div>
                {'<a href="/le-cabinet.html" class="v-more" style="font-size:.9rem">Découvrir le cabinet <span class="material-symbols-outlined" aria-hidden="true">arrow_forward</span></a>' if CONFIG["page_cabinet"] else ''}
                <div class="mt-12 pt-8 border-t border-white/10 flex items-center gap-8">
                    <a href="https://sofraco.com/courtier/cabinet-puxeddu/" target="_blank" rel="noopener">
                        <img src="/public/logo-sofraco.webp" alt="Sofraco - partenaire Valorys" width="192" height="64" loading="lazy" decoding="async" class="h-16 w-auto opacity-70 hover:opacity-100 transition-opacity duration-300" style="filter: brightness(0) invert(1);">
                    </a>
                    <a href="https://www.aurep.com/" target="_blank" rel="noopener">
                        <img src="/public/aurep_logo.webp" alt="AUREP - partenaire Valorys" width="206" height="64" loading="lazy" decoding="async" class="h-16 w-auto opacity-70 hover:opacity-100 transition-opacity duration-300" style="filter: brightness(0) invert(1);">
                    </a>
                </div>
            </div>
        </div>
    </div>
</section>

<!-- ===== POURQUOI NOUS ===== -->
<section id="pourquoi" class="py-24 bg-surface-container-low">
    <div class="container mx-auto px-8">
        <div class="text-center mb-20 reveal">
            <h2 class="font-headline font-black text-3xl md:text-5xl text-primary uppercase tracking-tighter">Pourquoi nos clients nous choisissent</h2>
        </div>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-12">
            <div class="text-center group reveal stagger-1">
                <div class="w-24 h-24 bg-primary rounded-full flex items-center justify-center mx-auto mb-8 group-hover:bg-secondary transition-colors duration-300"><span class="material-symbols-outlined text-white text-4xl" aria-hidden="true">verified_user</span></div>
                <h3 class="font-headline font-extrabold text-2xl text-primary mb-4 uppercase">100 % indépendant</h3>
                <p class="text-on-surface-variant font-medium">Aucune exclusivité avec un assureur : nous agissons dans votre intérêt, en sélectionnant, comparant et négociant les solutions adaptées à votre situation.</p>
            </div>
            <div class="text-center group reveal stagger-2">
                <div class="w-24 h-24 bg-primary rounded-full flex items-center justify-center mx-auto mb-8 group-hover:bg-secondary transition-colors duration-300"><span class="material-symbols-outlined text-white text-4xl" aria-hidden="true">support_agent</span></div>
                <h3 class="font-headline font-extrabold text-2xl text-primary mb-4 uppercase">Gestion des sinistres</h3>
                <p class="text-on-surface-variant font-medium">Un interlocuteur dédié vous accompagne de la déclaration à l'indemnisation. Nous défendons vos droits auprès des assureurs à chaque étape du sinistre.</p>
            </div>
            <div class="text-center group reveal stagger-3">
                <div class="w-24 h-24 bg-primary rounded-full flex items-center justify-center mx-auto mb-8 group-hover:bg-secondary transition-colors duration-300"><span class="material-symbols-outlined text-white text-4xl" aria-hidden="true">manage_search</span></div>
                <h3 class="font-headline font-extrabold text-2xl text-primary mb-4 uppercase">Audit social &amp; patrimonial</h3>
                <p class="text-on-surface-variant font-medium">Avant toute recommandation, nous faisons le point complet sur votre situation : protection, retraite, épargne et patrimoine.</p>
            </div>
        </div>
    </div>
</section>
""" + contact() + footer()

# ------------------------------------------------------------------ pages intérieures
def page_hero(crumb, h1, lead=""):
    lead_html = f'<p class="v-lead hero-subtitle">{lead}</p>' if lead else ""
    return f"""
<section class="relative overflow-hidden bg-architectural v-page-hero">
    <div class="absolute inset-0 z-[3] opacity-20 pointer-events-none" aria-hidden="true">
        <img alt="" role="presentation" width="512" height="512" decoding="async" class="w-full h-full object-cover" src="/public/hero-texture.webp">
    </div>
    <div class="v-inner">
        <p class="v-crumbs hero-badge"><a href="/">Accueil</a> &nbsp;/&nbsp; {crumb}</p>
        <div class="hero-badge flex items-center gap-3 mb-6">
            <span class="block w-8 h-px bg-secondary"></span>
            <span class="text-secondary font-body uppercase tracking-widest text-xs">Cabinet Valorys · Toulouse</span>
        </div>
        <h1 class="hero-title">{h1}</h1>
        {lead_html}
    </div>
</section>
"""

def service(p):
    faq_ld = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in p["faqs"]]}
    crumbs_ld = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Accueil", "item": BASE + "/"},
        {"@type": "ListItem", "position": 2, "name": p["name"], "item": f'{BASE}/{p["path"]}'}]}
    faqs = "".join(f"<details><summary>{html.escape(q)}</summary><p>{html.escape(a)}</p></details>" for q, a in p["faqs"])
    return head(p["title"], p["desc"], p["path"], [faq_ld, crumbs_ld]) + nav(False) + page_hero(html.escape(p["name"]), p["h1"], p["lead"]) + f"""
<section class="v-body">
    <div class="container mx-auto px-8 v-grid">
        <div class="v-prose reveal">{p["prose"]}</div>
        <aside class="v-aside reveal-right">
            <span class="material-symbols-outlined" aria-hidden="true">verified_user</span>
            <h3>{html.escape(p["aside_title"])}</h3>
            <p>{html.escape(p["aside_text"])}</p>
            <a class="v-btn" href="#contact">Prendre rendez-vous</a>
        </aside>
    </div>
</section>
{expert_blocks(p)}
<section class="v-faq">
    <div class="container mx-auto px-8">
        <h2 class="reveal">Questions fréquentes</h2>
        <div class="v-faq-list reveal">{faqs}</div>
    </div>
</section>
""" + contact(p["besoin"]) + footer()

def expert_blocks(p):
    """Blocs d'expertise optionnels d'une page service (même présentation que la page assurance emprunteur)."""
    out = ""
    if p.get("checks"):
        items = "".join(f'<li><span class="material-symbols-outlined" aria-hidden="true">verified_user</span><span><strong>{t}</strong> : {d}</span></li>' for t, d in p["checks"])
        out += f"""
<section class="py-32 bg-primary relative overflow-hidden" id="analyse">
    <div class="container mx-auto px-8 relative z-10">
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-20 items-center">
            <div class="reveal-left">
                <h2 class="font-headline font-black text-3xl md:text-5xl lg:text-6xl text-white mb-8 leading-tight tracking-tighter">{p["checks_title"]}</h2>
                <p class="v-lead-dark">{p["checks_lead"]}</p>
            </div>
            <ul class="v-checks reveal-right">{items}</ul>
        </div>
    </div>
</section>"""
    if p.get("profils"):
        wi, wt, wd = p["profil_wide"]
        cards = "".join(f'<div class="v-tcard"><span class="v-card-ico"><span class="material-symbols-outlined" aria-hidden="true">{i}</span></span><h3>{t}</h3><p>{d}</p><div class="v-card-mark" aria-hidden="true"><span class="material-symbols-outlined">{i}</span></div></div>' for i, t, d in p["profils"])
        out += f"""
<section class="py-24 bg-surface-container-low" id="profils">
    <div class="container mx-auto px-8">
        <div class="v-head-row reveal">
            <div><h2 class="v-section-title">{p["profils_title"]}</h2><div class="v-bar"></div></div>
            <p class="v-lead-light">{p["profils_lead"]}</p>
        </div>
        <div class="v-trust v-trust3 reveal">
            <div class="v-trust-wide"><span class="v-card-ico v-ico-dark"><span class="material-symbols-outlined" aria-hidden="true">{wi}</span></span><div><h3>{wt}</h3><p>{wd}</p></div><div class="v-card-mark" aria-hidden="true"><span class="material-symbols-outlined">{wi}</span></div></div>
            {cards}
        </div>
    </div>
</section>"""
    return out

COOKIES_TXT = ("""<p>Avec votre accord uniquement, ce site utilise des cookies de mesure d'audience (Google Analytics, via Google Tag Manager). Aucun de ces cookies n'est déposé tant que vous n'avez pas cliqué sur « Accepter ». Votre choix est conservé 6 mois ; les cookies de mesure ont une durée de vie maximale de 13 mois.</p>
<p><a href="#" data-cookie-settings>Modifier mes préférences cookies</a></p>""" if TRACKING else
"<p>Ce site ne dépose aucun cookie de mesure d'audience ni de publicité, et n'utilise aucun traceur nécessitant votre consentement.</p>")

def legal():
    body = f"""
<section class="v-body">
    <div class="container mx-auto px-8">
    <div class="v-prose v-legal">
<h2>Éditeur du site</h2>
<p><strong>{CONFIG["raison_sociale"]}</strong>, exerçant sous le nom commercial <strong>{CONFIG["nom_commercial"]}</strong><br>
{v("forme", "forme juridique")} au capital de {v("capital", "montant du capital")}<br>
{v("siren", "SIREN et ville du RCS")}<br>
Siège : 13 Port Saint-Étienne, 31000 Toulouse<br>
Téléphone : 06 69 94 56 08 · Email : <a href="mailto:contact@cabinet-valorys.com">contact@cabinet-valorys.com</a><br>
Directeur de la publication : Michaël Puxeddu, gérant.</p>

<h2>Statut réglementaire</h2>
<p>Courtier d'assurance ou de réassurance (COA), immatriculé au registre unique des intermédiaires en assurance, banque et finance (ORIAS) sous le n° <strong>{CONFIG["orias"]}</strong>, vérifiable sur <a href="https://www.orias.fr" rel="noopener" target="_blank">www.orias.fr</a>.</p>
<p>Membre de la <strong>CNCEF Assurance</strong>, association professionnelle agréée par l'ACPR.</p>
<p>Activité soumise au contrôle de l'Autorité de contrôle prudentiel et de résolution (ACPR), 4 place de Budapest, CS 92459, 75436 Paris Cedex 09 — <a href="https://acpr.banque-france.fr" rel="noopener" target="_blank">acpr.banque-france.fr</a>.</p>
<ul>
<li><strong>Responsabilité civile professionnelle :</strong> {v("rcp", "assureur et n° de contrat RC Pro")}</li>
<li><strong>Garantie financière :</strong> {v("garantie_fi", "assureur, ou mention qu'elle n'est pas requise")}</li>
<li><strong>Liens capitalistiques :</strong> {v("liens_capitalistiques", "aucun / à préciser")}</li>
<li><strong>Rémunération :</strong> {v("remuneration", "commissions incluses dans la prime, honoraires éventuels")}</li>
</ul>
<p>Le cabinet n'est soumis à aucune obligation contractuelle de travailler exclusivement avec une ou plusieurs entreprises d'assurance. La liste des entreprises avec lesquelles il travaille est disponible sur simple demande.</p>

<h2 id="reclamations">Réclamations</h2>
<p>Pour toute réclamation, vous pouvez écrire au cabinet :</p>
<ul>
<li>par email : <a href="mailto:contact@cabinet-valorys.com">contact@cabinet-valorys.com</a></li>
<li>par courrier : Cabinet Valorys, Service réclamations, 13 Port Saint-Étienne, 31000 Toulouse</li>
</ul>
<p>Nous accusons réception de votre réclamation dans un délai maximal de 10 jours ouvrables, et vous apportons une réponse dans un délai maximal de 2 mois à compter de sa réception, sauf circonstances particulières dont nous vous tiendrons informé.</p>
<h3>Médiation</h3>
<p>Si la réponse ne vous satisfait pas, ou en l'absence de réponse dans ces délais, vous pouvez saisir gratuitement le médiateur compétent :<br>{v("mediateur", "nom, adresse postale et site internet du médiateur")}</p>

<h2>Hébergement</h2>
<p>OVH SAS, 2 rue Kellermann, 59100 Roubaix, France — <a href="https://www.ovhcloud.com" rel="noopener" target="_blank">ovhcloud.com</a>.</p>

<h2 id="politique-confidentialite">Politique de confidentialité</h2>
<p><strong>Responsable du traitement :</strong> {CONFIG["raison_sociale"]} ({CONFIG["nom_commercial"]}), 13 Port Saint-Étienne, 31000 Toulouse.</p>
<p><strong>Données collectées par le formulaire :</strong> nom, email, téléphone (facultatif), type de demande et message.</p>
<p><strong>Finalité et base légale :</strong> répondre à votre demande et, le cas échéant, préparer un rendez-vous. Le traitement repose sur votre consentement, donné en cochant la case du formulaire, puis sur les mesures précontractuelles prises à votre demande.</p>
<p><strong>Destinataires :</strong> le seul Cabinet Valorys. Vos données ne sont ni vendues ni cédées. Elles sont hébergées en France par OVH.</p>
<p><strong>Durée de conservation :</strong> 3 ans à compter du dernier contact si aucune relation contractuelle ne s'ensuit ; si vous devenez client, pendant la durée de la relation et les durées légales applicables.</p>
<p><strong>Vos droits :</strong> accès, rectification, effacement, limitation, opposition, portabilité et retrait du consentement à tout moment, en écrivant à <a href="mailto:contact@cabinet-valorys.com">contact@cabinet-valorys.com</a>. Vous pouvez introduire une réclamation auprès de la CNIL (<a href="https://www.cnil.fr" rel="noopener" target="_blank">cnil.fr</a>).</p>

<h2 id="politique-cookies">Cookies</h2>
{COOKIES_TXT}

<h2>Propriété intellectuelle</h2>
<p>Les textes, logos et visuels de ce site sont la propriété du {CONFIG["raison_sociale"]}, sauf mention contraire. Toute reproduction sans autorisation est interdite.</p>
<p class="v-notice">Les informations de ce site sont données à titre général et ne constituent pas un conseil personnalisé. Toute recommandation fait l'objet d'un document de conseil écrit, établi après analyse de votre situation.</p>
    </div>
    </div>
</section>
"""
    return head("Mentions légales, réclamations et confidentialité | Cabinet Valorys",
                "Mentions légales, statut réglementaire, procédure de réclamation, médiation et politique de confidentialité du Cabinet Valorys.",
                "mentions-legales.html") + nav(False) + page_hero("Mentions légales", "Mentions légales &amp; informations réglementaires") + body + footer()

def page404():
    return head("Page introuvable | Cabinet Valorys", "Page introuvable.", "404.html", noindex=True) + nav(False) + page_hero(
        "Page introuvable", "Cette page n'existe pas.",
        'Elle a peut-être été déplacée. <a href="/" style="color:#fff;text-decoration:underline">Revenir à l\'accueil</a> ou <a href="/#contact" style="color:#fff;text-decoration:underline">nous contacter</a>.') + footer()


# ------------------------------------------------------------------ page assurance emprunteur
EMP_FAQ = [
    ("Puis-je changer d'assurance emprunteur en cours de prêt ?",
     "Oui. Depuis la loi Lemoine, vous pouvez résilier votre assurance de prêt immobilier à tout moment, sans frais, et la remplacer par un autre contrat offrant des garanties équivalentes. Votre banque a 10 jours ouvrés pour accepter la substitution ; l'ancien contrat prend fin 10 jours après que votre assureur a reçu son accord, sans interruption de couverture."),
    ("Ma banque peut-elle refuser le changement ?",
     "Uniquement si les garanties du nouveau contrat ne sont pas équivalentes à celles qu'elle exige. Elle doit répondre dans un délai de 10 jours ouvrés et motiver un éventuel refus. Nous vérifions l'équivalence avant de vous proposer un contrat."),
    ("Le taux de mon crédit va-t-il changer ?",
     "Non. La banque ne peut pas modifier le taux de votre prêt ni facturer de frais parce que vous changez d'assurance."),
    ("Dois-je remplir un questionnaire de santé ?",
     "Pas toujours. Aucun questionnaire de santé ne peut être demandé si la part assurée de vos crédits immobiliers ne dépasse pas 200 000 € par personne et si le prêt est intégralement remboursé avant vos 60 ans."),
    ("J'ai ou j'ai eu un problème de santé, puis-je être assuré ?",
     "Oui, dans la plupart des cas. La convention AERAS encadre l'assurance des personnes présentant un risque aggravé de santé, et le droit à l'oubli s'applique 5 ans après la fin du protocole thérapeutique d'un cancer ou d'une hépatite C, sans rechute. Nous connaissons les assureurs qui acceptent ces profils."),
    ("Qu'est-ce que l'« équivalence des garanties » exigée par la banque ?",
     "Le Comité consultatif du secteur financier (CCSF) a fixé une liste de 18 critères. Votre banque en retient au maximum 11 pour les garanties décès et incapacité (et jusqu'à 4 pour la perte d'emploi) et doit vous les communiquer, notamment dans la fiche standardisée d'information. Nous vérifions chaque critère avant de vous proposer un contrat : c'est ce qui évite un refus."),
    ("Je suis fonctionnaire ou agent territorial : mon assurance est-elle adaptée ?",
     "Pas toujours. Grâce au maintien de traitement, un agent public perd peu de revenus pendant un arrêt de travail : un contrat qui n'indemnise que la perte de revenus (indemnitaire) peut alors ne presque rien verser. Une indemnisation forfaitaire, qui prend en charge l'échéance quel que soit votre salaire, est souvent plus protectrice. Nous accompagnons régulièrement les agents publics et les collectivités."),
    ("Combien coûte votre accompagnement ?",
     "Rien pour vous. Le cabinet est rémunéré par une commission versée par l'assureur retenu, incluse dans la cotisation."),
]

def emprunteur():
    path = "assurance-emprunteur.html"
    faq_ld = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in EMP_FAQ]}
    svc_ld = {"@context": "https://schema.org", "@type": "Service", "name": "Assurance emprunteur", "serviceType": "Courtage en assurance de prêt immobilier",
              "provider": {"@id": BASE + "/#organization"}, "areaServed": "Toulouse et Haute-Garonne", "url": f"{BASE}/{path}"}
    faqs = "".join(f"<details><summary>{html.escape(q)}</summary><p>{html.escape(a)}</p></details>" for q, a in EMP_FAQ)
    return head("Assurance emprunteur à Toulouse : changez d'assurance de prêt | Cabinet Valorys",
                "Courtier en assurance emprunteur à Toulouse : comparaison des contrats, changement à tout moment grâce à la loi Lemoine, démarches auprès de votre banque. Étude sans engagement.",
                path, [faq_ld, svc_ld], preload_hero=True) + nav(False) + f"""
<!-- ===== HERO EMPRUNTEUR ===== -->
<section class="relative h-screen overflow-hidden bg-architectural">
    <div class="absolute inset-0 z-[3] opacity-20 pointer-events-none" aria-hidden="true">
        <img alt="" role="presentation" width="512" height="512" decoding="async" loading="eager" class="w-full h-full object-cover" src="/public/hero-texture.webp">
    </div>
    <div class="v-hero-mob" aria-hidden="true"><img src="/public/Hero-Valo-mobile.webp" alt="" width="800" height="835" decoding="async" loading="eager"></div>
    <div class="hidden lg:block absolute inset-0 z-[1]">
        <picture>
            <source type="image/avif" srcset="/public/Hero-Valo.avif 1x">
            <source type="image/webp" srcset="/public/Hero-Valo.webp 1x">
            <img src="/public/Hero-Valo.png" alt="" role="presentation" width="1376" height="768" fetchpriority="high" loading="eager" decoding="async" class="absolute inset-0 w-full h-full object-cover object-right">
        </picture>
        <div class="absolute inset-0" style="background: linear-gradient(to right, #041534 0%, #041534 20%, rgba(4,21,52,0.95) 35%, rgba(4,21,52,0.7) 50%, rgba(4,21,52,0.2) 70%, transparent 100%);"></div>
        <div class="absolute inset-0" style="background: linear-gradient(to bottom, rgba(4,21,52,0.5) 0%, transparent 20%, transparent 80%, rgba(4,21,52,0.4) 100%);"></div>
    </div>
    <div class="relative z-10 h-full flex items-center pt-24 pb-16 px-8 md:pl-[8%] lg:pl-[12%]">
        <div>
            <div class="hero-badge flex items-center gap-3 mb-6">
                <span class="block w-8 h-px bg-secondary"></span>
                <span class="text-secondary font-body uppercase tracking-widest text-xs">Courtier en assurance emprunteur à Toulouse</span>
            </div>
            <h1 class="hero-title text-5xl lg:text-6xl text-white leading-tight mb-6 drop-shadow-2xl" style="font-family:'DM Serif Display',serif;">
                Votre assurance de prêt,<br>
                <span class="text-transparent bg-clip-text bg-gradient-to-r from-[#C0392B] to-red-400">entre des mains expertes.</span>
            </h1>
            <p class="hero-subtitle text-slate-300 text-base md:text-lg max-w-lg font-medium leading-relaxed mb-10">
                Nouveau crédit ou prêt en cours : nous analysons votre contrat garantie par garantie, nous mettons en concurrence plus de 60 partenaires et nous menons la substitution avec votre banque, jusqu'à son accord.
            </p>
            <div class="hero-cta flex flex-col sm:flex-row items-start gap-6">
                <a href="#contact" class="bg-secondary text-white px-8 py-4 font-body font-semibold text-base rounded-[40px] hover:brightness-110 hover:scale-[1.02] transition-all duration-200">Comparer mon assurance</a>
                <a href="#etapes" class="text-white font-body font-medium text-base border border-transparent px-8 py-4 rounded-[40px] bg-transparent hover:bg-white/15 hover:border-white/50 transition-all duration-300">Comment ça marche ?</a>
            </div>
        </div>
    </div>
</section>

<!-- ===== POURQUOI CHANGER ===== -->
<section class="py-24 bg-surface-container-low" id="pourquoi">
    <div class="container mx-auto px-8">
        <div class="v-head-row reveal">
            <div><h2 class="v-section-title">Pourquoi revoir votre assurance de prêt</h2><div class="v-bar"></div></div>
            <p class="v-lead-light">L'assurance proposée par la banque n'est pas une obligation. Un contrat individuel, choisi sur le marché, couvre souvent mieux votre profil pour un coût plus juste. Sur la durée d'un prêt, l'écart peut représenter plusieurs milliers d'euros.</p>
        </div>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-12">
            <div class="text-center group reveal stagger-1">
                <div class="w-24 h-24 bg-primary rounded-full flex items-center justify-center mx-auto mb-8 group-hover:bg-secondary transition-colors duration-300"><span class="material-symbols-outlined text-white text-4xl" aria-hidden="true">schedule</span></div>
                <h3 class="font-headline font-extrabold text-2xl text-primary mb-4 uppercase">À tout moment</h3>
                <p class="text-on-surface-variant font-medium">Résiliation sans frais, dès la signature de l'offre ou à n'importe quel moment de votre prêt. Nous gérons les délais avec la banque et l'assureur.</p>
            </div>
            <div class="text-center group reveal stagger-2">
                <div class="w-24 h-24 bg-primary rounded-full flex items-center justify-center mx-auto mb-8 group-hover:bg-secondary transition-colors duration-300"><span class="material-symbols-outlined text-white text-4xl" aria-hidden="true">compare_arrows</span></div>
                <h3 class="font-headline font-extrabold text-2xl text-primary mb-4 uppercase">Garanties équivalentes</h3>
                <p class="text-on-surface-variant font-medium">Nous vérifions que le nouveau contrat respecte les exigences de votre banque : elle ne peut alors pas le refuser, ni modifier votre taux.</p>
            </div>
            <div class="text-center group reveal stagger-3">
                <div class="w-24 h-24 bg-primary rounded-full flex items-center justify-center mx-auto mb-8 group-hover:bg-secondary transition-colors duration-300"><span class="material-symbols-outlined text-white text-4xl" aria-hidden="true">health_and_safety</span></div>
                <h3 class="font-headline font-extrabold text-2xl text-primary mb-4 uppercase">Sans questionnaire</h3>
                <p class="text-on-surface-variant font-medium">Aucun questionnaire de santé si la part assurée ne dépasse pas 200 000 € par personne et que le prêt se termine avant vos 60 ans.</p>
            </div>
        </div>
    </div>
</section>

<!-- ===== CE QUE NOUS COMPARONS ===== -->
<section class="py-32 bg-primary relative overflow-hidden" id="comparaison">
    <div class="container mx-auto px-8 relative z-10">
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-20 items-center">
            <div class="reveal-left">
                <h2 class="font-headline font-black text-3xl md:text-5xl lg:text-6xl text-white mb-8 leading-tight tracking-tighter">
                    Le prix compte.<br><span class="text-secondary">Les garanties aussi.</span>
                </h2>
                <p class="v-lead-dark">Deux contrats au même tarif peuvent protéger très différemment le jour d'un arrêt de travail. Un comparateur en ligne compare des prix ; nous comparons des garanties. Nous lisons les conditions générales à votre place et vous montrons les écarts, ligne par ligne.</p>
            </div>
            <ul class="v-checks reveal-right">
                <li><span class="material-symbols-outlined" aria-hidden="true">verified_user</span><span><strong>Les critères de votre banque</strong> : les 11 critères d'équivalence (parmi les 18 du CCSF) qu'elle exige, vérifiés un par un.</span></li>
                <li><span class="material-symbols-outlined" aria-hidden="true">verified_user</span><span><strong>Décès et PTIA</strong> : capital remboursé à la banque, pour protéger votre famille.</span></li>
                <li><span class="material-symbols-outlined" aria-hidden="true">verified_user</span><span><strong>ITT et invalidité</strong> : franchise, durée d'indemnisation, seuil d'invalidité (IPT, IPP), et surtout calcul forfaitaire ou indemnitaire.</span></li>
                <li><span class="material-symbols-outlined" aria-hidden="true">verified_user</span><span><strong>Exclusions</strong> : pathologies du dos et troubles psychiques, souvent exclus sans hospitalisation, et leur éventuel rachat.</span></li>
                <li><span class="material-symbols-outlined" aria-hidden="true">verified_user</span><span><strong>Couverture de votre métier</strong> : incapacité appréciée par rapport à votre profession ou à toute activité, ce qui change tout pour un indépendant.</span></li>
                <li><span class="material-symbols-outlined" aria-hidden="true">verified_user</span><span><strong>Coût réel</strong> : tarification sur le capital initial ou restant dû, TAEA et coût total sur toute la durée du prêt.</span></li>
                <li><span class="material-symbols-outlined" aria-hidden="true">verified_user</span><span><strong>Quotité</strong> : répartition de la couverture entre co-emprunteurs, selon vos revenus et votre situation familiale.</span></li>
                <li><span class="material-symbols-outlined" aria-hidden="true">verified_user</span><span><strong>Formalités</strong> : questionnaire de santé, droit à l'oubli, convention AERAS et justificatifs selon le montant emprunté.</span></li>
            </ul>
        </div>
    </div>
</section>

<!-- ===== PROFILS ===== -->
<section class="py-24 bg-surface-container-low" id="profils">
    <div class="container mx-auto px-8">
        <div class="v-head-row reveal">
            <div><h2 class="v-section-title">Tous les dossiers, du plus simple au plus complexe</h2><div class="v-bar"></div></div>
            <p class="v-lead-light">Achat de votre résidence principale ou situation plus délicate : chaque dossier bénéficie de la même analyse et du même suivi, jusqu'à l'accord de la banque.</p>
        </div>
        <div class="v-trust v-trust3 reveal">
            <div class="v-trust-wide"><span class="v-card-ico v-ico-dark"><span class="material-symbols-outlined" aria-hidden="true">home</span></span><div><h3>Résidence principale et premier achat</h3><p>Salariés, couples, primo-accédants : c'est le cœur de notre activité. Nous trouvons rapidement le contrat le plus juste, réglons la quotité entre co-emprunteurs et vous remettons une attestation conforme aux exigences de votre banque, dans les délais de votre offre de prêt.</p></div><div class="v-card-mark" aria-hidden="true"><span class="material-symbols-outlined">home</span></div></div>
            <div class="v-tcard"><span class="v-card-ico"><span class="material-symbols-outlined" aria-hidden="true">health_and_safety</span></span><h3>Risques aggravés de santé</h3><p>Antécédents médicaux, maladie chronique, surprime ou exclusion proposée : nous connaissons les assureurs qui acceptent ces profils et appliquons la convention AERAS et le droit à l'oubli.</p><div class="v-card-mark" aria-hidden="true"><span class="material-symbols-outlined">health_and_safety</span></div></div>
            <div class="v-tcard"><span class="v-card-ico"><span class="material-symbols-outlined" aria-hidden="true">account_balance</span></span><h3>Agents publics</h3><p>Fonctionnaires et agents des collectivités : le maintien de traitement change la façon de choisir la garantie incapacité. Nous vous évitons de payer pour une couverture qui ne vous versera rien.</p><div class="v-card-mark" aria-hidden="true"><span class="material-symbols-outlined">account_balance</span></div></div>
            <div class="v-tcard"><span class="v-card-ico"><span class="material-symbols-outlined" aria-hidden="true">stethoscope</span></span><h3>Professions libérales et médicales</h3><p>Médecins, kinés, infirmiers, avocats, indépendants : incapacité appréciée dans votre profession, franchises adaptées, garanties cohérentes avec votre prévoyance.</p><div class="v-card-mark" aria-hidden="true"><span class="material-symbols-outlined">stethoscope</span></div></div>
            <div class="v-tcard"><span class="v-card-ico"><span class="material-symbols-outlined" aria-hidden="true">engineering</span></span><h3>Métiers et sports à risque</h3><p>Travail en hauteur, conduite, port de charges, sports mécaniques ou aériens : nous recherchons les contrats qui couvrent votre activité sans exclusion.</p><div class="v-card-mark" aria-hidden="true"><span class="material-symbols-outlined">engineering</span></div></div>
            <div class="v-tcard"><span class="v-card-ico"><span class="material-symbols-outlined" aria-hidden="true">apartment</span></span><h3>Investissement et gros capitaux</h3><p>Locatif, SCI, plusieurs prêts, capitaux élevés : quotités, formalités médicales et financières et coût global optimisés sur l'ensemble de vos financements.</p><div class="v-card-mark" aria-hidden="true"><span class="material-symbols-outlined">apartment</span></div></div>
            <div class="v-tcard"><span class="v-card-ico"><span class="material-symbols-outlined" aria-hidden="true">sync_alt</span></span><h3>Prêts en cours</h3><p>Votre crédit a déjà quelques années ? Nous chiffrons l'économie réelle sur la durée restante et prenons en charge la substitution de A à Z.</p><div class="v-card-mark" aria-hidden="true"><span class="material-symbols-outlined">sync_alt</span></div></div>
        </div>
    </div>
</section>

<!-- ===== ÉTAPES ===== -->
<section class="py-24 bg-surface" id="etapes">
    <div class="container mx-auto px-8">
        <div class="v-head-row reveal">
            <div><h2 class="v-section-title">Comment ça marche</h2><div class="v-bar"></div></div>
            <p class="v-lead-light">Vous nous transmettez quelques documents, nous nous occupons du reste, y compris des échanges avec votre banque.</p>
        </div>
        <ol class="v-steps reveal">
            <li><h3>Vos documents</h3><p>Votre offre de prêt et son tableau d'amortissement, ainsi que votre contrat d'assurance actuel si le prêt est en cours.</p></li>
            <li><h3>La comparaison</h3><p>Nous interrogeons nos assureurs partenaires et vous présentons les offres à garanties équivalentes, avec le coût total sur la durée du prêt.</p></li>
            <li><h3>La souscription</h3><p>Vous choisissez votre contrat et le signez en ligne. Les formalités médicales éventuelles sont faites directement avec l'assureur, en toute confidentialité.</p></li>
            <li><h3>La substitution</h3><p>Nous transmettons la demande à votre banque, qui a 10 jours ouvrés pour répondre. Le nouveau contrat remplace l'ancien sans interruption de couverture.</p></li>
        </ol>
        <div class="v-docs reveal"><span>Offre de prêt</span><span>Tableau d'amortissement</span><span>Contrat d'assurance actuel</span><span>Fiche standardisée d'information</span></div>
    </div>
</section>

<!-- ===== FAQ ===== -->
<section class="v-faq" id="faq">
    <div class="container mx-auto px-8">
        <h2 class="reveal">Questions fréquentes</h2>
        <div class="v-faq-list reveal">{faqs}</div>
    </div>
</section>

<!-- ===== INTERLOCUTEUR ===== -->
<section class="py-24 bg-primary relative overflow-hidden">
    <div class="container mx-auto px-8 relative z-10">
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-20 items-center">
            <div class="relative reveal-left">
                <div class="absolute -top-12 -left-12 w-48 h-48 border-t-8 border-l-8 border-secondary opacity-50"></div>
                <img alt="Michaël Puxeddu, courtier en assurance à Toulouse" width="341" height="512" loading="lazy" decoding="async" class="rounded-none shadow-2xl relative z-10 grayscale hover:grayscale-0 transition-all duration-700 w-4/5 object-cover mx-auto block" src="/public/PUXEDDU-Michael.webp">
            </div>
            <div class="reveal-right">
                <h2 class="font-headline font-black text-3xl md:text-5xl text-white mb-8 leading-tight tracking-tighter">Une équipe experte,<br><span class="text-secondary">pas une plateforme.</span></h2>
                <p class="v-lead-dark">Nous vous accompagnons de l'analyse de vos garanties jusqu'à l'accord de votre banque, avec une équipe à taille humaine, experte en protection sociale et indépendante de tout assureur. Ici, pas de centre d'appels ni de formulaire sans réponse : vous savez qui suit votre dossier et vous nous joignez directement. Et nous restons à vos côtés bien après la signature, le jour où votre contrat doit jouer son rôle.</p>
                <div class="grid grid-cols-2 gap-8 mt-12">
                    <div class="border-l-4 border-secondary pl-6"><span class="v-stat">15+</span><span class="text-slate-400 font-bold uppercase tracking-widest text-sm">Années d'expertise</span></div>
                    <div class="border-l-4 border-secondary pl-6"><span class="v-stat">60+</span><span class="text-slate-400 font-bold uppercase tracking-widest text-sm">Partenaires</span></div>
                </div>
            </div>
        </div>
    </div>
</section>
""" + contact("Assurance emprunteur") + footer()


# ------------------------------------------------------------------ page Le cabinet
def cabinet():
    path = "le-cabinet.html"
    ld = {"@context": "https://schema.org", "@type": "AboutPage", "name": "Le Cabinet Valorys", "url": f"{BASE}/{path}",
          "about": {"@id": BASE + "/#organization"}}
    return head("Le cabinet : votre courtier en assurance à Toulouse | Cabinet Valorys",
                "Le Cabinet Valorys, courtier indépendant à Toulouse : un interlocuteur unique, une méthode d'audit social et patrimonial, plus de 60 compagnies partenaires.",
                path, [ld]) + nav(False) + page_hero("Le cabinet", "Un cabinet à taille humaine, un interlocuteur qui connaît votre dossier.",
                "Pas de centre d'appels ni de conseiller différent à chaque appel. Au Cabinet Valorys, la personne qui étudie votre situation est celle qui vous suit ensuite, du devis jusqu'au sinistre.") + f"""
<!-- ===== FONDATEUR ===== -->
<section class="py-32 bg-primary relative overflow-hidden">
    <div class="container mx-auto px-8 relative z-10">
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-20 items-center">
            <div class="relative reveal-left">
                <div class="absolute -top-12 -left-12 w-48 h-48 border-t-8 border-l-8 border-secondary opacity-50"></div>
                <img alt="Michaël Puxeddu, fondateur du Cabinet Valorys" width="341" height="512" loading="lazy" decoding="async" class="rounded-none shadow-2xl relative z-10 grayscale hover:grayscale-0 transition-all duration-700 w-4/5 object-cover mx-auto block" src="/public/PUXEDDU-Michael.webp">
            </div>
            <div class="reveal-right">
                <p class="text-secondary font-body uppercase tracking-widest text-xs mb-4">Fondateur</p>
                <h2 class="font-headline font-black text-3xl md:text-5xl text-white mb-8 leading-tight tracking-tighter">Michaël Puxeddu</h2>
                <p class="v-lead-dark">Courtier en assurance depuis plus de 15 ans à Toulouse, j'ai fondé le Cabinet Valorys pour accompagner particuliers, indépendants et dirigeants sur ce qui compte vraiment : protéger leurs revenus, leur famille et leur retraite.</p>
                <p class="v-lead-dark" style="margin-top:1.25rem">Je ne travaille pour aucune compagnie en particulier. Mon rôle est de comprendre votre situation, de chercher sur le marché les garanties qui y répondent, puis de défendre vos intérêts auprès de l'assureur quand vous en avez besoin.</p>
                <div class="grid grid-cols-2 gap-8 mt-12">
                    <div class="border-l-4 border-secondary pl-6"><span class="block text-4xl font-headline font-black text-white mb-2"><span class="counter" data-target="15" data-suffix="+">15+</span></span><span class="text-slate-400 font-bold uppercase tracking-widest text-sm">Ans d'expérience</span></div>
                    <div class="border-l-4 border-secondary pl-6"><span class="block text-4xl font-headline font-black text-white mb-2"><span class="counter" data-target="60" data-suffix="+">60+</span></span><span class="text-slate-400 font-bold uppercase tracking-widest text-sm">Compagnies partenaires</span></div>
                </div>
            </div>
        </div>
    </div>
</section>

<!-- ===== MÉTHODE ===== -->
<section class="py-24 bg-surface" id="methode">
    <div class="container mx-auto px-8">
        <div class="v-head-row reveal">
            <div><h2 class="v-section-title">Notre méthode</h2><div class="v-bar"></div></div>
            <p class="v-lead-light">Le même déroulé pour chaque client. Une recommandation n'a de sens qu'une fois toute la situation connue.</p>
        </div>
        <ol class="v-steps reveal">
            <li><h3>Audit social et patrimonial</h3><p>Au premier rendez-vous, nous faisons le tour de votre situation : statut, revenus, famille, contrats en place, droits à la retraite.</p></li>
            <li><h3>Comparaison du marché</h3><p>Nous interrogeons nos compagnies partenaires et comparons garanties, exclusions et tarifs, pour votre profil précis.</p></li>
            <li><h3>Conseil écrit</h3><p>Vous recevez un document de conseil qui explique ce que nous recommandons, pourquoi, et ce que cela coûte.</p></li>
            <li><h3>Suivi dans la durée</h3><p>Nous revoyons vos contrats quand votre situation évolue et vous accompagnons de la déclaration de sinistre jusqu'à l'indemnisation.</p></li>
        </ol>
    </div>
</section>

<!-- ===== ENGAGEMENTS ===== -->
<section class="py-24 bg-surface-container-low">
    <div class="container mx-auto px-8">
        <div class="text-center mb-20 reveal"><h2 class="font-headline font-black text-3xl md:text-5xl text-primary uppercase tracking-tighter">Nos engagements</h2></div>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-12">
            <div class="text-center group reveal stagger-1">
                <div class="w-24 h-24 bg-primary rounded-full flex items-center justify-center mx-auto mb-8 group-hover:bg-secondary transition-colors duration-300"><span class="material-symbols-outlined text-white text-4xl" aria-hidden="true">verified_user</span></div>
                <h3 class="font-headline font-extrabold text-2xl text-primary mb-4 uppercase">Indépendance</h3>
                <p class="text-on-surface-variant font-medium">Aucune exclusivité avec un assureur. Nous recommandons le contrat adapté à votre besoin, pas celui d'un catalogue.</p>
            </div>
            <div class="text-center group reveal stagger-2">
                <div class="w-24 h-24 bg-primary rounded-full flex items-center justify-center mx-auto mb-8 group-hover:bg-secondary transition-colors duration-300"><span class="material-symbols-outlined text-white text-4xl" aria-hidden="true">description</span></div>
                <h3 class="font-headline font-extrabold text-2xl text-primary mb-4 uppercase">Transparence</h3>
                <p class="text-on-surface-variant font-medium">Chaque proposition est expliquée par écrit. Notre rémunération est une commission versée par l'assureur, incluse dans votre cotisation.</p>
            </div>
            <div class="text-center group reveal stagger-3">
                <div class="w-24 h-24 bg-primary rounded-full flex items-center justify-center mx-auto mb-8 group-hover:bg-secondary transition-colors duration-300"><span class="material-symbols-outlined text-white text-4xl" aria-hidden="true">support_agent</span></div>
                <h3 class="font-headline font-extrabold text-2xl text-primary mb-4 uppercase">Disponibilité</h3>
                <p class="text-on-surface-variant font-medium">Une ligne directe, du lundi au vendredi de 9 h à 20 h et le samedi matin. Au cabinet, chez vous ou en visio.</p>
            </div>
        </div>
    </div>
</section>

<!-- ===== CADRE & RÉSEAU ===== -->
<section class="py-24 bg-surface">
    <div class="container mx-auto px-8">
        <div class="v-head-row reveal">
            <div><h2 class="v-section-title">Un cadre réglementé</h2><div class="v-bar"></div></div>
            <p class="v-lead-light">Le métier de courtier est encadré. Voici ce qui protège nos clients, et que chacun peut vérifier.</p>
        </div>
        <div class="v-trust reveal">
            <div><span class="material-symbols-outlined" aria-hidden="true">gavel</span><h3>Immatriculé ORIAS</h3><p>N° {CONFIG["orias"]}, vérifiable sur orias.fr. Activité sous le contrôle de l'ACPR.</p></div>
            <div><span class="material-symbols-outlined" aria-hidden="true">shield</span><h3>RC professionnelle</h3><p>Le cabinet est assuré pour ses activités d'intermédiation auprès d'AIG Europe.</p></div>
            <div><span class="material-symbols-outlined" aria-hidden="true">group</span><h3>CNCEF Assurance</h3><p>Membre de l'association professionnelle agréée par l'ACPR pour les courtiers.</p></div>
            <div><span class="material-symbols-outlined" aria-hidden="true">check_circle</span><h3>Médiation</h3><p>Une procédure de réclamation et un médiateur indépendant, détaillés dans nos <a href="/mentions-legales.html#reclamations" class="underline">mentions légales</a>.</p></div>
        </div>
        <div class="v-logos reveal">
            <a href="https://sofraco.com/courtier/cabinet-puxeddu/" target="_blank" rel="noopener"><img src="/public/logo-sofraco.webp" alt="Sofraco" width="192" height="64" loading="lazy"></a>
            <a href="https://www.aurep.com/" target="_blank" rel="noopener"><img src="/public/aurep_logo.webp" alt="AUREP" width="206" height="64" loading="lazy"></a>
        </div>
    </div>
</section>
""" + contact() + footer()

def write(name, s):
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
        f.write(s)

if __name__ == "__main__":
    js = os.path.join(OUT, "public", "js", "consent.js")
    if TRACKING:
        t = open(os.path.join(SRC, "consent.template.js"), encoding="utf-8").read()
        open(js, "w", encoding="utf-8").write(t.replace("__GTM_ID__", CONFIG["gtm_id"] or "").replace("__GA_ID__", CONFIG["ga_id"] or ""))
    elif os.path.exists(js):
        os.remove(js)
    write("index.html", index())
    for p in PAGES:
        write(p["path"], service(p))
    write("mentions-legales.html", legal())
    write("assurance-emprunteur.html", emprunteur())
    cab = os.path.join(OUT, "le-cabinet.html")
    if CONFIG["page_cabinet"]:
        write("le-cabinet.html", cabinet())
    elif os.path.exists(cab):
        os.remove(cab)
    write("404.html", page404())
    today = date.today().isoformat()
    urls = [""] + [p["path"] for p in PAGES] + (["le-cabinet.html"] if CONFIG["page_cabinet"] else []) + ["assurance-emprunteur.html", "mentions-legales.html"]
    write("sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
          + "".join(f"<url><loc>{BASE}/{u}</loc><lastmod>{today}</lastmod></url>" for u in urls) + "</urlset>\n")
    write("robots.txt", f"User-agent: *\nAllow: /\nSitemap: {BASE}/sitemap.xml\n")
    print("Site généré dans", OUT)
