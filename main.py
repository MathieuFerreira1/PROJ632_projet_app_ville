import datetime
import json
import sys
import folium
import requests
import math

from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWebChannel import QWebChannel
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *

from shapely.geometry import Point, Polygon


# Fenêtre d'accueil de l'application
class HomeWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.html = None
        self.ville = None
        self.filtre = {}
        self.initUI()

        # Setup de l'icône et du nom de l'application
        self.setWindowTitle("Travel App")
        self.setWindowIcon(QIcon("png/voyage.png"))

    def initUI(self):
        self.setFixedSize(405, 900)

        # Création du widget principal
        widget = QWidget()

        # Création des widgets enfants
        self.titre = QLabel("Travel App", self)
        self.titre.setGeometry(10, 0, 405, 100)
        self.titre.setStyleSheet("Font-size : 40px; font-weight: bold;text-align: center;")
        self.titre.setAlignment(Qt.AlignCenter)
        self.search_label = QLabel("Ville :", self)
        self.search_label.setStyleSheet("font-size : 20px;")
        self.search_box = QLineEdit()
        self.search_box.setStyleSheet("font-size : 25px")
        self.filter1 = QCheckBox("Bar")
        self.filter1.setStyleSheet("font-size :15px")
        self.filter2 = QCheckBox("Restaurant")
        self.filter3 = QCheckBox("Fast-food")
        self.filter4 = QCheckBox("Location de voitures")
        self.filter5 = QCheckBox("Station-service")
        self.filter6 = QCheckBox("Parking")
        self.filter7 = QCheckBox("Hotel")
        self.filter8 = QCheckBox("Randonnées")
        self.filter9 = QCheckBox("Loisirs")
        self.filter10 = QCheckBox("Transport en commun")
        self.filter11 = QCheckBox("Epiceries")
        self.filter12 = QCheckBox("park")

        submit_button = QPushButton("Valider")
        submit_button.clicked.connect(self.buttonClicked)
        submit_button.setFixedHeight(50)
        submit_button.setFixedWidth(150)

        # Création des layouts
        search_layout = QHBoxLayout()
        search_layout.addWidget(self.search_label)
        search_layout.addWidget(self.search_box)

        self.sousVert1 = QVBoxLayout()
        self.sousVert1 = QVBoxLayout()
        self.sousVert1 = QVBoxLayout()

        self.button_layout = QHBoxLayout()
        self.button_layout.addStretch()
        self.button_layout.addWidget(submit_button)
        self.button_layout.addStretch()

        main_layout = QVBoxLayout()
        main_layout.addLayout(search_layout)
        main_layout.addWidget(self.filter1)
        main_layout.addWidget(self.filter2)
        main_layout.addWidget(self.filter3)
        main_layout.addWidget(self.filter4)
        main_layout.addWidget(self.filter5)
        main_layout.addWidget(self.filter6)
        main_layout.addWidget(self.filter7)
        main_layout.addWidget(self.filter8)
        main_layout.addWidget(self.filter9)
        main_layout.addWidget(self.filter10)
        main_layout.addWidget(self.filter11)
        main_layout.addWidget(self.filter12)

        main_layout.addLayout(self.button_layout)
        main_layout.setContentsMargins(20, 100, 20, 50)

        self.setStyleSheet("""                   
                QCheckBox {
                        font-size : 15px;
                   }
                           """)

        # Configuration du widget principal
        widget.setLayout(main_layout)
        self.setCentralWidget(widget)

    # Récupération des filtres et de la ville quand on clique sur le bouton de validation
    def buttonClicked(self):
        if self.ville is None and (self.search_box.text() != ""):
            self.ville = self.search_box.text().title()
        if self.filter1.isChecked():
            if 'amenity' in self.filtre:
                self.filtre['amenity'].append('bar')
            else:
                self.filtre['amenity'] = ['bar']
        if self.filter2.isChecked():
            if 'amenity' in self.filtre:
                self.filtre['amenity'].append('restaurant')
            else:
                self.filtre['amenity'] = ['restaurant']
        if self.filter3.isChecked():
            if 'amenity' in self.filtre:
                self.filtre['amenity'].append('fast_food')
            else:
                self.filtre['amenity'] = ['fast_food']
        if self.filter4.isChecked():
            if 'amenity' in self.filtre:
                self.filtre['amenity'].append('car_rental')
            else:
                self.filtre['amenity'] = ['car_rental']
        if self.filter5.isChecked():
            if 'amenity' in self.filtre:
                self.filtre['amenity'].append('fuel')
            else:
                self.filtre['amenity'] = ['fuel']
        if self.filter6.isChecked():
            if 'amenity' in self.filtre:
                self.filtre['amenity'].append('parking')
            else:
                self.filtre['amenity'] = ['parking']
        if self.filter7.isChecked():
            if 'tourism' in self.filtre:
                self.filtre['tourism'].append('hotel')
            else:
                self.filtre['tourism'] = ['hotel']

        if self.filter8.isChecked():
            if 'highway' in self.filtre:
                self.filtre['highway'].append('smoothness')
            else:
                self.filtre['highway'] = ['smoothness']

        if self.filter9.isChecked():
            if 'leisure' in self.filtre:
                for i in ['adult_gaming_centre', 'amusement_arcade', 'beach_resort', 'bowling_alley',
                          'disc_golf_course', 'escape_game', 'fitness_centre', 'garden', '	golf_course', 'ice_rink',
                          'miniature_golf', 'sauna', 'swimming_pool', 'trampoline_park', 'water_park']:
                    self.filtre['leisure'].append(i)
            else:
                self.filtre['leisure'] = ['adult_gaming_centre', 'amusement_arcade', 'beach_resort', 'bowling_alley',
                                          'disc_golf_course', 'escape_game', 'fitness_centre', 'garden',
                                          '	golf_course', 'ice_rink', 'miniature_golf', 'sauna', 'swimming_pool',
                                          'trampoline_park', 'water_park']
        if self.filter10.isChecked():
            if 'public_transport' in self.filtre:
                for i in ['platform']:
                    self.filtre['public_transport'].append(i)
            else:
                self.filtre['public_transport'] = ['platform']
        if self.filter11.isChecked():
            if 'shop' in self.filtre:
                for i in ['alcohol', 'bakery', 'beverages', 'brewing_supplies', 'butcher', 'cheese', 'chocolate',
                          'coffee', 'confectionery', 'convenience', 'deli', 'dairy', 'farm', 'frozen_food',
                          'greengrocer', 'health_food', 'ice_cream', 'pasta', 'pastry', 'seafood', 'spices', 'tea',
                          'wine', 'water', 'supermarket']:
                    self.filtre['shop'].append(i)
            else:
                self.filtre['shop'] = ['alcohol', 'bakery', 'beverages', 'brewing_supplies', 'butcher', 'cheese',
                                       'chocolate', 'coffee', 'confectionery', 'convenience', 'deli', 'dairy', 'farm',
                                       'frozen_food', 'greengrocer', 'health_food', 'ice_cream', 'pasta', 'pastry',
                                       'seafood', 'spices', 'tea', 'wine', 'water', 'supermarket']

        if self.filter12.isChecked():
            if 'leisure' in self.filtre:
                self.filtre['leisure'].append('park')
            else:
                self.filtre['leisure'] = ['park']

        if (self.ville is not None):
            html, legende = carte_ville(self.ville, self.filtre)
            change_page(html, self.ville, "map", legende)
        else:
            if self.ville is None:
                self.filtre = {}
                print("Choisir ville")


