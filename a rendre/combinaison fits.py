import sys
import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QPushButton, QFileDialog, QWidget
)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


class AstroApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AstroApp")
        self.setGeometry(100, 100, 1200, 800)


        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        layout = QVBoxLayout(self.central_widget)

        self.load_button = QPushButton("Charger les images FITS")
        self.load_button.clicked.connect(self.load_images)
        layout.addWidget(self.load_button)


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
        self.combine_images()

    def combine_images(self):
        """Combine les images normalisées en une seule image avec autant de canaux que nécessaire."""
        if not self.image_data_list:
            return


        image_shape = self.image_data_list[0].shape
        for data in self.image_data_list:
            if data.shape != image_shape:
                print("Les images doivent avoir la même taille.")
                return


        num_images = len(self.image_data_list)
        combined_image = np.zeros((image_shape[0], image_shape[1], num_images))


        for i in range(num_images):
            combined_image[:, :, i] = self.image_data_list[i]

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


if __name__ == "__main__":
    app = QApplication(sys.argv)
    viewer = AstroApp()
    viewer.show()
    sys.exit(app.exec())
