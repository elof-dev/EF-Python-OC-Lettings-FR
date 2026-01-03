## Résumé

Site web d'Orange County Lettings

## Développement local

### Prérequis

- Compte GitHub avec accès en lecture à ce repository
- Git CLI
- SQLite3 CLI
- Interpréteur Python, version 3.6 ou supérieure

Dans le reste de la documentation sur le développement local, il est supposé que la commande `python` de votre OS shell exécute l'interpréteur Python ci-dessus (à moins qu'un environnement virtuel ne soit activé).

### macOS / Linux

#### Cloner le repository

- `cd /path/to/put/project/in`
- `git clone https://github.com/elof-dev/EF-Python-OC-Lettings-FR

#### Créer l'environnement virtuel

- `cd /path/to/EF-Python-OC-Lettings-FR`
- `python -m venv venv`
- `apt-get install python3-venv` (Si l'étape précédente comporte des erreurs avec un paquet non trouvé sur Ubuntu)
- Activer l'environnement `source venv/bin/activate`
- Confirmer que la commande `python` exécute l'interpréteur Python dans l'environnement virtuel
`which python`
- Confirmer que la version de l'interpréteur Python est la version 3.6 ou supérieure `python --version`
- Confirmer que la commande `pip` exécute l'exécutable pip dans l'environnement virtuel, `which pip`
- Pour désactiver l'environnement, `deactivate`

#### Exécuter le site

- `cd /path/to/EF-Python-OC-Lettings-FR`
- `source venv/bin/activate`
- `pip install --requirement requirements.txt`
- `python manage.py runserver`
- Aller sur `http://localhost:8000` dans un navigateur.
- Confirmer que le site fonctionne et qu'il est possible de naviguer (vous devriez voir plusieurs profils et locations).

#### Linting

- `cd /path/to/EF-Python-OC-Lettings-FR`
- `source venv/bin/activate`
- `flake8`

#### Tests unitaires

- `cd /path/to/EF-Python-OC-Lettings-FR`
- `source venv/bin/activate`
- `pytest`

#### Base de données

- `cd /path/to/EF-Python-OC-Lettings-FR`
- Ouvrir une session shell `sqlite3`
- Se connecter à la base de données `.open oc-lettings-site.sqlite3`
- Afficher les tables dans la base de données `.tables`
- Afficher les colonnes dans le tableau des profils, `pragma table_info(EF-Python-OC-Lettings-FR_profile);`
- Lancer une requête sur la table des profils, `select user_id, favorite_city from
  EF-Python-OC-Lettings-FR_profile where favorite_city like 'B%';`
- `.quit` pour quitter

#### Panel d'administration

- Aller sur `http://localhost:8000/admin`
- Connectez-vous avec l'utilisateur `admin`, mot de passe `Abc1234!`

### Windows

Utilisation de PowerShell, comme ci-dessus sauf :

- Pour activer l'environnement virtuel, `.\venv\Scripts\Activate.ps1` 
- Remplacer `which <my-command>` par `(Get-Command <my-command>).Path`

## Déploiement

Le projet est déployé automatiquement via un pipeline **CI/CD** reposant sur **GitHub Actions**, **Docker**, **Docker Hub** et **Render**.

L'application est hébergée en production sur Render à l’adresse suivante :
https://ef-oc-lettings-fr-latest.onrender.com

Le fonctionnement est le suivant :

1. À chaque push sur la branche `master`, un pipeline GitHub Actions est déclenché.
2. Le pipeline exécute :
   - le linting du code (flake8),
   - la suite de tests automatisés (pytest),
   - la vérification de la couverture de tests (≥ 80 %).
3. Si toutes les étapes précédentes réussissent :
   - une image Docker de l’application est construite,
   - l’image est taguée avec :
     - `latest`,
     - le hash du commit Git correspondant,
   - l’image est poussée vers le registre Docker Hub.
4. Render détecte automatiquement la nouvelle image Docker et redéploie l’application en production.

Les modifications apportées aux autres branches déclenchent uniquement les tests, sans conteneurisation ni déploiement.

---

### Configuration requise pour le déploiement

Pour que le déploiement fonctionne correctement, les éléments suivants doivent être configurés :

#### Variables d’environnement (Render)

Les variables d’environnement suivantes doivent être définies dans l’interface Render :

| Variable | Description |
|--------|------------|
| `DJANGO_DEBUG` | Afin de pouvoir déployer le site en production, cette variable doit être définie sur `False`. |
| `DJANGO_SECRET_KEY` | Clé secrète Django pour la production : à renseigner sur Render sinon Django refusera de démarrer en production |
| `DJANGO_ALLOWED_HOSTS` | Domaine autorisé pour la production fourni par Render (ef-oc-lettings-fr-latest.onrender.com) |
| `SENTRY_DSN` | URL de configuration Sentry : à renseigner sur Render sinon Sentry ne fonctionne pas en production |

Ces variables permettent à Django de fonctionner correctement en environnement de production.

---

### Gestion des fichiers statiques

Les fichiers statiques (CSS, JavaScript, images) sont collectés lors du build Docker à l’aide de la commande :

```bash
python manage.py collectstatic --noinput
```

Cela garantit que tous les fichiers statiques sont disponibles pour le serveur web en production.
Ils sont servis par le serveur web intégré de Render car Django ne sert pas les fichiers statiques en production

### Procédure de déploiement
Après avoir effectué les modifications souhaitées dans le code source, la procédure de déploiement est la suivante :

```bash 
git add .
git commit -m "Description des changements"
git push origin master
```

Ou bien si vous utilisez GitHub Desktop, cliquez sur "Commit to master" puis "Push origin".

Le pipeline CI/CD se déclenchera automatiquement.
Vous pouvez le vérifier dans l’onglet "Actions" du repository GitHub.
- Si toutes les étapes de tests réussissent :
L'image Docker sera construite, poussée vers Docker Hub, et Render redéploiera l’application.
Aucune intervention manuelle n’est nécessaire après le push vers la branche `master`.

Il est normal que le déploiement prenne quelques minutes puisque Render doit télécharger la nouvelle image Docker et redémarrer l’application

- Si une étape échoue, cliquhez sur l’étape échouée dans l’interface GitHub Actions pour voir les logs d’erreur
Le pipeline s’arrêtera et l’image Docker ne sera pas construite ni poussée ce qui garantit que le code déployé en production a passé tous les tests
La version en production restera inchangée tant que le pipeline n’aura pas réussi.
