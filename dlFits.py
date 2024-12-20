import os
from astroquery.skyview import SkyView
import astropy.units as u


target = input("Entrez le nom de l'objet céleste : ").strip()

# Définir les surveys souhaités
surveys = ["DSS2 Red", "DSS2 Blue", "DSS2 IR"]
image_size = 0.5 * u.deg 

try:
    # Télécharger les fichiers FITS pour l'objet saisi
    fits_files = SkyView.get_images(position=target, survey=surveys, radius=image_size)

    # Vérifier si des images ont été retournées
    if fits_files:
        # Créer un dossier pour enregistrer les fichiers
        output_dir = target.replace(' ', '_')  
        os.makedirs(output_dir, exist_ok=True)

        # Sauvegarder les fichiers localement dans le dossier
        for i, fits_file in enumerate(fits_files):
            filename = os.path.join(output_dir, f"{surveys[i].replace(' ', '_')}.fits")
            fits_file[0].writeto(filename, overwrite=True)
            print(f"Fichier enregistré : {filename}")

        print(f"Tous les fichiers ont été enregistrés dans le dossier : {output_dir}")
    else:
        print(f"Aucune image trouvée pour l'objet : {target}")

except Exception as e:
    print(f"Une erreur s'est produite : {e}")
