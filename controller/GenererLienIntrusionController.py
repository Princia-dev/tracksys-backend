import os
import shutil
import subprocess
import webbrowser
import pyperclip
from datetime import datetime

from PyQt5.QtWidgets import QMainWindow, QInputDialog, QMessageBox
from PyQt5.QtGui import QGuiApplication

from view.GenererLienTrackIn import GenererLienTrackIn
from model.services.cuttly_service import shorten_url_cuttly
from model.services.zip_builder import create_intrusion_zip
from model.services.uploader import uploader_fileio
from model.services.email_checker import is_valid_email


class IntrusionController(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = GenererLienTrackIn()
        self.ui.setupUi(self)
        self.ui.pushButton_2.clicked.connect(self.generer_lien_intrusion)

        self.api_key_cuttly = "0535f0bbe820e467acc47a2b26cab681f1e80"

    def generer_lien_intrusion(self):
        email, ok = QInputDialog.getText(self, "Adresse email", "Entrez votre adresse email de réception :")
        if not ok or not is_valid_email(email):
            QMessageBox.warning(self, "Email invalide", "Veuillez entrer une adresse email valide.")
            return

        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        temp_dir = os.path.join("model", "temp")
        os.makedirs(temp_dir, exist_ok=True)
        zip_path = os.path.join(temp_dir, f"rapport_{timestamp}.zip")

        try:
            create_intrusion_zip(email, zip_path)
        except Exception as e:
            QMessageBox.critical(self, "Erreur ZIP", f"Erreur lors de la création du ZIP : {e}")
            return

        lien = uploader_fileio(zip_path)
        if not lien:
            QMessageBox.warning(self, "Erreur", "Impossible d'uploader le fichier.")
            return

        # Supprimer le zip après upload réussi
        try:
            os.remove(zip_path)
        except Exception as e:
            print(f"Erreur suppression zip temporaire : {e}")

        try:
            lien_court = shorten_url_cuttly(lien, self.api_key_cuttly)
        except Exception:
            lien_court = lien

        QGuiApplication.clipboard().setText(lien_court)
        self.partager_lien(lien_court, "Lien du fichier intrusif prêt à être partagé :")

    def partager_lien(self, lien, message="Voici votre lien prêt à être partagé :"):
        pyperclip.copy(lien)

        partage_box = QMessageBox(self)
        partage_box.setWindowTitle("Partager le lien")
        partage_box.setText(f"{message}\n\n{lien}")
        whatsapp_btn = partage_box.addButton("Partager sur WhatsApp", QMessageBox.ActionRole)
        facebook_btn = partage_box.addButton("Partager sur Facebook", QMessageBox.ActionRole)
        telegram_btn = partage_box.addButton("Partager sur Telegram", QMessageBox.ActionRole)
        copier_btn = partage_box.addButton("Copier seulement", QMessageBox.AcceptRole)
        partage_box.addButton("Annuler", QMessageBox.RejectRole)
        partage_box.exec_()

        if partage_box.clickedButton() == whatsapp_btn:
            webbrowser.open(f"https://wa.me/?text={lien}")
        elif partage_box.clickedButton() == facebook_btn:
            webbrowser.open(f"https://www.facebook.com/sharer/sharer.php?u={lien}")
        elif partage_box.clickedButton() == telegram_btn:
            webbrowser.open(f"https://t.me/share/url?url={lien}")
        elif partage_box.clickedButton() == copier_btn:
            QMessageBox.information(self, "Copié", "Lien copié dans le presse-papier.")