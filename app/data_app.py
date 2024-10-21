import streamlit as st
import pandas as pd
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import os

# Configurer les logs pour qu'ils s'affichent dans la console avec Streamlit
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

# Titre de l'application
st.markdown("<h1 style='text-align: center;'>Scraper de données : Dakar Vente</h1>", unsafe_allow_html=True)

# Fonction pour charger les fichiers CSV exportés par Web Scraper
def load_scraper_csv(file_path):
    if os.path.exists(file_path):
        # Charger le CSV dans un DataFrame
        df = pd.read_csv(file_path)
        st.subheader(f"Aperçu des données du fichier : {file_path}")
        st.write("Ces données ont été scrapées à l'aide de **Web Scraper**.")
        st.write(f"Dimension des données : {df.shape[0]} lignes et {df.shape[1]} colonnes.")
        st.dataframe(df)
        
        # Bouton pour télécharger le fichier CSV
        csv_data = df.to_csv(index=False)
        st.download_button(label="Télécharger les données en CSV", data=csv_data, file_name=file_path.split("/")[-1], mime="text/csv")
    else:
        st.warning(f"Le fichier {file_path} n'existe pas. Assurez-vous que le scraping a été effectué et que le fichier est présent.")

# Fonction pour initialiser Selenium
def init_selenium():
    # Configuration de ChromeDriver
    chrome_service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Exécuter en mode sans interface
    driver = webdriver.Chrome(service=chrome_service, options=options)
    return driver

# Fonction de scraping avec Selenium
def load_bs_selenium(pageMax, title, key, category_id):
    st.markdown("<style>div.stButton {text-align:center}</style>", unsafe_allow_html=True)

    if st.button(title, key) or st.session_state.get("button_pressed", False):
        # Mettre à jour l'état du bouton dans session_state
        st.session_state["button_pressed"] = True

        logging.info(f"Début du scraping pour {title} avec la catégorie ID : {category_id}")
        st.write(f"Début du scraping pour {title} avec la catégorie ID : {category_id}")
        DF = pd.DataFrame()

        # Initialiser Selenium
        driver = init_selenium()

        # Conteneur pour les données scrappées
        data = []

        for p in range(2, pageMax):  
            logging.info(f"Dans la boucle de scraping, page {p}")
            st.write(f"Dans la boucle de scraping, page {p}")
            url = f"https://dakarvente.com/index.php?page=annonces_categorie&id={category_id}&sort=&nb={p}"
            logging.info(f"Scraping de la page {p} à l'URL : {url}")
            st.write(f"Scraping de la page {p} à l'URL : {url}")
            driver.get(url)
            time.sleep(3)  # Attendre que la page se charge complètement

            # Récupérer tous les articles
            articles = driver.find_elements(By.CLASS_NAME, "item-product-grid-3")
            logging.info(f"{len(articles)} articles trouvés sur la page {p}")
            st.write(f"{len(articles)} articles trouvés sur la page {p}")

            for article in articles:
                try:
                    # Récupérer les détails
                    detail = article.find_element(By.CLASS_NAME, "content-desc").text.strip()
                    prix = article.find_element(By.CLASS_NAME, "content-price").text.strip()
                    adresse = article.find_elements(By.CLASS_NAME, "content-price")[1].text.strip()
                    lien_image = article.find_element(By.TAG_NAME, "img").get_attribute("src")

                    logging.info(f"Détail : {detail}, Prix : {prix}, Adresse : {adresse}")
                    st.write(f"Détail : {detail}, Prix : {prix}, Adresse : {adresse}")

                    # Créer un dictionnaire pour stocker les informations
                    dico = {
                        "Détails": detail,
                        "Prix (FCA)": prix,
                        "Adresse": adresse,
                        "Lien de l'image": lien_image
                    }
                    data.append(dico)
                except Exception as e:
                    logging.error(f"Erreur lors de l'extraction des informations : {e}")
                    st.write(f"Erreur lors de l'extraction des informations : {e}")

        # Créer un DataFrame avec les données récupérées
        df = pd.DataFrame(data)
        DF = pd.concat([DF, df], axis=0).reset_index(drop=True)

        # Fermer Selenium
        driver.quit()

        # Affichage des données
        st.subheader('Aperçu des données')
        st.write(f'Dimension des données : {DF.shape[0]} lignes et {DF.shape[1]} colonnes.')
        st.dataframe(DF)

        # Bouton pour télécharger les données en CSV
        csv_data = DF.to_csv(index=False)
        st.download_button(label="Télécharger les données en CSV", data=csv_data, file_name="scraping_dakarvente.csv", mime="text/csv", key=f"{category_id}_download")

# Interface utilisateur
col1, col2 = st.columns(2)

with col2:
    st.header("Page Indexes")
    page = st.selectbox("Sélectionner la page", options=["Sélectionner une page"] + [str(opt) for opt in range(2, 50)])

with col1:
    st.header("Options")
    option = st.selectbox("Choisir une option", ("Scraper les données", "Charger des données scrappées par Web Scraper"))

# Scraper les données avec Selenium
if option == "Scraper les données" and page != "Sélectionner une page":  # Ne pas scraper si l'option par défaut est sélectionnée
    tab1, tab2, tab3 = st.tabs(["Appartements à louer", "Appartements à vendre", "Terrains à vendre"])

    with tab1:
        logging.info(f"Page sélectionnée : {page}")
        st.write(f"Page sélectionnée : {page}")
        load_bs_selenium(int(page), 'Charger Appartements à louer', '1', 10)

    with tab2:
        load_bs_selenium(int(page), 'Charger Appartements à vendre', '2', 61)

    with tab3:
        load_bs_selenium(int(page), 'Charger Terrains à vendre', '3', 13)

# Si l'utilisateur choisit "Charger des données scrappées par Web Scraper"
if option == "Charger des données scrappées par Web Scraper":
    # Ajouter une option pour charger les fichiers CSV existants
    file_choice = st.selectbox("Choisir un fichier à charger", ["Sélectionner un fichier", "Appartements à louer", "Appartements à vendre", "Terrains à vendre"])

    # Chemins des fichiers CSV (à ajuster en fonction de l'endroit où les fichiers CSV sont enregistrés)
    files = {
        "Appartements à louer": "data/dakarvente-logement-scraper.csv",
        "Appartements à vendre": "data/dakarvente-vente-scraper.csv",
        "Terrains à vendre": "data/dakarvente-terrains.csv"
    }

    # Charger le fichier sélectionné
    if file_choice != "Sélectionner un fichier":
        load_scraper_csv(files[file_choice])