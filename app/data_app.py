import streamlit as st
import pandas as pd
import logging
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

# Configurer les logs pour qu'ils s'affichent dans la console avec Streamlit
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

# Titre de l'application
st.markdown("<h1 style='text-align: center;'>Scraper de données : Dakar Vente</h1>", unsafe_allow_html=True)

# Fonction pour charger les fichiers CSV
def load_scraper_csv(file_path):
    if os.path.exists(file_path):
        df = pd.read_csv(file_path)
        st.subheader(f"Aperçu des données du fichier : {file_path}")
        st.write("Ces données ont été scrappées à l'aide de Selenium.")
        st.write(f"Dimension des données : {df.shape[0]} lignes et {df.shape[1]} colonnes.")
        st.dataframe(df)
        
        # Bouton pour télécharger le fichier CSV
        csv_data = df.to_csv(index=False)
        st.download_button(label="Télécharger les données en CSV", data=csv_data, file_name=file_path.split("/")[-1], mime="text/csv")
    else:
        st.warning(f"Le fichier {file_path} n'existe pas encore. Effectuez le scraping pour générer le fichier.")

# Fonction pour initialiser Selenium
def init_selenium():
    # Configuration de ChromeDriver
    chrome_service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Exécuter en mode sans interface
    driver = webdriver.Chrome(service=chrome_service, options=options)
    return driver

# Fonction pour scraper plusieurs pages avec Selenium
def scrape_data_with_selenium(base_url, max_pages, category_name, file_name):
    logging.info(f"Début du scraping des données pour {category_name}...")
    st.write(f"Scraping des données pour {category_name} sur {max_pages} pages...")
    data = []
    
    # Initialiser Selenium
    driver = init_selenium()

    for p in range(1, max_pages + 1):
        url = f"{base_url}&nb={p}"
        logging.info(f"Scraping de la page {p} à l'URL : {url}")
        st.write(f"Scraping de la page {p} à l'URL : {url}")
        driver.get(url)
        time.sleep(3)

        articles = driver.find_elements(By.CLASS_NAME, "item-product-grid-3")
        logging.info(f"{len(articles)} articles trouvés sur la page {p}")
        st.write(f"{len(articles)} articles trouvés sur la page {p}")

        for article in articles:
            try:
                detail = article.find_element(By.CLASS_NAME, "content-desc").text.strip()
                prix = article.find_element(By.CLASS_NAME, "content-price").text.strip()
                adresse = article.find_elements(By.CLASS_NAME, "content-price")[1].text.strip()
                lien_image = article.find_element(By.TAG_NAME, "img").get_attribute("src")

                data.append({
                    "Détails": detail,
                    "Prix": prix,
                    "Adresse": adresse,
                    "Lien de l'image": lien_image
                })
            except Exception as e:
                logging.error(f"Erreur lors de l'extraction : {e}")
                st.write(f"Erreur lors de l'extraction des informations : {e}")

    # Fermer Selenium
    driver.quit()

    # Convertir les données en DataFrame et sauvegarder le fichier CSV
    df = pd.DataFrame(data)
    file_path = f"app/data/{file_name}"
    df.to_csv(file_path, index=False)
    
    # Afficher et proposer le téléchargement
    st.subheader(f"Aperçu des données scrappées : {category_name}")
    st.write(f"Dimension des données : {df.shape[0]} lignes et {df.shape[1]} colonnes.")
    st.dataframe(df)

    csv_data = df.to_csv(index=False)
    st.download_button(label="Télécharger les données en CSV", data=csv_data, file_name=file_name, mime="text/csv")

# Interface utilisateur
col1, col2 = st.columns(2)

with col2:
    st.header("Page Indexes")
    page = st.selectbox("Sélectionner la page", options=["Sélectionner une page"] + [str(opt) for opt in range(1, 50)])

with col1:
    st.header("Options")
    option = st.selectbox("Choisir une option", ("Scraper les données", "Charger des données scrappées"))

# Scraper les données avec Selenium
if option == "Scraper les données" and page != "Sélectionner une page":
    tab1, tab2, tab3 = st.tabs(["Appartements à louer", "Appartements à vendre", "Terrains à vendre"])

    with tab1:
        scrape_data_with_selenium("https://dakarvente.com/index.php?page=annonces_categorie&id=10&sort=", int(page), "Appartements à louer", "dakarvente_appartements_louer_cleaned.csv")

    with tab2:
        scrape_data_with_selenium("https://dakarvente.com/index.php?page=annonces_categorie&id=61&sort=", int(page), "Appartements à vendre", "dakarvente_appartements_vendre_cleaned.csv")

    with tab3:
        scrape_data_with_selenium("https://dakarvente.com/index.php?page=annonces_categorie&id=13&sort=", int(page), "Terrains à vendre", "dakarvente_terrains_vendre_cleaned.csv")

# Charger des données déjà scrappées
if option == "Charger des données scrappées":
    file_choice = st.selectbox("Choisir un fichier à charger", ["Sélectionner un fichier", "Appartements à louer", "Appartements à vendre", "Terrains à vendre"])
    files = {
        "Appartements à louer": "app/data/dakarvente_appartements_louer_cleaned.csv",
        "Appartements à vendre": "app/data/dakarvente_appartements_vendre_cleaned.csv",
        "Terrains à vendre": "app/data/dakarvente_terrains_vendre_cleaned.csv"
    }

    if file_choice != "Sélectionner un fichier":
        load_scraper_csv(files[file_choice])
