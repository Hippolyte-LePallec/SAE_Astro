# AstroApp

AstroApp est une application de bureau permettant de rechercher, visualiser et combiner des images astronomiques au format FITS. Elle offre une interface utilisateur intuitive pour explorer les données célestes et créer des images composites RGB à partir de différentes bandes.

## Fonctionnalités

- **Recherche d'objets célestes :**
  - Résolution de noms d'objets célestes en coordonnées (via `SkyCoord` ou `JPL Horizons`).
  - Téléchargement d'images FITS à partir de missions tels que DSS2 (Red, Blue, InfraRouge).

- **Chargement local :**
  - Importation d'images FITS locales pour les afficher et les combiner.

- **Combinaison d'images :**
  - Création d'images composites RGB en sélectionnant des canaux personnalisés pour chaque image.

- **Thèmes personnalisables :**
  - Choix entre plusieurs thèmes visuels (Clair, Sombre, Bleu Nuit, etc.).

## Prérequis

- Python 3.9 ou supérieur
- Bibliothèques Python :
  - `numpy`
  - `matplotlib`
  - `astropy`
  - `PyQt6`
  - `astroquery`


# Utilisation

## Lancer l'application

1. Démarrez l'application avec la commande suivante :

    ```bash
    python main.py
    ```

2. L'interface principale s'ouvrira avec :
   - Une barre de recherche en haut.
   - Des zones pour afficher les images individuelles.
   - Une section dédiée à l'image combinée.

---

## Rechercher un objet céleste

1. Entrez un nom dans la barre de recherche (par exemple, "Andromeda", "Tarantula", "Orion", "M45", etc.).
2. Appuyez sur **Entrée** pour Télécharger les images associées.
3. Les images disponibles seront automatiquement téléchargées et affichées.
4. Si l'objet n'est pas trouvé, un message s'affichera dans le terminal avec des suggestions, noter le nom suggeré.

---

## Charger des fichiers FITS localement

1. Cliquez sur le bouton **"Charger FITS"** dans la barre d'outils.
2. Sélectionnez un ou plusieurs fichiers `.fits` ou `.fit` sur votre ordinateur.
3. Les images seront chargées et affichées dans les zones dédiées.

---

## Combiner les images en RGB

1. Dans les menus déroulants situés sous chaque image, sélectionnez le canal à associer :
   - **R** : Rouge
   - **G** : Vert
   - **B** : Bleu
2. L'image combinée apparaîtra automatiquement dans la zone dédiée en bas de l'écran.

---

## Changer le thème

1. Dans la barre d'outils, sélectionnez un thème dans le menu déroulant (par exemple, Clair, Sombre, Bleu Nuit).
2. L'interface se mettra à jour selon le style du thème choisi.

---

# Architecture

## Modules principaux

- **`controller.py`** :
  - Contient la logique métier, notamment pour résoudre les cibles, télécharger des images et gérer leur combinaison.

- **`view.py`** :
  - Définit l'interface utilisateur en utilisant PyQt6.

- **`main.py`** :
  - Point d'entrée de l'application.

---

## Dossier `qss`

- Contient les fichiers de style pour personnaliser l'apparence de l'application.

---

# Problèmes connus

- Les images FITS doivent avoir les mêmes dimensions pour être combinées.
- Le fichier QSS du thème sélectionné doit exister, sinon un message d'erreur s'affichera.