# Fenêtre principale de l'application
class MainWindow(QMainWindow):
    def __init__(self, html, ville, legende):
        super().__init__()

        self.html = html
        self.ville = ville
        self.legende = legende

        # Setup de l'icône et du nom de l'application
        self.setWindowTitle("Travel App")
        self.setWindowIcon(QIcon("png/voyage.png"))

        self.initUI(html)

    def initUI(self, html):
        self.setFixedSize(405, 900)

        # Convertion de la carte en HTML et injection dans le widget QWebEngineView
        self.browser = QWebEngineView()
        self.setCentralWidget(self.browser)
        self.channel = QWebChannel()
        self.browser.page().setWebChannel(self.channel)
        self.channel.registerObject("MainWindow", self)
        self.browser.setHtml(html, QUrl("http://localhost/"))

        # Création d'un bouton
        button = QPushButton("Filtres", self)
        button.setGeometry(48.75, 800, 70, 70)
        button.setStyleSheet("""
                   QPushButton {
                        border-radius : 15px;
                        background-color : white;
                        box-shadow: 0px 2px 10px rgba(0, 0, 0, 0.5);
                   }
                   QPushButton:hover{
                        background-color : #F4F4F4;
                   }
               """)
        button.clicked.connect(self.buttonClicked)

        button1 = QPushButton("Infos", self)
        button1.setGeometry(286.25, 800, 70, 70)  # Définir les dimensions et la position du bouton
        button1.setStyleSheet("""
                   QPushButton {
                        border-radius : 15px;
                        background-color : white;
                        box-shadow: 0px 2px 10px rgba(0, 0, 0, 0.5);
                   }
                   QPushButton:hover{
                        background-color : #F4F4F4;
                   }
               """)
        button1.clicked.connect(self.buttonClicked1)

        button2 = QPushButton("Météo", self)
        button2.setGeometry(167.5, 800, 70, 70)  # Définir les dimensions et la position du bouton
        button2.setStyleSheet("""
                   QPushButton {
                        border-radius : 15px;
                        background-color : white;
                        box-shadow: 0px 2px 10px rgba(0, 0, 0, 0.5);
                   }
                   QPushButton:hover{
                        background-color : #F4F4F4;
                   }
               """)
        button2.clicked.connect(self.buttonClicked2)

        # Création de la légende
        if self.legende != {}:
            wid = QWidget(self)
            vertical = QVBoxLayout(self)
            for l in self.legende.keys():
                label = QLabel(
                    f"<span style='background-color: {self.legende[l]}; color : {self.legende[l]};'>aaa</span><span style='color: black;'> {l}</span>",
                    self)
                vertical.addWidget(label)
            wid.setLayout(vertical)
            wid.setStyleSheet("background-color : white;border-radius : 10px")
            nombrel = len(self.legende)

            # format de la légende en fonction des filtres choisis
            if 'location de voiture' in self.legende.keys() or 'transport en commun' in self.legende.keys() or 'station service' in self.legende.keys():
                if nombrel == 1:
                    wid.setGeometry(250, 10, 150, 40)
                else:
                    wid.setGeometry(250, 10, 150, nombrel * 30)
            else:
                if nombrel == 1:
                    wid.setGeometry(300, 10, 100, 40)
                else:
                    wid.setGeometry(300, 10, 100, nombrel * 30)

    # passage à la page home
    def buttonClicked(self):
        change_page(self.html, self.ville, "filtre", self.legende)

    # passage à la page infos
    def buttonClicked1(self):
        change_page(self.html, self.ville, "info", self.legende)

    # passage à la page météo
    def buttonClicked2(self):
        change_page(self.html, self.ville, "meteo", self.legende)


