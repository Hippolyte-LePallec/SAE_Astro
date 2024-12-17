from astroquery.mast import Observations
from astropy.coordinates import SkyCoord
import astropy.units as u
from astropy.io import fits
import numpy as np
import os

# Paramètres
object_name = "Andromeda"
radius = 0.1 * u.deg  # Rayon élargi
output_dir = "fits_downloads"

# Étape 1 : Convertir le nom en coordonnées
coordinates = SkyCoord.from_name(object_name)
print(f"Coordonnées de {object_name} : {coordinates}")

# Étape 2 : Rechercher toutes les observations autour de l'objet
obs_table = Observations.query_region(coordinates, radius=radius)
print(f"Nombre total d'observations trouvées : {len(obs_table)}")

# Étape 3 : Afficher les missions disponibles
available_missions = set(obs_table['obs_collection'])
print("Missions disponibles :", available_missions)

# Filtrer manuellement par mission
missions = ['JWST']  # Utilise une mission fiable comme Hubble
filtered_obs_table = obs_table[np.isin(obs_table['obs_collection'], missions)]
print(f"Nombre d'observations après filtrage par mission : {len(filtered_obs_table)}")

# Si aucune observation n'est trouvée, essayer avec une autre mission
if len(filtered_obs_table) == 0:
    print(f"Aucune observation trouvée pour la mission {missions}. Essayons avec une autre mission.")
    missions = ['HST']  # Par exemple, essayer Hubble (HST)
    filtered_obs_table = obs_table[np.isin(obs_table['obs_collection'], missions)]
    print(f"Nombre d'observations après filtrage par mission {missions} : {len(filtered_obs_table)}")

# Étape 4 : Récupérer les produits FITS associés aux observations filtrées
if len(filtered_obs_table) > 0:
    products = Observations.get_product_list(filtered_obs_table)
    print(f"Nombre total de produits trouvés : {len(products)}")
    print("Colonnes disponibles dans les produits :", products.colnames)

    # Filtrer uniquement les produits avec une extension .fits
    filtered_products = products[np.char.endswith(products['productFilename'].astype(str), '.fits')]
    print(f"Nombre de produits FITS filtrés : {len(filtered_products)}")

    # Étape 5 : Télécharger les fichiers FITS
    if len(filtered_products) == 0:
        print("Aucun produit FITS trouvé après filtrage.")
    else:
        os.makedirs(output_dir, exist_ok=True)
        manifest = Observations.download_products(filtered_products, download_dir=output_dir)
        print("Téléchargement terminé.")

        # Vérifier les coordonnées des fichiers téléchargés
        for file_info in manifest['Local Path']:
            if file_info.endswith('.fits'):
                with fits.open(file_info) as hdul:
                    header = hdul[0].header
                    ra = header.get('RA')
                    dec = header.get('DEC')
                    print(f"Fichier : {file_info} | RA : {ra} | DEC : {dec}")
else:
    print("Aucune observation filtrée disponible pour télécharger des produits.")
