import sys
from PyQt5.QtWidgets import QApplication
from controller.accueil_controller import AccueilController


if __name__ == "__main__":
    app = QApplication(sys.argv) 
    controller = AccueilController()
    controller.show()
    sys.exit(app.exec_())