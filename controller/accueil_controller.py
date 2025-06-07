from PyQt5.QtWidgets import QMainWindow
from view.TrackSys import Ui_Accueil
from controller.GenererLien_controller import GenererLienController
from PyQt5.QtWidgets import QMainWindow


class AccueilController(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Accueil()
        self.ui.setupUi(self)

        # Connexion du bouton
        self.ui.pushButton.clicked.connect(self.ouvrir_generer_lien)

    def ouvrir_generer_lien(self):
        self.generer_window = QMainWindow()
        self.generer_lien_window = GenererLienController()
        self.generer_lien_window.show()
        self.close()