# DIT DEVOPS PROJECT : Dakar Vente Scraper

Cette application **Streamlit** permet de télécharger des données extraites de **Dakar Vente** sur les "appartements à louer", "appartements à vendre" et "terrains à vendre".

## Fonctionnalités

- **Bibliothèques Python** : pandas, streamlit, selenium, logging
- **Source de données** : [Dakar Vente](https://dakarvente.com/)
- **Options** :
  - Scraping des données avec Selenium
  - Téléchargement des données extraites
  - Chargement des données précédemment scrappées par **Web Scraper**
  - Formulaire d'évaluation simple intégré

## Prérequis

- [Python](https://www.python.org/)
- [Docker](https://www.docker.com/) (facultatif)
- [Web Scraper](https://webscraper.io/) (extension Chrome)

## Installation

### LOCAL

Clonez ce dépôt :
   ```sh
   git clone https://github.com/aminacherif/data_collection_dit_devoir.git
   cd dit-devops-project
pip install -r requirements.txt
streamlit run app/data_app.py
http://localhost:8501
