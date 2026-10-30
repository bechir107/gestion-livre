# Application de gestion des livres

## 1. Description du projet

Cette application web permet de gérer une collection de livres. Elle offre les fonctionnalités suivantes :
- Afficher la liste des livres.
- Ajouter un livre.
- Modifier les informations d’un livre.
- Supprimer un livre.

## 2. Technologies utilisées

- **Frontend :** Angular
- **Backend :** Python, Flask
- **Base de données :** MySQL / MariaDB
- **API :** REST API

## 3. Structure du projet

- `frontend-angular/` : code source de l’interface Angular.
- `backend-flask/` : code source du serveur Flask.
- `books_db.sql` : fichier d’export de la base de données.

## 4. Installation de la base de données

1. Démarrer Apache et MySQL depuis XAMPP.
2. Ouvrir phpMyAdmin : http://localhost/phpmyadmin
3. Créer une base de données nommée `books_db`, si elle n’existe pas.
4. Importer le fichier `books_db.sql`.

## 5. Installation et lancement du backend

Ouvrir un terminal dans le dossier `backend-flask/`, puis exécuter :

```bash
python -m pip install Flask Flask-SQLAlchemy Flask-Cors PyMySQL
python app.py
```

Le backend sera accessible à l’adresse :

http://127.0.0.1:5000

## 6. Installation et lancement du frontend

Ouvrir un terminal dans le dossier `frontend-angular/`, puis exécuter :

```bash
npm install
ng serve
```

L’application sera accessible à l’adresse :

http://localhost:4200

## 7. Configuration

La connexion à MySQL est configurée dans le backend Flask. Par défaut, la configuration utilisée est :

- Hôte : `localhost`
- Base de données : `books_db`
- Utilisateur : `root`

Si MySQL utilise un mot de passe, modifier la configuration de connexion dans `app.py`.

## 8. Importation des données

Le fichier `books_db.sql` contient la structure de la table `livre` et les données exportées.

