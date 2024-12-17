import sys
import numpy as np
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QPushButton, QSlider, QLabel, QComboBox, QFileDialog, QWidget
)
from PyQt6.QtCore import Qt
from matplotlib.backends.backend_qt5agg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar
)
import matplotlib.pyplot as plt
from astropy.io import fits
from astropy.visualization import ImageNormalize, LogStretch, MinMaxInterval

class FitsViewer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("FITS Viewer avec PyQt6")
        self.setGeometry(100, 100, 800, 600)

        # Widget principal
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        layout = QVBoxLayout(self.central_widget)

        # Canvas pour afficher l'image
        self.canvas = FigureCanvas(plt.figure())
        layout.addWidget(NavigationToolbar(self.canvas, self))
        layout.addWidget(self.canvas)

        # Panneau de contrôle
        controls_layout = QHBoxLayout()

        # Bouton pour charger les fichiers FITS
        self.load_button = QPushButton("Charger 3 FITS")
        self.load_button.clicked.connect(self.load_fits)
        controls_layout.addWidget(self.load_button)

        # Contrôle des contrastes avec un slider
        self.contrast_label = QLabel("Contraste :")
        controls_layout.addWidget(self.contrast_label)

        self.contrast_slider = QSlider(Qt.Orientation.Horizontal)
        self.contrast_slider.setMinimum(1)
        self.contrast_slider.setMaximum(100)
        self.contrast_slider.setValue(99)
        self.contrast_slider.sliderReleased.connect(self.update_image)
        controls_layout.addWidget(self.contrast_slider)

        # Sélecteur de palettes de couleurs
        self.colormap_label = QLabel("Palette :")
        controls_layout.addWidget(self.colormap_label)

        self.colormap_selector = QComboBox()
        self.colormap_selector.addItems(["Accent", "Accent_r", "Blues", "Blues_r", "BrBG", "BrBG_r", "BuGn", "BuGn_r", "BuPu", "BuPu_r", 
    "CMRmap", "CMRmap_r", "Dark2", "Dark2_r", "GnBu", "GnBu_r", "Grays", "Greens", "Greens_r", "Greys", 
    "Greys_r", "OrRd", "OrRd_r", "Oranges", "Oranges_r", "PRGn", "PRGn_r", "Paired", "Paired_r", 
    "Pastel1", "Pastel1_r", "Pastel2", "Pastel2_r", "PiYG", "PiYG_r", "PuBu", "PuBuGn", "PuBuGn_r", 
    "PuBu_r", "PuOr", "PuOr_r", "PuRd", "PuRd_r", "Purples", "Purples_r", "RdBu", "RdBu_r", "RdGy", 
    "RdGy_r", "RdPu", "RdPu_r", "RdYlBu", "RdYlBu_r", "RdYlGn", "RdYlGn_r", "Reds", "Reds_r", "Set1", 
    "Set1_r", "Set2", "Set2_r", "Set3", "Set3_r", "Spectral", "Spectral_r", "Wistia", "Wistia_r", 
    "YlGn", "YlGnBu", "YlGnBu_r", "YlGn_r", "YlOrBr", "YlOrBr_r", "YlOrRd", "YlOrRd_r", "afmhot", 
    "afmhot_r", "autumn", "autumn_r", "binary", "binary_r", "bone", "bone_r", "brg", "brg_r", "bwr", 
    "bwr_r", "cividis", "cividis_r", "cool", "cool_r", "coolwarm", "coolwarm_r", "copper", "copper_r", 
    "cubehelix", "cubehelix_r", "flag", "flag_r", "gist_earth", "gist_earth_r", "gist_gray", 
    "gist_gray_r", "gist_grey", "gist_heat", "gist_heat_r", "gist_ncar", "gist_ncar_r", "gist_rainbow", 
    "gist_rainbow_r", "gist_stern", "gist_stern_r", "gist_yarg", "gist_yarg_r", "gist_yerg", "gnuplot", 
    "gnuplot2", "gnuplot2_r", "gnuplot_r", "gray", "gray_r", "grey", "hot", "hot_r", "hsv", "hsv_r", 
    "inferno", "inferno_r", "jet", "jet_r", "magma", "magma_r", "nipy_spectral", "nipy_spectral_r", 
    "ocean", "ocean_r", "pink", "pink_r", "plasma", "plasma_r", "prism", "prism_r", "rainbow", 
    "rainbow_r", "seismic", "seismic_r", "spring", "spring_r", "summer", "summer_r", "tab10", 
    "tab10_r", "tab20", "tab20_r", "tab20b", "tab20b_r", "tab20c", "tab20c_r", "terrain", "terrain_r", 
    "turbo", "turbo_r", "twilight", "twilight_r", "twilight_shifted", "twilight_shifted_r", "viridis", 
    "viridis_r", "winter", "winter_r"])
        self.colormap_selector.currentTextChanged.connect(self.update_image)
        controls_layout.addWidget(self.colormap_selector)

        layout.addLayout(controls_layout)

        # Initialisation des données
        self.image_data_list = []
        self.combined_image = None

    def load_fits(self):
        """Charger trois fichiers FITS."""
        self.image_data_list = []

        for i in range(3):
            file_path, _ = QFileDialog.getOpenFileName(self, f"Ouvrir l'image FITS {i+1}", "", "FITS Files (*.fit *.fits)")
            if file_path:
                try:
                    hdul = fits.open(file_path)
                    image_data = hdul[0].data
                    hdul.close()

                    # Nettoyage des données
                    image_data = np.nan_to_num(image_data, nan=0.0, posinf=0.0, neginf=0.0)
                    self.image_data_list.append(image_data)

                except Exception as e:
                    print(f"Erreur lors du chargement du fichier FITS {i+1} : {e}")
                    return

        if len(self.image_data_list) == 3:
            print("Trois images FITS chargées avec succès.")
            self.combine_images()
        else:
            print("Veuillez charger trois images FITS.")

    def combine_images(self):
        """Combiner les trois images FITS par la moyenne."""
        try:
            self.combined_image = np.mean(self.image_data_list, axis=0)
            self.update_image()
        except Exception as e:
            print(f"Erreur lors de la combinaison des images : {e}")

    def update_image(self):
        """Met à jour l'affichage de l'image en fonction des paramètres."""
        if self.combined_image is None:
            return

        # Récupérer les paramètres de contraste
        vmin = np.percentile(self.combined_image, 1)
        vmax = np.percentile(self.combined_image, self.contrast_slider.value())

        # Palette de couleurs
        colormap = self.colormap_selector.currentText()

        # Création de la normalisation
        norm = ImageNormalize(self.combined_image, interval=MinMaxInterval(), stretch=LogStretch(), vmin=vmin, vmax=vmax)

        # Mise à jour de l'affichage
        self.canvas.figure.clear()
        ax = self.canvas.figure.add_subplot(111)
        im = ax.imshow(self.combined_image, cmap=colormap, origin="lower", norm=norm)
        self.canvas.figure.colorbar(im, ax=ax, orientation="vertical")
        ax.set_title("Image FITS combinée")
        self.canvas.draw()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    viewer = FitsViewer()
    viewer.show()
    sys.exit(app.exec())