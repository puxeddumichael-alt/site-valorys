# Site du Cabinet Valorys — règles de travail

Ce dépôt est la **seule source** du site www.cabinet-valorys.com. Il est publié automatiquement sur l'hébergement OVH (cluster127, compte `cabingw`) à chaque modification poussée sur la branche `main`.

## Règles impératives
1. **Ne jamais modifier les fichiers directement sur le serveur** (FileZilla, éditeur OVH). Toute modification passe par ce dépôt, sinon elle sera écrasée au prochain déploiement.
2. **Toujours partir de la dernière version** : `git pull` avant de commencer.
3. **Ne jamais modifier les fichiers HTML à la main.** Les pages sont générées : modifier `_source/build.py` (structure, accueil, formulaire) ou `_source/contenu.py` (textes des pages services), puis lancer `python3 _source/build.py` et vérifier le rendu avant de pousser.
4. Décrire chaque changement dans le message de commit, en français, en une phrase.

## Choix déjà validés par Michaël (ne pas revenir dessus sans qu'il le demande)
- Accueil : bandeau « Courtier en assurance & gestion de patrimoine à Toulouse ».
- Pas de ligne de réassurance (ORIAS · 60+ compagnies · ligne directe) sous les boutons du hero, ni sur l'accueil ni sur la page assurance emprunteur.
- Pas de « 500+ clients » ni « 98 % de satisfaction » ; pas de faux membres d'équipe ni de fausses photos.
- Page « Le cabinet » désactivée (`page_cabinet: False`) jusqu'à un vrai recrutement.
- Mesure d'audience désactivée (`gtm_id` / `ga_id` vides) tant que Michaël n'a pas ses propres comptes Google.
- Pied de page : « Cabinet Valorys » seul ; la dénomination « Cabinet Puxeddu » n'apparaît que dans les mentions légales.
- Formulaire « Être rappelé » : Prénom, Nom, Téléphone, créneau.

## Formulaire de contact
- `contact.php` envoie à **contact@cabinet-valorys.com** (boîte MX Plan, lue dans Outlook sous « CONTACT VALORYS »), par SMTP authentifié (`ssl0.ovh.net:465`), avec un email HTML aux couleurs du cabinet.
- Réglages SMTP et mot de passe : fichier `/home/cabingw/valorys-smtp.php`, **hors du dépôt et hors du site**. Ne jamais le versionner.
- Chaque demande est aussi journalisée dans `/home/cabingw/demandes-site/demandes.csv` (hors du site).

## Organisation des fichiers
- Racine : le site publié (pages, `public/`, `lib/`, `contact.php`, `.htaccess`).
- `_source/` : générateur et textes (inaccessible depuis internet).
- Les fichiers `.md`, `.py` et le dossier `.git` sont bloqués par `.htaccess`.
