from PyQt5.QtWidgets import QMainWindow
from view.GenererLien import Ui_GenererLien
from controller.GenererLienTrackIn_controller import GenererLienTrackInController




class GenererLienController(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_GenererLien()
        self.ui.setupUi(self)

        # Connexion du bouton
        
        self.ui.pushButton.clicked.connect(self.ouvrir_generer_lien_trackIn)

    def ouvrir_generer_lien_trackIn(self):
        self.trackIn_window = GenererLienTrackInController()
        self.trackIn_window.show()
        self.close()