Installation
============

Prérequis
---------

- Python 3.8 ou supérieur
- Git
- Docker (optionnel)

Installation locale
-------------------

Cloner le dépôt :

.. code-block:: bash

   git clone https://github.com/<utilisateur>/Python-OC-Lettings-FR.git
   cd Python-OC-Lettings-FR

Créer un environnement virtuel et installer les dépendances :

.. code-block:: bash

   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt

Appliquer les migrations :

.. code-block:: bash

   python manage.py migrate

Lancer le serveur :

.. code-block:: bash

   python manage.py runserver
