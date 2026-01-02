# récupération de l'image officielle de Python 3.10 allégée
FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements-prod.txt

# Copie des fichiers de l'application dans le conteneur
COPY . .

# Collecte des fichiers statiques
RUN python manage.py collectstatic --noinput

# Exposition du port 8000
EXPOSE 8000
# Commande pour démarrer l'application avec Gunicorn
CMD ["gunicorn", "oc_lettings_site.wsgi:application", "--bind", "0.0.0.0:8000"]
