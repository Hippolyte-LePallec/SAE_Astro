import sys
from PyQt6.QtWidgets import QApplication
from controller import AstroAppController

if __name__ == "__main__":
    app = QApplication(sys.argv)
    controller = AstroAppController()
    controller.view.show()
    sys.exit(app.exec())
