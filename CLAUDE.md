# Site du Cabinet Valorys — règles de travail

Ce dépôt est la **seule source** du site www.cabinet-valorys.com. Il est publié automatiquement sur l'hébergement OVH (cluster127, compte `cabingw`) à chaque modification poussée sur la branche `main`.

Déploiement : Multisite OVH « Test nouveau site » → dossier racine `site-git`, associé à ce dépôt (HTTPS, branche `main`) ; webhook GitHub → OVH actif depuis le 2 novembre 2026. Le dépôt est public : n'y mettre aucun mot de passe ni donnée client.

## Règles impératives
1. **Ne jamais modifier les fichiers directement sur le serveur** (FileZilla, éditeur OVH). Toute modification passe par ce dépôt, sinon elle sera écrasée au prochain déploiement.
2. **Toujours partir de la dernière version** : `git pull` avant de commencer.
3. **Ne jamais modifier les fichiers HTML à la main.** Les pages sont générées : modifier `_source/build.py` (structure, accueil, formulaire) ou `_source/contenu.py` (textes des pages services), puis lancer `python3 _source/build.py` et vérifier le rendu avant de pousser.
4. Décrire chaque changement dans le message de commit, en français, en une phrase.
5. **Montrer chaque modification à Michaël (captures ordinateur et téléphone) et attendre sa validation avant de la mettre en ligne.** Proposer une seule version recommandée, déjà vérifiée (cohérence, répétitions, longueur), plutôt qu'une liste d'options.
6. **Penser à tout ce qu'un changement touche.** Les titres et les contrats des six rubriques sont définis une seule fois dans `NAV_CARTES` (`_source/build.py`) : cartes de l'accueil, menu « Notre expertise » et pied de page en dépendent. Pour toute autre modification de nom ou de texte, vérifier aussi les pages services, le formulaire de contact et les titres Google.
7. **Regrouper les retouches en une seule mise en ligne**, et ne jamais pousser deux fois sur `main` à moins de quelques minutes d'intervalle : le webhook OVH refuse alors les envois (erreur 401). Si une mise à jour n'apparaît pas, Michaël clique sur « Déployer » dans OVH (Multisite) ou sur « Redeliver » dans GitHub.

## Choix déjà validés par Michaël (ne pas revenir dessus sans qu'il le demande)
- Accueil : bandeau « Courtier en assurance & gestion de patrimoine à Toulouse » ; titre « Une expertise locale. Une vision globale. » (positionnement national malgré tout) ; titres de cartes en minuscules, orientés client, avec les contrats en petit au-dessus.
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
