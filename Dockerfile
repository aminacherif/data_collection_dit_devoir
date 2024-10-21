# Utiliser une image de base Python
FROM python:3.8-slim

# Définir le répertoire de travail
WORKDIR /app

# Copier le fichier des dépendances et installer les dépendances
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copier le reste du code source
COPY . .

# Exposer le port sur lequel l'application va tourner
EXPOSE 8501

# Commande pour démarrer l'application
CMD ["streamlit", "run", "app/data_app.py"]