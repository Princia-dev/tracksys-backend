import os
import re
import requests
import urllib.parse
import webbrowser
import pyperclip
import base64
from datetime import datetime

from PyQt5.QtWidgets import (
    QMainWindow, QInputDialog, QMessageBox, QFileDialog
)
from PyQt5.QtGui import QGuiApplication

from view.GenererLienTracking import GenererLienTracking
from model.services.cuttly_service import shorten_url_cuttly
from model.templates.html_generator_track import generate_image_tracker_html


class GenererLienTrackingController(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = GenererLienTracking()
        self.ui.setupUi(self)

        self.ui.pushButton.clicked.connect(self.generer_payload)
        self.ui.pushButton_2.clicked.connect(self.generer_lien_image)

        self.url_formsubmit_heberge = "princia.netlify.app"
        self.api_key_cuttly = "0535f0bbe820e467acc47a2b26cab681f1e80"

        self.github_token = "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"
        self.repo = "Princia-dev/tracksys-links"
        self.base_url = "https://tracksys-links.netlify.app"

       


    def generer_payload(self):
        email, ok = QInputDialog.getText(self, "Adresse email", "Entrez votre adresse email de réception :")
        if not ok or not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email):
            QMessageBox.warning(self, "Email invalide", "Veuillez entrer une adresse email valide.")
            return

        email_encode = urllib.parse.quote_plus(email)
        lien = f"https://{self.url_formsubmit_heberge}/tracker.html?email={email_encode}"

        try:
            lien_court = shorten_url_cuttly(lien, self.api_key_cuttly)
        except Exception:
            QMessageBox.warning(self, "Lien original", f"Impossible de raccourcir. Lien original :\n{lien}")
            lien_court = lien

        texte_message = lien_court
        action_box = QMessageBox(self)
        action_box.setWindowTitle("Lien généré")
        action_box.setText("Le lien traqueur a été généré. Que voulez-vous faire ?")
        envoyer_btn = action_box.addButton("Envoyer", QMessageBox.ActionRole)
        camoufler_btn = action_box.addButton("Camoufler", QMessageBox.ActionRole)
        action_box.addButton("Annuler", QMessageBox.RejectRole)
        action_box.exec_()

        if action_box.clickedButton() == camoufler_btn:
            texte, ok = QInputDialog.getText(self, "Texte du lien", "Entrez le texte à afficher pour camoufler le lien :")
            if ok and texte:
                texte_message = f"{texte} : {lien_court}"
                QMessageBox.information(self, "Lien camouflé", f"<a href='{lien_court}'>{texte}</a>")

        QGuiApplication.clipboard().setText(lien_court)
        self.partager_lien(lien_court, texte_message)


    def generer_lien_image(self):
        # 1. Demander l'email
        email, ok = QInputDialog.getText(self, "Adresse email", "Entrez votre adresse email de réception :")
        if not ok or not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email):
            QMessageBox.warning(self, "Email invalide", "Veuillez entrer une adresse email valide.")
            return

        # 2. Sélectionner une image locale
        image_path, _ = QFileDialog.getOpenFileName(self, "Choisir une image", "", "Images (*.png *.jpg *.jpeg *.gif)")
        if not image_path:
            QMessageBox.warning(self, "Aucune image", "Vous devez sélectionner une image.")
            return

        # 3. Upload de l'image sur GitHub
        image_filename = os.path.basename(image_path)
        image_url = self.uploader_sur_github(image_path, f"images/{image_filename}")
        if not image_url:
            QMessageBox.warning(self, "Erreur", "Échec de l’upload de l’image.")
            return

        # 4. Générer le HTML traqueur avec l’image
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        html_filename = f"image_tracker_{timestamp}.html"
        temp_dir = os.path.join("model", "temp")
        os.makedirs(temp_dir, exist_ok=True)
        html_local_path = os.path.join(temp_dir, html_filename)

        generate_image_tracker_html(email, image_url, html_local_path)

        # 5. Upload du fichier HTML sur GitHub
        html_url = self.uploader_sur_github(html_local_path, f"html/{html_filename}")
        if not html_url:
            return

        # 6. Raccourcir le lien (TinyURL ou Cuttly)
        try:
            lien_court = shorten_url_cuttly(html_url, self.api_key_cuttly)
        except Exception:
            lien_court = html_url

        QGuiApplication.clipboard().setText(lien_court)

        # 7. Partage du lien
        self.partager_lien(lien_court, "Lien vers image traqueur généré :")

    def generate_image_tracker_html(self, email, image_url, output_path):
        """Génère un fichier HTML avec image visible + tracking JS"""
        # On encode l'email pour l'URL JS côté client
        import urllib.parse
        email_js = urllib.parse.quote(email)

        html_template = f"""
    <!DOCTYPE html>
    <html>
    <head><meta charset="UTF-8"><title>Image Tracker</title></head>
    <body>
        <img src="{image_url}" alt="Image Tracker" />
        <script>
        fetch('https://tonserveur.com/track?email={email_js}&img=' + encodeURIComponent('{image_url}'))
        .catch(e => console.error('Erreur tracking:', e));
        </script>
        <p>Merci de votre visite.</p>
    </body>
    </html>
    """
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(html_template)
        

    def uploader_sur_github(self, chemin_fichier, nom_fichier):
        try:
            with open(chemin_fichier, "rb") as f:
                contenu = f.read()

            url = f"https://api.github.com/repos/{self.repo}/contents/{nom_fichier}"
            headers = {
                "Authorization": f"Bearer {self.github_token}",
                "Accept": "application/vnd.github+json"
            }

            # Vérifier si le fichier existe déjà
            sha = None
            res_get = requests.get(url, headers=headers)
            if res_get.status_code == 200:
                sha = res_get.json().get("sha")

            # Préparer les données pour la requête PUT
            data = {
                "message": f"Ajout ou mise à jour de {nom_fichier}",
                "content": base64.b64encode(contenu).decode("utf-8"),
            }
            if sha:
                data["sha"] = sha  # Ajoute le SHA si le fichier existe déjà

            # Envoyer la requête PUT
            res_put = requests.put(url, headers=headers, json=data)

            if res_put.status_code in [200, 201]:
                return f"{self.base_url}/{nom_fichier}"
            else:
                print("Erreur GitHub:", res_put.text)
                QMessageBox.warning(self, "Échec GitHub", f"Erreur lors de l'envoi sur GitHub :\n{res_put.text}")
                return None

        except Exception as e:
            QMessageBox.warning(self, "Erreur Upload", f"Erreur lors de l'upload GitHub :\n{str(e)}")
            return None


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