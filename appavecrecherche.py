import sys
from astropy.io import fits
from astropy.visualization import ImageNormalize, LogStretch, MinMaxInterval
import matplotlib.pyplot as plt
import numpy as np
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QPushButton, QComboBox, QFileDialog, QLineEdit, QLabel, QWidget
)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from astroquery.mast import Observations
from astropy.coordinates import SkyCoord
import astropy.units as u
import os


class AstroApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AstroApp")
        self.setGeometry(100, 100, 1200, 800)

        # Initialisation des widgets
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        layout = QVBoxLayout(self.central_widget)

        # Barre de recherche
        search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Entrez un objet céleste (ex. : Tarantula)")
        self.search_button = QPushButton("Rechercher et télécharger")
        self.search_button.clicked.connect(self.search_and_download)
        search_layout.addWidget(QLabel("Recherche d'objet :"))
        search_layout.addWidget(self.search_input)
        search_layout.addWidget(self.search_button)
        layout.addLayout(search_layout)

        # Ajout des trois images individuelles avec sélecteurs de palette
        self.image_canvases = []
        self.colormap_selectors = []
        self.image_data_list = []

        images_layout = QHBoxLayout()
        for i in range(3):
            # Création de la figure et du sélecteur de palette
            canvas = FigureCanvas(plt.figure())
            self.image_canvases.append(canvas)
            colormap_selector = QComboBox()
            colormap_selector.addItems(plt.colormaps())
            # Connecter la mise à jour de l'image individuelle
            colormap_selector.currentTextChanged.connect(lambda _, idx=i: self.update_individual_image(idx))
            # Connecter la mise à jour de l'image combinée
            colormap_selector.currentTextChanged.connect(self.combine_images)
            self.colormap_selectors.append(colormap_selector)

            # Ajout dans un sous-layout
            image_layout = QVBoxLayout()
            image_layout.addWidget(canvas)
            image_layout.addWidget(colormap_selector)
            images_layout.addLayout(image_layout)

        layout.addLayout(images_layout)

        # Ajout de l'image combinée
        self.combined_canvas = FigureCanvas(plt.figure())
        layout.addWidget(self.combined_canvas)

        # Bouton de chargement
        self.load_button = QPushButton("Ouvrir les images FITS")
        self.load_button.clicked.connect(self.load_images)
        layout.addWidget(self.load_button)

        self.combined_image = None

    def search_and_download(self):
        """Recherche et télécharge les fichiers FITS pour l'objet entré."""
        object_name = self.search_input.text().strip()
        if not object_name:
            print("Veuillez entrer un nom d'objet.")
            return

        print(f"Recherche pour l'objet : {object_name}")
        radius = 0.1 * u.deg
        output_dir = "fits_downloads"
        os.makedirs(output_dir, exist_ok=True)

        try:
            # Obtenir les coordonnées de l'objet
            coordinates = SkyCoord.from_name(object_name)
            print(f"Coordonnées de {object_name} : {coordinates}")

            # Rechercher les observations
            obs_table = Observations.query_region(coordinates, radius=radius)
            missions = ['JWST', 'HST']  # Filtrer par mission
            filtered_obs_table = obs_table[np.isin(obs_table['obs_collection'], missions)]

            if len(filtered_obs_table) == 0:
                print(f"Aucune observation trouvée pour {object_name}.")
                return

            # Récupérer les produits FITS
            products = Observations.get_product_list(filtered_obs_table)
            filtered_products = products[np.char.endswith(products['productFilename'].astype(str), '.fits')]

            if len(filtered_products) == 0:
                print("Aucun produit FITS trouvé.")
                return

            # Télécharger les fichiers FITS
            manifest = Observations.download_products(filtered_products, download_dir=output_dir)
            downloaded_files = manifest['Local Path']
            print(f"Fichiers téléchargés : {downloaded_files}")

            # Charger les images dans l'application
            self.image_data_list = []
            for file in downloaded_files:
                if file.endswith(".fits"):
                    with fits.open(file) as hdul:
                        image_data = hdul[0].data
                        self.image_data_list.append(np.nan_to_num(image_data, nan=0.0, posinf=0.0, neginf=0.0))

            print(f"{len(self.image_data_list)} images FITS chargées.")
            self.update_individual_images()
            self.combine_images()

        except Exception as e:
            print(f"Erreur lors de la recherche ou du téléchargement : {e}")

    def load_images(self):
        """Charge trois images FITS depuis des fichiers locaux."""
        file_paths, _ = QFileDialog.getOpenFileNames(
            self, "Sélectionnez trois fichiers FITS", "", "FITS Files (*.fit *.fits)"
        )

        if len(file_paths) != 3:
            print("Veuillez sélectionner exactement trois fichiers FITS.")
            return

        self.image_data_list = []
        for i, file_path in enumerate(file_paths):
            try:
                with fits.open(file_path) as hdul:
                    image_data = hdul[0].data
                    self.image_data_list.append(np.nan_to_num(image_data, nan=0.0, posinf=0.0, neginf=0.0))
            except Exception as e:
                print(f"Erreur lors du chargement du fichier FITS {i + 1}: {e}")
                return

        print("Trois images FITS chargées avec succès.")
        self.update_individual_images()
        self.combine_images()

    def update_individual_images(self):
        """Affiche les trois images individuelles."""
        for i in range(3):
            self.update_individual_image(i)

    def update_individual_image(self, index):
        """Met à jour l'image individuelle avec le filtre sélectionné."""
        if index >= len(self.image_data_list):
            return

        canvas = self.image_canvases[index]
        colormap = self.colormap_selectors[index].currentText()
        image_data = self.image_data_list[index]

        canvas.figure.clear()
        ax = canvas.figure.add_subplot(111)
        norm = ImageNormalize(image_data, interval=MinMaxInterval(), stretch=LogStretch())
        ax.imshow(image_data, cmap=colormap, origin="lower", norm=norm)
        ax.set_title(f"Image {index + 1}")
        canvas.draw()

    def combine_images(self):
        """Combine les images avec leurs filtres appliqués tout en conservant les couleurs."""
        if not self.image_data_list:
            return

        # Appliquer les colormaps aux images
        combined_rgba = None
        for i, image_data in enumerate(self.image_data_list):
            colormap = self.colormap_selectors[i].currentText()
            norm = ImageNormalize(image_data, interval=MinMaxInterval(), stretch=LogStretch())
            rgba_image = plt.cm.get_cmap(colormap)(norm(image_data))  # Génère un tableau RGBA

            # Initialisation ou accumulation des images RGBA
            if combined_rgba is None:
                combined_rgba = rgba_image
            else:
                combined_rgba[:, :, :3] += rgba_image[:, :, :3]  # Additionner les couleurs RGB
                combined_rgba[:, :, 3] = np.maximum(combined_rgba[:, :, 3], rgba_image[:, :, 3])  # Gérer l'opacité

        # Normalisation des couleurs après combinaison
        combined_rgba[:, :, :3] /= np.max(combined_rgba[:, :, :3])  # Échelle entre 0 et 1

        # Mise à jour de l'image combinée
        self.combined_image = combined_rgba
        self.update_combined_image()

    def update_combined_image(self):
        """Affiche l'image combinée."""
        if self.combined_image is None:
            return

        self.combined_canvas.figure.clear()
        ax = self.combined_canvas.figure.add_subplot(111)
        ax.imshow(self.combined_image, origin="lower")  # Utilisation d'un affichage neutre
        ax.set_title("Image combinée")
        self.combined_canvas.draw()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    viewer = AstroApp()
    viewer.show()
    sys.exit(app.exec())
