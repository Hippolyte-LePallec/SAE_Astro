from astroquery.skyview import SkyView

# Définir les paramètres
objet = "Andromeda"  # Nom de l'objet céleste (ou donner des coordonnées comme "10.684, 41.269")
surveys = ["SWIFT"]  # Liste des missions, ici le Digitized Sky Survey
pixels = 500  # Taille de l'image en pixels (pour une image plus grande ou plus précise)
file_format = "fits"  # Format de sortie

# Télécharger les fichiers FITS
images = SkyView.get_images(position=objet, survey=surveys, pixels=pixels, cache=True)

# Sauvegarder les fichiers téléchargés localement
for i, image in enumerate(images):
    filename = f"{objet}_image_{i}.fits"
    image.writeto(filename, overwrite=True)
    print(f"Image {i+1} sauvegardée sous le nom {filename}")
