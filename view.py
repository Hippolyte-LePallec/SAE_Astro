import os 
from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QHBoxLayout, QPushButton, QComboBox, QLabel, QLineEdit, QToolBar, QWidget
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt

class AstroAppView(QMainWindow):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.setWindowTitle("AstroApp")
        self.toolbar = QToolBar("Barre d'outils")
        self.addToolBar(self.toolbar)


        self.load_button = QPushButton("Charger FITS")
        self.load_button.clicked.connect(self.controller.load_images)
        self.toolbar.addWidget(self.load_button)


        self.theme_selector = QComboBox()
        self.theme_selector.addItems(["Clair", "Sombre", "Bleu Nuit", "Irrorater", "Combinear"])
        self.theme_selector.currentTextChanged.connect(self.change_theme)
        self.toolbar.addWidget(self.theme_selector)


        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Rechercher des missions ou objets célestes")
        self.search_bar.returnPressed.connect(self.controller.search_object)
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
            channel_selector.currentIndexChanged.connect(self.controller.combine_images)  # Assure la mise à jour de l'image combinée
            self.channel_selectors.append(channel_selector)
            image_layout.addWidget(channel_selector)

            images_layout.addLayout(image_layout)
        layout.addLayout(images_layout)

        self.combined_canvas = FigureCanvas(plt.figure())
        layout.addWidget(self.combined_canvas)


        self.coord_label = QLabel("Coordonnées : N/A")
        layout.addWidget(self.coord_label)

    def update_coordinates(self, coordinates):
        """Affiche les coordonnées résolues de l'objet céleste."""
        if coordinates is not None:
            self.coord_label.setText(f"Coordonnées : {coordinates.to_string('hmsdms')}")
        else:
            self.coord_label.setText("Coordonnées : Impossible de résoudre l'objet.")

    def update_combined_image(self, combined_image):
        """Affiche l'image combinée."""
        if combined_image is None:
            return

        self.combined_canvas.figure.clear()
        ax = self.combined_canvas.figure.add_subplot(111)
        ax.imshow(combined_image, origin='lower')
        ax.set_title("Image combinée")
        self.combined_canvas.draw()

    def update_individual_images(self, image_data_list):
        """Affiche chaque image individuelle."""
        for i, canvas in enumerate(self.image_canvases):
            if i < len(image_data_list):
                image_data = image_data_list[i]
                canvas.figure.clear()
                ax = canvas.figure.add_subplot(111)
                ax.imshow(image_data, origin='lower', cmap='gray')
                ax.set_title(f"Image {i + 1}")
                canvas.draw()

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
                qss_path = os.path.join(os.path.dirname(__file__), qss_file)
                with open(qss_path, "r") as f:
                    self.setStyleSheet(f.read())
            except FileNotFoundError:
                print(f"Le fichier {qss_path} est introuvable.")