from astroquery.skyview import SkyView
import astropy.units as u  # Import des unités

# Demander à l'utilisateur de saisir le nom de l'objet
target = input("Entrez le nom de l'objet céleste (par ex., M31 pour Andromède) : ").strip()

# Définir les surveys souhaités
surveys = ["DSS2 Red", "DSS2 Blue", "DSS2 IR"]  # Vous pouvez adapter cette liste si nécessaire
image_size = 0.5 * u.deg  # Taille de l'image avec unités (en degrés)

try:
    # Télécharger les fichiers FITS pour l'objet saisi
    fits_files = SkyView.get_images(position=target, survey=surveys, radius=image_size)

    # Sauvegarder les fichiers localement
    for i, fits_file in enumerate(fits_files):
        filename = f"{target.replace(' ', '_')}_{surveys[i].replace(' ', '_')}.fits"
        fits_file[0].writeto(filename, overwrite=True)
        print(f"Fichier enregistré : {filename}")

except Exception as e:
    print(f"Une erreur s'est produite : {e}")