# Fenêtre d'information de l'application
class InfoWindow(QMainWindow):
    def __init__(self, html, ville, legende):
        super().__init__()

        self.html = html
        self.ville = ville
        self.legende = legende

        # Setup de l'icône et du nom de l'application
        self.setWindowTitle("Travel App")
        self.setWindowIcon(QIcon("png/voyage.png"))

        self.initUI(html, ville)

    def initUI(self, html, ville):
        self.setFixedSize(405, 900)

        # on récupère les infos sur la ville
        texte = infoVille(ville)

        button = QPushButton("Retour", self)
        button.clicked.connect(self.buttonClicked)
        button.setGeometry(10, 10, 100, 30)

        self.titre = QTextEdit(self)
        self.titre.setGeometry(10, 50, 385, 30)  # Position et taille du widget
        self.titre.setPlainText(ville)
        self.titre.setReadOnly(True)
        self.titre.setAlignment(Qt.AlignCenter)

        self.text_edit = QTextEdit(self)
        self.text_edit.setGeometry(10, 85, 385, 600)  # Position et taille du widget
        self.text_edit.setPlainText(texte)
        self.text_edit.setReadOnly(True)

    def buttonClicked(self):
        change_page(self.html, self.ville, "map", self.legende)


# Fenêtre météo de l'application
class MeteoWindow(QMainWindow):
    def __init__(self, html, ville, texte=None, jour=None, legende=None):
        super().__init__()

        self.html = html
        self.ville = ville
        self.texte = texte
        self.jour = jour
        self.legende = legende

        # Setup de l'icône et du nom de l'application
        self.setWindowTitle("Travel App")
        self.setWindowIcon(QIcon("png/voyage.png"))

        # passage à la page principale de la météo
        if jour is None:
            self.initUI()
        # passage à la page des vêtements de la météo
        else:
            self.initUIJour()

    def initUI(self):
        global window
        self.setFixedSize(405, 900)

        mainWidget = QWidget()

        if self.texte is None:
            self.texte = afficheMeteo(self.ville)

        button = QPushButton("Retour", self)
        button.clicked.connect(self.buttonClicked)
        button.setGeometry(10, 15, 70, 30)

        titre = QLabel(self.ville, self)
        titre.setStyleSheet("Font-size : 25px; font-weight: bold;")
        titre.setGeometry(0, 50, self.width(), 50)
        titre.setAlignment(Qt.AlignCenter)

        verticalLayout = QVBoxLayout(self)

        self.jours = []
        self.clothes = []

        for jour in self.texte.items():
            grandBloc = QVBoxLayout(self)
            label = QLabel(jour[0], self)
            label.setStyleSheet("Font-size : 20px; border-bottom-style: 2 px solid;")

            self.jours.append(jour)
            button_clothe = QPushButton("Conseils vestimentaires", self)

            horizontalBloc = QHBoxLayout(self)
            horizontalBloc.addWidget(label)
            self.clothes.append(button_clothe)
            horizontalBloc.addWidget(button_clothe)

            petitBloc1 = QVBoxLayout(self)
            horizontalBloc1 = QHBoxLayout(self)
            for i in jour[1]:
                label1 = QLabel(str(i[0]), self)
                label1.setAlignment(Qt.AlignCenter)
                horizontalBloc1.addWidget(label1)

            petitBloc1.addLayout(horizontalBloc1)

            petitBloc2 = QVBoxLayout(self)
            horizontalBloc2 = QHBoxLayout(self)
            for i in jour[1]:
                # Récupérer l'icône météorologique
                icon_url = f"http://openweathermap.org/img/w/{i[3]}.png"
                icon_data = requests.get(icon_url).content
                icon_pixmap = QPixmap()
                icon_pixmap.loadFromData(icon_data)

                label_icone = QLabel(self)
                label_icone.setPixmap(icon_pixmap.scaled(40, 40, Qt.KeepAspectRatio, Qt.SmoothTransformation))
                label_icone.setAlignment(Qt.AlignCenter)

                horizontalBloc2.addWidget(label_icone)

            petitBloc2.addLayout(horizontalBloc2)

            petitBloc3 = QVBoxLayout(self)
            horizontalBloc3 = QHBoxLayout(self)
            for i in jour[1]:
                label2 = QLabel(str(i[2]) + "°C", self)
                label2.setAlignment(Qt.AlignCenter)
                horizontalBloc3.addWidget(label2)
            petitBloc3.addLayout(horizontalBloc3)

            grandBloc.addLayout(horizontalBloc)
            grandBloc.addLayout(petitBloc1)
            grandBloc.addLayout(petitBloc2)
            grandBloc.addLayout(petitBloc3)

            grandBloc.setContentsMargins(0, 0, 0, 40)
            verticalLayout.addLayout(grandBloc)
            verticalLayout.setContentsMargins(5, 5, 5, 5)

        self.clothes[0].clicked.connect(self.pageClothes1)
        self.clothes[1].clicked.connect(self.pageClothes2)
        self.clothes[2].clicked.connect(self.pageClothes3)
        self.clothes[3].clicked.connect(self.pageClothes4)
        self.clothes[4].clicked.connect(self.pageClothes5)
        self.clothes[5].clicked.connect(self.pageClothes6)

        mainWidget.setLayout(verticalLayout)

        # Création d'un QScrollArea pour envelopper le mainWidget
        scrollArea = QScrollArea(self)
        scrollArea.setWidgetResizable(True)
        scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scrollArea.setWidget(mainWidget)
        scrollArea.setGeometry(-2, 110, self.width() + 4, self.height() - 110)

    def initUIJour(self):
        global window
        self.setFixedSize(405, 900)

        mainWidget = QWidget()

        # récupération des infos principales nécessaire pour le choix des vêtements
        maxTemps = -10000
        pluie = False
        soleil = False
        for tuple in self.jour[1]:
            if tuple[2] >= maxTemps:
                maxTemps = tuple[2]
            if 'rain' in tuple[1]:
                pluie = True
            if 'clear sky' in tuple[1]:
                soleil = True;

        # choix des vêtements et accessoires en fonction de la température, du soleil et de la pluie
        if maxTemps < 0:
            listeClothes = [("png/thermal under-shirt.png", "Sous-pull thermolactile"),
                            ("png/knit sweatshirt.png", "Sweat chaud"), ("winter overcoat.png", "Manteau d'hiver"),
                            ("png/fleece -lined pants.png", "Pantalon d'hiver")]
            accesoires = [("png/hat-scarf.png", 'bonnet'), ('png/gants.png', 'Gants')]
        if maxTemps >= 0 and maxTemps < 8:
            listeClothes = [('png/t-shirt.png', "T-shirt"), ('png/sweat.png', 'Sweat'), ('png/overcoat.png', 'Manteau'),
                            ('png/jeans.png', 'Jeans')]
            accesoires = [('png/baskets.png', 'Baskets')]
        if maxTemps >= 8 and maxTemps < 17:
            listeClothes = [("png/sous-pull.png", "Petit-pull"), ("png/overcoat.png", "Manteau"),
                            ("png/jeans.png", "Jeans")]
            accesoires = [("png/baskets.png", "Baskets")]
        if maxTemps >= 17 and maxTemps < 20:
            listeClothes = [('png/t-shirt.png', 'T-shirt'), ('png/sweatshirt.png', 'Sweatshirt'),
                            ('png/jeans.png', 'Jeans')]
            accesoires = [('png/baskets.png', 'Baskets')]
        if maxTemps >= 20 and maxTemps < 23:
            listeClothes = [('png/t-shirt.png', 'T-shirt'), ('png/jeans.png', 'Jeans')]
            accesoires = [('png/baskets.png', 'Baskets')]
        if maxTemps >= 23 and maxTemps < 28:
            listeClothes = [('png/t-shirt.png', 'T-shirt'), ('png/pantalon toile.png', 'Pantalon léger')]
            accesoires = [('png/baskets.png', 'Baskets')]
        if maxTemps >= 28:
            listeClothes = [('png/débardeur.png', 'Débardeur'), ('png/short.png', 'Short')]
            accesoires = [('png/baskets.png', 'Baskets')]

        if pluie:
            accesoires.append(('png/umbrella.png', 'Parapluie'))

        if soleil:
            accesoires.append(('png/lunettes de soleil.png', 'Lunettes de soleil'))


        # Création des widgets
        button = QPushButton("Retour", self)
        button.clicked.connect(self.retourMeteo)
        button.setGeometry(10, 15, 70, 30)

        titre = QLabel(self.jour[0], self)
        titre.setStyleSheet("Font-size : 25px; font-weight: bold;")
        titre.setGeometry(0, 50, self.width(), 50)
        titre.setAlignment(Qt.AlignCenter)

        vertical = QVBoxLayout(self)

        vertical1 = QVBoxLayout(self)
        vertical1_1 = QVBoxLayout(self)
        horizontal1_1 = QHBoxLayout(self)
        label = QLabel("What to wear", self)
        label.setStyleSheet("Font-size : 25px;")
        horizontal1_1.addWidget(label)
        horizontal1_1.setContentsMargins(0, 0, 0, 20)
        vertical1_2 = QVBoxLayout(self)
        horizontal1_2 = QHBoxLayout(self)
        vertical1_3 = QVBoxLayout(self)
        horizontal1_3 = QHBoxLayout(self)

        vertical1_1.addLayout(horizontal1_1)
        vertical1_2.addLayout(horizontal1_2)
        vertical1_3.addLayout(horizontal1_3)
        vertical1.addLayout(vertical1_1)
        vertical1.addLayout(vertical1_2)
        vertical1.addLayout(vertical1_3)

        # ajout des vêtements et accessoires à la page
        for clothe in listeClothes:
            nom = QLabel(clothe[1], self)
            nom.setStyleSheet("font-weight: bold;")
            pixmap = QPixmap(clothe[0])
            pixmap_resized = pixmap.scaled(50, 50, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            image = QLabel()
            image.setPixmap(pixmap_resized)

            image.setAlignment(Qt.AlignCenter)
            nom.setAlignment(Qt.AlignCenter)

            horizontal1_2.addWidget(image)
            horizontal1_3.addWidget(nom)
        vertical.addLayout(vertical1)

        if accesoires != []:
            vertical2 = QVBoxLayout(self)
            vertical2_1 = QVBoxLayout(self)
            horizontal2_1 = QHBoxLayout(self)
            label = QLabel("Other", self)
            label.setStyleSheet("Font-size : 25px;")
            horizontal2_1.addWidget(label)
            vertical2_2 = QVBoxLayout(self)
            horizontal2_2 = QHBoxLayout(self)
            vertical2_3 = QVBoxLayout(self)
            horizontal2_3 = QHBoxLayout(self)

            vertical2_1.addLayout(horizontal2_1)
            vertical2_2.addLayout(horizontal2_2)
            vertical2_3.addLayout(horizontal2_3)
            vertical2.addLayout(vertical2_1)
            vertical2.addLayout(vertical2_2)
            vertical2.addLayout(vertical2_3)
            vertical.addLayout(vertical2)

            for acc in accesoires:
                nom = QLabel(acc[1], self)
                nom.setStyleSheet("font-weight: bold;")
                pixmap = QPixmap(acc[0])
                pixmap_resized = pixmap.scaled(50, 50, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                image = QLabel()
                image.setPixmap(pixmap_resized)

                image.setAlignment(Qt.AlignCenter)
                nom.setAlignment(Qt.AlignCenter)

                horizontal2_2.addWidget(image)
                horizontal2_3.addWidget(nom)

        mainWidget.setLayout(vertical)

        vertical1.setContentsMargins(0, 0, 0, 40)

        # Création d'un QScrollArea pour envelopper le mainWidget
        scrollArea = QScrollArea(self)
        scrollArea.setWidgetResizable(True)
        scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scrollArea.setWidget(mainWidget)
        scrollArea.setGeometry(-2, 110, self.width() + 4, 350)

    # passage à la page de la carte
    def buttonClicked(self):
        change_page(self.html, self.ville, "map", legende=self.legende)


    # passage au page des vêtements
    def pageClothes1(self):
        global window
        window.close()
        window = MeteoWindow(self.html, self.ville, self.texte, self.jours[0], legende=self.legende)
        window.show()

    def pageClothes2(self):
        global window
        window.close()
        window = MeteoWindow(self.html, self.ville, self.texte, self.jours[1], legende=self.legende)
        window.show()

    def pageClothes3(self):
        global window
        window.close()
        window = MeteoWindow(self.html, self.ville, self.texte, self.jours[2], legende=self.legende)
        window.show()

    def pageClothes4(self):
        global window
        window.close()
        window = MeteoWindow(self.html, self.ville, self.texte, self.jours[3], legende=self.legende)
        window.show()

    def pageClothes5(self):
        global window
        window.close()
        window = MeteoWindow(self.html, self.ville, self.texte, self.jours[4], legende=self.legende)
        window.show()

    def pageClothes6(self):
        global window
        window.close()
        window = MeteoWindow(self.html, self.ville, self.texte, self.jours[5], legende=self.legende)
        window.show()

    def retourMeteo(self):
        global window
        window.close()
        window = MeteoWindow(self.html, self.ville, self.texte, jour=None, legende=self.legende)
        window.show()


# fonction qui permet de changer de page
def change_page(html, ville, texte, legende=None):
    global window
    window.close()
    if texte == "filtre":
        window = HomeWindow()
    if texte == "map":
        window = MainWindow(html, ville, legende=legende)
    if texte == "info":
        window = InfoWindow(html, ville, legende=legende)
    if texte == 'meteo':
        window = MeteoWindow(html, ville, legende=legende)
    window.show()


# Récupération des infos dans l'API OpenWeather afin de pouvoir faire la page de la météo
def afficheMeteo(ville):
    API_key = '9e2945533ae5bdedb1d7bdbad8b3c44f'
    unite = "metric"
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={ville}&units={unite}&appid={API_key}"
    response = requests.get(url)
    data = json.loads(response.text)

    texte = {}

    # récupération des prévisions météo
    jour_actuel = ""
    for prevision in data["list"]:
        date_heure = datetime.datetime.fromtimestamp(int(prevision["dt"])).strftime('%Y-%m-%d %H:%M:%S')
        jour = date_heure.split(" ")[0]
        heure = date_heure.split(" ")[1]
        temperature = int(prevision["main"]["temp"])
        conditions = prevision["weather"][0]["description"]
        icon = prevision["weather"][0]["icon"]

        if jour != jour_actuel:
            jour_actuel = jour
            date = datetime.datetime.strptime(jour, "%Y-%m-%d").strftime("%A %d %B")
            texte[date] = []
        texte[date].append((heure[0:2], conditions, temperature, icon))

    return texte


# Récupération des infos dans l'API de Wikipédia pour faire la page d'informations
def infoVille(ville):
    url = f'https://fr.wikipedia.org/w/api.php?action=query&format=json&prop=extracts&titles={ville}&exsentences=5&explaintext=1'
    response = requests.get(url)
    data = json.loads(response.text)
    page = data['query']['pages']
    extract = page[list(page.keys())[0]]['extract']
    return extract


# Ajout des marqueurs sur la map en fonction des filtres choisis
def pointsInteret(ville, lieu, points, m, color, key):
    if key == 'highway':
        # Demande à l'utilisateur de saisir le nom de la ville
        city_name = 'Annecy'

        # Récupération des coordonnées géographiques de la ville à partir de l'API nominatim
        geocode_url = "https://nominatim.openstreetmap.org/search"
        geocode_params = {"q": city_name, "format": "json"}
        response = requests.get(geocode_url, params=geocode_params)
        result = response.json()[0]
        lat, lon = result["lat"], result["lon"]

        # Définition de la position de départ et du niveau de zoom pour la carte centrée sur la ville
        start_coords = (float(lat), float(lon))

        # Récupération des données de randonnées depuis l'API OpenStreetMap pour la zone autour de la ville
        overpass_url = "http://overpass-api.de/api/interpreter"
        overpass_query = f"""
        [out:json];
        // Récupération de tous les chemins de randonnée
        way[highway=path][foot=yes](around:5000,{lat},{lon});

        // Récupération de tous les relations de randonnée
        relation[route=hiking](around:5000,{lat},{lon});

        // Affichage des chemins de randonnée
        (
            ._;
            >;
        );

        out;"""

        response = requests.get(overpass_url, params={'data': overpass_query})
        data = response.json()

        # Affichage des chemins de randonnée
        for way in data['elements']:
            if way['type'] == 'way':
                coords = []
                for node_id in way['nodes']:
                    for node in data['elements']:
                        if node['type'] == 'node' and node['id'] == node_id:
                            lat_node, lon_node = float(node['lat']), float(node['lon'])
                            lat_rad, lon_rad = math.radians(lat_node), math.radians(lon_node)
                            distance = 6371.0 * math.acos(math.sin(math.radians(start_coords[0])) * math.sin(lat_rad) +
                                                          math.cos(math.radians(start_coords[0])) * math.cos(lat_rad) *
                                                          math.cos(math.radians(lon_node - start_coords[1])))
                            if distance < 20:
                                coords.append((lat_node, lon_node))
                if coords != []:
                    folium.PolyLine(coords, color='darkgreen', weight=3, opacity=0.7).add_to(m)

    else:
        # Recherchez tous les lieux dans la ville avec l'API Overpass
        overpass_url = "http://overpass-api.de/api/interpreter"
        overpass_query = f"""
            [out:json];
            area[name="{ville}"]->.boundaryarea;
            node["{key}"="{lieu}"](area.boundaryarea);
            out center;
        """

        if lieu == 'hotel' or key == 'shop':
            overpass_url = "http://overpass-api.de/api/interpreter"
            overpass_query = f"""
                [out:json];
                area[name="{ville}"]->.boundaryarea;
                node["{key}"="{lieu}"](area.boundaryarea);
                way["{key}"="{lieu}"](area.boundaryarea);
                relation["{key}"="{lieu}"](area.boundaryarea);
                out center;
            """

        response = requests.get(overpass_url, params={"data": overpass_query})
        lieux = response.json()["elements"]

        # Parcourez tous les restaurants et ajoutez un marqueur pour chacun sur la carte
        for l in lieux:
            if lieu == "hotel" or key == 'shop':
                lat, lon = l['center']['lat'], l['center']['lon']
            else:
                lat, lon = l['lat'], l['lon']
            polygone = Polygon(points)
            point_to_check = Point(lat, lon)
            if polygone.contains(point_to_check) and "name" in l["tags"]:
                name = l["tags"]["name"]
                infos = [
                    ("opening_hours", bool("opening_hours" in l["tags"])),
                    ("phone", bool("phone" in l["tags"])),
                    ("website", bool("website" in l["tags"]))
                ]

                # Créer une chaîne de caractères contenant le texte à afficher
                popup_text = f'<b>{name}</b><br>'
                for info in infos:
                    if info[1]:
                        popup_text += f'{info[0]} : {l["tags"][f"{info[0]}"]}<br>'

                marker = folium.Marker(location=[lat, lon], tooltip=name, icon=folium.Icon(color=(color)),
                                       popup=folium.Popup(popup_text, max_width=300))
                marker.add_to(m)


# Création de la map en fonction de la ville et des filtres choisis
def carte_ville(ville, lieux):
    city_name = ville
    url = f'https://nominatim.openstreetmap.org/search?q={city_name}&format=json&limit=1&polygon_geojson=1'
    response = requests.get(url).json()
    latitude, longitude = float(response[0]['lat']), float(response[0]['lon'])
    points = []
    for liste in response[0]['geojson']['coordinates'][0]:
        points.append((liste[1], liste[0]))
    m = folium.Map(location=[latitude, longitude], zoom_start=12)
    folium.Polygon(locations=points, color='blue', fill=True, fill_color='blue', fill_opacity=0.1).add_to(m)

    legende = {}
    # choix des couleurs des filtres
    for key in lieux.keys():
        for filtre in lieux[key]:
            if filtre == 'bar':
                color = 'red'
                legende['bar'] = 'rgb(214, 62, 42)'
            if filtre == 'restaurant':
                color = 'blue'
                legende['restaurant'] = 'rgb(56, 170, 221)'
            if filtre == 'fast_food':
                color = 'lightred'
                legende['fast-food'] = 'rgb(255, 142, 127)'
            if filtre == 'car_rental':
                color = 'orange'
                legende['location de voiture'] = 'rgb(245, 150, 48)'
            if filtre == 'fuel':
                color = 'black'
                legende['station service'] = 'rgb(48, 48, 48)'
            if filtre == 'parking':
                color = 'gray'
                legende['parking'] = 'rgb(86, 86, 86)'
            if filtre == 'hotel':
                color = 'white'
                legende['hotel'] = 'rgb(251, 251, 251)'
            if filtre == 'smoothness':
                color = 'darkgreen'
                legende['randonnées'] = 'rgb(9, 105, 9)'
            if key == 'leisure' and filtre != 'park':
                color = 'pink'
                legende['loisirs'] = 'rgb(255, 145, 234)'
            if key == 'public_transport':
                color = 'purple'
                legende['transport publique'] = 'rgb(209, 82, 184)'
            if key == 'shop':
                color = 'beige'
                legende['épicerie'] = 'rgb(255, 203, 146)'
            if filtre == 'park':
                color = 'green'
                legende['parc'] = 'rgb(114, 176, 38)'
            pointsInteret(ville, filtre, points, m, color, key)

    html = m.get_root().render()

    return html, legende


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = HomeWindow()
    window.show()
    sys.exit(app.exec())
