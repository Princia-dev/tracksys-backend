from PyQt5.QtWidgets import QMainWindow
from view.GenererLienTrackIn import GenererLienTrackIn
from controller.GenererLienTracking_controller import GenererLienTrackingController
from controller.GenererLienIntrusionController import IntrusionController
from PyQt5.QtWidgets import QMainWindow

class GenererLienTrackInController(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = GenererLienTrackIn()
        self.ui.setupUi(self)

    #     # Connexion des boutons de la page finale
        self.ui.pushButton.clicked.connect(self.generer_tracking)
        self.ui.pushButton_2.clicked.connect(self.generer_intrusion)

    def generer_tracking(self):
      
        self.tracking_window = GenererLienTrackingController()
        self.tracking_window.show()
        self.close() 

    def generer_intrusion(self):
        self.intrusion_window = IntrusionController()
        self.intrusion_window.show()
        self.close()