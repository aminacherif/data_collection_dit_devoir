import streamlit as st
import pandas as pd
import os
import requests
from bs4 import BeautifulSoup

API_KEY = "eda30bb1a85eb4974c982d6cdd33ce04"

# Titre de l'application
st.markdown("<h1 style='text-align: center;'>Scraper de données : <br> Dakar Vente</h1>", unsafe_allow_html=True)

# Fonction pour charger les fichiers CSV
def load_scraper_csv(file_path):
    if os.path.exists(file_path):
        df = pd.read_csv(file_path)
        st.write(f"Dimension des données : {df.shape[0]} lignes et {df.shape[1]} colonnes.")
        st.dataframe(df)
        
        # Bouton pour télécharger le fichier CSV
        csv_data = df.to_csv(index=False)
        st.download_button(label="Télécharger les données en CSV", data=csv_data, file_name=file_path.split("/")[-1], mime="text/csv")
    else:
        st.warning(f"Le fichier {file_path} n'existe pas encore. Effectuez le scraping pour générer le fichier.")

# Fonction pour scraper des pages avec ScraperAPI
def scrape_data_with_scraperapi(base_url, max_pages, category_name, file_name):
    data = []

    for p in range(1, max_pages + 1):
        url = f"{base_url}&nb={p}"
        # Utilisation de ScraperAPI pour scraper la page avec un User-Agent
        response = requests.get(
            "http://api.scraperapi.com",
            params={
                "api_key": API_KEY,
                "url": url,
                "render": "true"
            },
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
                "Accept-Language": "fr-SN,fr;q=0.9,en;q=0.8",
                "Accept-Encoding": "gzip, deflate, br",
                "Connection": "keep-alive"
            }

        )

        # Afficher le contenu brut de la page pour diagnostic
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')

            # Extraire les articles à partir de la balise <article>
            articles = soup.find_all("article", class_="item-product-grid-3")
            if articles:
                for article in articles:
                    try:

                        # Extraire l'image
                        image_lien = article.find("img")["src"] if article.find("img") else 'N/A'

                        # Extraire la description
                        description = article.find("div", class_="content-desc").text.strip() if article.find("div", class_="content-desc") else 'N/A'

                        # Extraire le prix
                        prix = article.find("div", class_="content-price").text.strip() if article.find("div", class_="content-price") else 'N/A'

                        # Extraire l'adresse
                        adresse = article.find_all("div", class_="content-price")[1].text.strip() if len(article.find_all("div", class_="content-price")) > 1 else 'N/A'

                        data.append({
                            "Détails": description,
                            "Prix": prix,
                            "Adresse": adresse,
                            "Image": image_lien,
                        })
                    except Exception as e:
                        st.write(f"Erreur lors de l'extraction des informations : {e}")
            else:
                st.warning(f"Aucun article trouvé sur la page {p}.")
        else:
            st.error(f"Erreur lors de l'accès à la page {url} (Code {response.status_code})")

    # Convertir les données en DataFrame et sauvegarder le fichier CSV
    if data:
        df = pd.DataFrame(data)
        file_path = f"app/data/{file_name}"
        df.to_csv(file_path, index=False)
        
        # Afficher et proposer le téléchargement
        st.subheader(f"Aperçu des données scrappées : {category_name}")
        st.write(f"Dimension des données : {df.shape[0]} lignes et {df.shape[1]} colonnes.")
        st.dataframe(df)

        csv_data = df.to_csv(index=False)
        st.download_button(label="Télécharger les données en CSV", data=csv_data, file_name=file_name, mime="text/csv")
    else:
        st.warning("Aucune donnée n'a été extraite.")

# Interface utilisateur
col1, col2 = st.columns(2)

with col2:
    st.header("Page Indexes")
    page = st.selectbox("Sélectionner la page", options=["Sélectionner une page"] + [str(opt) for opt in range(1, 50)])

with col1:
    st.header("Options")
    option = st.selectbox("Choisir une option", ("Scraper les données", "Charger des données scrappées"))

# Scraper les données avec ScraperAPI
if option == "Scraper les données" and page != "Sélectionner une page":
    tab1, tab2, tab3 = st.tabs(["Appartements à louer", "Appartements à vendre", "Terrains à vendre"])

    with tab1:
        scrape_data_with_scraperapi("https://dakarvente.com/index.php?page=annonces_categorie&id=10&sort=", int(page), "Appartements à louer", "dakarvente_appartements_louer_cleaned.csv")

    with tab2:
        scrape_data_with_scraperapi("https://dakarvente.com/index.php?page=annonces_categorie&id=61&sort=", int(page), "Appartements à vendre", "dakarvente_appartements_vendre_cleaned.csv")

    with tab3:
        scrape_data_with_scraperapi("https://dakarvente.com/index.php?page=annonces_categorie&id=13&sort=", int(page), "Terrains à vendre", "dakarvente_terrains_vendre_cleaned.csv")

# Charger des données déjà scrappées
if option == "Charger des données scrappées":
    file_choice = st.selectbox("Choisir un fichier à charger", ["Sélectionner un fichier", "Appartements à louer", "Appartements à vendre", "Terrains à vendre"])
    files = {
        "Appartements à louer": "app/data/dakarvente-logement-scraper.csv",
        "Appartements à vendre": "app/data/dakarvente-vente-scraper.csv",
        "Terrains à vendre": "app/data/dakarvente-terrains-scraper.csv"
    }

    if file_choice != "Sélectionner un fichier":
        load_scraper_csv(files[file_choice])
