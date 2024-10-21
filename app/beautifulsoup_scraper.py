import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

# URLs à scraper
urls = {
    "Appartements à louer": "https://dakarvente.com/annonces-categorie-appartements-louer-10.html",
    "Appartements à vendre": "https://dakarvente.com/annonces-categorie-appartements-vendre-61.html",
    "Terrains à vendre": "https://dakarvente.com/annonces-categorie-terrains-vendre-13.html"
}

# Fonction pour scraper une page donnée
def scrape_page(url, page_num):
    full_url = f"{url}&sort=&nb={page_num}"
    page = requests.get(full_url)
    soup = BeautifulSoup(page.content, "html.parser")
    
    # Conteneur pour stocker les données de la page
    data = []

    # Trouver les annonces sur la page
    annonces = soup.find_all("div", class_="item-product-grid-3")

    for annonce in annonces:
        try:
            details = annonce.find("div", class_="content-desc").text.strip()
            prix = annonce.find("div", class_="content-price").text.strip()
            adresse = annonce.find_all("div", class_="content-price")[1].text.strip()
            image_lien = annonce.find("img")["src"]
            
            data.append({
                "Détails": details,
                "Prix": prix,
                "Adresse": adresse,
                "Image Lien": image_lien
            })
        except Exception as e:
            print(f"Erreur lors du scraping d'une annonce : {e}")
    
    return data

# Fonction pour scraper plusieurs pages avec pagination
def scrape_all_pages(base_url, max_pages=50):
    all_data = []
    for page_num in range(1, max_pages + 1):
        print(f"Scraping page {page_num} de {base_url}")
        page_data = scrape_page(base_url, page_num)
        if not page_data:
            print(f"Aucune donnée trouvée à la page {page_num}, arrêt du scraping.")
            break
        all_data.extend(page_data)
        time.sleep(2)  # Pause entre chaque requête pour éviter de surcharger le serveur

    return pd.DataFrame(all_data)

# Scraping et nettoyage pour chaque URL avec pagination
all_scraped_data = pd.DataFrame()

for category, url in urls.items():
    print(f"Scraping des données pour {category}...")
    category_data = scrape_all_pages(url, max_pages=50)
    all_scraped_data = pd.concat([all_scraped_data, category_data], ignore_index=True)

# Sauvegarder les données nettoyées dans un fichier CSV
all_scraped_data.to_csv("app/data/dakarvente_cleaned_data.csv", index=False)
print("Scraping terminé et données sauvegardées.")
