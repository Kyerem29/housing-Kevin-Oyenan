# Utiliser une image Python officielle
FROM python:3.10-slim

# Installer les dépendances système nécessaires pour psycopg2 et autres packages
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Définir le répertoire de travail à l'intérieur du conteneur
WORKDIR /app

# Copier le contenu du répertoire actuel dans le conteneur
COPY . /app/

# Installer Poetry
RUN pip install poetry

# Désactiver la création de virtualenv avec Poetry, puis installer les dépendances
RUN poetry config virtualenvs.create false && poetry install --only main --no-root

# Exposer le port 5000 pour l'application
EXPOSE 5000

# Commande pour lancer l'application
CMD ["python", "app.py"]
