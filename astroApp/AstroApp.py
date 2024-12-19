import sys
import os
import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QPushButton, QFileDialog,
    QWidget, QToolBar, QComboBox, QLabel,QLineEdit
)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


class AstroApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AstroApp")

        
        self.toolbar = QToolBar("Barre d'outils")
        self.addToolBar(self.toolbar)

        
        self.load_button = QPushButton("Charger FITS")
        self.load_button.clicked.connect(self.load_images)
        self.toolbar.addWidget(self.load_button)

       
        self.theme_selector = QComboBox()
        self.theme_selector.addItems(["Clair", "Sombre", "Bleu Nuit", "Irrorater", "Combinear"])
        self.theme_selector.currentTextChanged.connect(self.change_theme)
        self.toolbar.addWidget(self.theme_selector)

        
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("rechercher des missions")
        self.toolbar.addWidget(self.search_bar)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        layout = QVBoxLayout(self.central_widget)

        
        self.image_canvases = []
        self.channel_selectors = []
        images_layout = QHBoxLayout()
        for i in range(3):  
            image_layout = QVBoxLayout()
            canvas = FigureCanvas(plt.figure())
            self.image_canvases.append(canvas)
            image_layout.addWidget(canvas)

            
            channel_selector = QComboBox()
            channel_selector.addItems(["R", "G", "B"])
            channel_selector.currentIndexChanged.connect(self.combine_images)
            self.channel_selectors.append(channel_selector)
            image_layout.addWidget(channel_selector)

            images_layout.addLayout(image_layout)
        layout.addLayout(images_layout)

        
        self.combined_canvas = FigureCanvas(plt.figure())
        layout.addWidget(self.combined_canvas)

        
        self.image_data_list = []

    def load_images(self):
        """Charge plusieurs images FITS et les affiche."""
        file_paths, _ = QFileDialog.getOpenFileNames(
            self, "Sélectionnez des fichiers FITS", "", "FITS Files (*.fit *.fits)"
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
        self.update_individual_images()
        self.combine_images()

    def update_individual_images(self):
        """Affiche chaque image individuelle."""
        for i, canvas in enumerate(self.image_canvases):
            if i < len(self.image_data_list):
                image_data = self.image_data_list[i]
                canvas.figure.clear()
                ax = canvas.figure.add_subplot(111)
                ax.imshow(image_data, origin='lower', cmap='gray')
                ax.set_title(f"Image {i + 1}")
                canvas.draw()

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

        for i in range(min(len(self.image_data_list), 3)):
            channel = self.channel_selectors[i].currentText()
            if channel == "R":
                combined_image[:, :, 0] = self.image_data_list[i]
            elif channel == "G":
                combined_image[:, :, 1] = self.image_data_list[i]
            elif channel == "B":
                combined_image[:, :, 2] = self.image_data_list[i]

        self.update_combined_image(combined_image)

    def update_combined_image(self, combined_image):
        """Affiche l'image combinée."""
        if combined_image is None:
            return

        self.combined_canvas.figure.clear()
        ax = self.combined_canvas.figure.add_subplot(111)
        ax.imshow(combined_image, origin='lower')
        ax.set_title("Image combinée")
        self.combined_canvas.draw()

    def change_theme(self, theme):
        """Change le thème en chargeant un fichier QSS."""
        theme_files = {
            "Clair": "qss/clair.qss",
            "Sombre": "qss/sombre.qss",
            "Bleu Nuit": "qss/bleu_nuit.qss",
            "Irrorater": "qss/Irrorater.qss",
            "Combinear": "qss/Combinear.qss",
        }

        if theme in theme_files:
            qss_file = theme_files[theme]
            try:
                # Construire un chemin absolu basé sur l'emplacement actuel du script
                qss_path = os.path.join(os.path.dirname(__file__), qss_file)
                with open(qss_path, "r") as f:
                    self.setStyleSheet(f.read())
            except FileNotFoundError:
                print(f"Le fichier {qss_path} est introuvable.")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    viewer = AstroApp()
    viewer.show()
    sys.exit(app.exec())
