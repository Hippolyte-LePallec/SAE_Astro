import sys
import os
import numpy as np
from PyQt6.QtWidgets import QFileDialog
from astroquery.skyview import SkyView
from astroquery.jplhorizons import Horizons
from astropy.coordinates import SkyCoord
from astropy.io import fits
import astropy.units as u
from view import AstroAppView


class AstroAppController:
    def __init__(self):
        self.view = AstroAppView(self)
        self.image_data_list = []

    def resolve_target(self, target):
        """Résout le nom de l'objet céleste en coordonnées."""
        try:
            # Tenter avec SkyCoord
            coords = SkyCoord.from_name(target)
            print(f"Coordonnées résolues pour {target} (via SkyCoord): {coords.to_string('hmsdms')}")
            self.view.update_coordinates(coords)  # Affiche les coordonnées dans la vue
            return coords
        except Exception:
            print(f"SkyCoord ne peut pas résoudre {target}. Tentative via JPL Horizons...")
            try:
                # Tenter avec JPL Horizons
                obj = Horizons(id=target, location="@sun", epochs=None)
                eph = obj.ephemerides()
                coords = SkyCoord(eph['RA'][0], eph['DEC'][0], unit=(u.deg, u.deg), frame="icrs")
                print(f"Coordonnées résolues pour {target} (via JPL Horizons): {coords.to_string('hmsdms')}")
                self.view.update_coordinates(coords)  # Affiche les coordonnées dans la vue
                return coords
            except Exception as e:
                print(f"Impossible de résoudre {target} via JPL Horizons : {e}")
                self.view.update_coordinates(None)  # Affiche un message d'erreur
                return None

    def search_object(self):
        """Recherche un objet céleste et télécharge les images FITS associées."""
        target = self.view.search_bar.text().strip()
        if not target:
            print("Veuillez entrer un nom d'objet céleste.")
            return

        coordinates = self.resolve_target(target)
        if coordinates is None:
            print(f"Aucune coordonnée trouvée pour l'objet : {target}.")
            return

        surveys = ["DSS2 Red", "DSS2 Blue", "DSS2 IR"]
        image_size = 0.5 * u.deg

        try:
            fits_files = SkyView.get_images(position=coordinates, survey=surveys, radius=image_size)
            if fits_files:
                output_dir = os.path.join(target.replace(' ', '_'), "SkyView")
                os.makedirs(output_dir, exist_ok=True)

                self.image_data_list = []
                for i, fits_file in enumerate(fits_files):
                    filename = os.path.join(output_dir, f"{surveys[i].replace(' ', '_')}.fits")
                    fits_file[0].writeto(filename, overwrite=True)

                    with fits.open(filename) as hdul:
                        image_data = hdul[0].data
                        vmin, vmax = np.percentile(image_data, (1, 99))
                        normalized_data = np.clip((image_data - vmin) / (vmax - vmin), 0, 1)
                        self.image_data_list.append(normalized_data)

                print(f"Images téléchargées et enregistrées dans : {output_dir}")
                self.view.update_individual_images(self.image_data_list)
                self.combine_images()
            else:
                print(f"Aucune image trouvée pour l'objet : {target}")
        except Exception as e:
            print(f"Une erreur s'est produite : {e}")

    def load_images(self):
        """Charge plusieurs images FITS localement et les affiche."""
        file_paths, _ = QFileDialog.getOpenFileNames(
            self.view, "Sélectionnez des fichiers FITS", "", "FITS Files (*.fit *.fits)"
        )
        if not file_paths:
            print("Aucun fichier sélectionné.")
            return

        self.image_data_list = []
        for file_path in file_paths:
            try:
                with fits.open(file_path) as hdul:
                    image_data = hdul[0].data
                    vmin, vmax = np.percentile(image_data, (1, 99))
                    normalized_data = np.clip((image_data - vmin) / (vmax - vmin), 0, 1)
                    self.image_data_list.append(normalized_data)
            except Exception as e:
                print(f"Erreur lors du chargement du fichier FITS {file_path}: {e}")
                return

        print(f"{len(file_paths)} images FITS chargées avec succès.")
        self.view.update_individual_images(self.image_data_list)
        self.combine_images()

    def combine_images(self):
        """Combine les images normalisées en une seule image RGB selon les canaux sélectionnés."""
        if not self.image_data_list:
            return

        image_shape = self.image_data_list[0].shape
        for data in self.image_data_list:
            if data.shape != image_shape:
                print("Les images doivent avoir la même taille.")
                return

        combined_image = np.zeros((image_shape[0], image_shape[1], 3))

        # Met à jour l'image combinée selon la sélection de chaque canal
        for i in range(min(len(self.image_data_list), 3)):
            channel = self.view.channel_selectors[i].currentText()  # Récupère le canal sélectionné
            if channel == "R":
                combined_image[:, :, 0] = self.image_data_list[i]  # Canal rouge
            elif channel == "G":
                combined_image[:, :, 1] = self.image_data_list[i]  # Canal vert
            elif channel == "B":
                combined_image[:, :, 2] = self.image_data_list[i]  # Canal bleu

        self.view.update_combined_image(combined_image)