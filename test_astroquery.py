# essaye d'ajouter ça à l'appli en gros il donne plus d'info à skyview ce qui permet de trouver plus d'images
# mais faut faire en sorte que ça crash pas quand tu tape pas le bon nom d'objet
# test tu verra c'est sympa

import os
from astroquery.skyview import SkyView
from astroquery.jplhorizons import Horizons
from astropy.coordinates import SkyCoord
import astropy.units as u

# Fonction pour résoudre les coordonnées
def resolve_target(target):
    try:
        # Tenter d'abord avec SkyCoord (pour les objets fixes)
        coords = SkyCoord.from_name(target)
        print(f"Coordonnées résolues pour {target} (via SkyCoord): {coords.to_string('hmsdms')}")
        return coords
    except Exception:
        print(f"SkyCoord ne peut pas résoudre {target}. Tentative via JPL Horizons...")

        try:
            # Utiliser JPL Horizons pour les objets du système solaire
            obj = Horizons(id=target, location="@sun", epochs=None)
            eph = obj.ephemerides()
            coords = SkyCoord(eph['RA'][0], eph['DEC'][0], unit=(u.deg, u.deg), frame="icrs")
            print(f"Coordonnées résolues pour {target} (via JPL Horizons): {coords.to_string('hmsdms')}")
            return coords
        except Exception as e:
            print(f"Impossible de résoudre {target} via JPL Horizons : {e}")
            return None

# Entrée utilisateur pour le nom de l'objet céleste
target = input("Entrez le nom de l'objet céleste : ").strip()

# Résoudre les coordonnées
coordinates = resolve_target(target)

# Si les coordonnées ne sont pas trouvées, arrêter le script
if coordinates is None:
    print(f"Aucune coordonnée trouvée pour l'objet : {target}. Vérifiez le nom de l'objet.")
    exit()

# Définir les surveys souhaités pour SkyView
surveys = ["DSS2 Red", "DSS2 Blue", "DSS2 IR"]
image_size = 0.5 * u.deg  # Taille de l'image

# Fonction pour rechercher et sauvegarder les images de SkyView
def fetch_skyview_images(coords, target, surveys, image_size):
    try:
        # Télécharger les fichiers FITS pour les coordonnées résolues
        fits_files = SkyView.get_images(position=coords, survey=surveys, radius=image_size)

        if fits_files:
            # Créer un dossier pour enregistrer les fichiers
            output_dir = os.path.join(target.replace(' ', '_'), "SkyView")
            os.makedirs(output_dir, exist_ok=True)

            # Sauvegarder les fichiers localement
            for i, fits_file in enumerate(fits_files):
                filename = os.path.join(output_dir, f"{surveys[i].replace(' ', '_')}.fits")
                fits_file[0].writeto(filename, overwrite=True)
                print(f"Fichier SkyView enregistré : {filename}")

            print(f"Tous les fichiers SkyView ont été enregistrés dans le dossier : {output_dir}")
        else:
            print(f"Aucune image trouvée dans SkyView pour l'objet : {target}")
    except Exception as e:
        print(f"Une erreur s'est produite avec SkyView : {e}")

# Appeler les fonctions pour SkyView
fetch_skyview_images(coordinates, target, surveys, image_size)