import sys
from astropy.io import fits
from astropy.visualization import ImageNormalize, LogStretch, MinMaxInterval
import matplotlib.pyplot as plt
import numpy as np
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QPushButton, QComboBox, QFileDialog, QWidget
)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


class AstroApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AstroApp")
        self.setGeometry(100, 100, 1200, 800)

        # Initialisation des widgets
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        layout = QVBoxLayout(self.central_widget)

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

    def load_images(self):
        """Charge trois images FITS et les affiche."""
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
        norm = ImageNormalize(self.combined_image, interval=MinMaxInterval(), stretch=LogStretch())
        im = ax.imshow(self.combined_image, cmap="gray", origin="lower", norm=norm)  # Utilisation d'un affichage neutre
        self.combined_canvas.figure.colorbar(im, ax=ax, orientation="vertical")
        ax.set_title("Image combinée")
        self.combined_canvas.draw()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    viewer = AstroApp()
    viewer.show()
    sys.exit(app.exec())
