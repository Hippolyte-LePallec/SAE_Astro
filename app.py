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

        # Ajout des trois images individuelles
        self.image_canvases = [FigureCanvas(plt.figure()) for _ in range(3)]
        images_layout = QHBoxLayout()
        for canvas in self.image_canvases:
            images_layout.addWidget(canvas)
        layout.addLayout(images_layout)

        # Ajout de l'image combinée
        self.combined_canvas = FigureCanvas(plt.figure())
        layout.addWidget(self.combined_canvas)

        # Sélecteur de palette de couleurs
        self.colormap_selector = QComboBox()
        self.colormap_selector.addItems(plt.colormaps())
        self.colormap_selector.currentTextChanged.connect(self.update_combined_image)
        layout.addWidget(self.colormap_selector)

        # Bouton de chargement
        self.load_button = QPushButton("Charger les images FITS")
        self.load_button.clicked.connect(self.load_images)
        layout.addWidget(self.load_button)

        # Données des images
        self.image_data_list = []
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
        for i, (canvas, image_data) in enumerate(zip(self.image_canvases, self.image_data_list)):
            canvas.figure.clear()
            ax = canvas.figure.add_subplot(111)
            norm = ImageNormalize(image_data, interval=MinMaxInterval(), stretch=LogStretch())
            ax.imshow(image_data, cmap="gray", origin="lower", norm=norm)
            ax.set_title(f"Image {i + 1}")
            canvas.draw()

    def combine_images(self):
        """Combine les trois images en utilisant la moyenne."""
        try:
            self.combined_image = np.mean(self.image_data_list, axis=0)
            self.update_combined_image()
        except Exception as e:
            print(f"Erreur lors de la combinaison des images : {e}")

    def update_combined_image(self):
        """Affiche l'image combinée."""
        if self.combined_image is None:
            return

        colormap = self.colormap_selector.currentText()
        self.combined_canvas.figure.clear()
        ax = self.combined_canvas.figure.add_subplot(111)
        norm = ImageNormalize(self.combined_image, interval=MinMaxInterval(), stretch=LogStretch())
        im = ax.imshow(self.combined_image, cmap=colormap, origin="lower", norm=norm)
        self.combined_canvas.figure.colorbar(im, ax=ax, orientation="vertical")
        ax.set_title("Image combinée")
        self.combined_canvas.draw()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    viewer = AstroApp()
    viewer.show()
    sys.exit(app.exec())
