# Définition de la méthode d'installation (conda par défaut)
INSTALL_METHOD ?= conda

# Nom de l'environnement virtuel
ENV_NAME = myenv

# Dépendances
REQ_FILE = requirements/requirements.txt
REQ_DEV_FILE = requirements/requirements.dev.txt

# 🏗 Initialisation de l'environnement virtuel
init:
	@if [ "$(INSTALL_METHOD)" = "conda" ]; then \
		echo "📦 Installation avec Conda..."; \
		conda create --name $(ENV_NAME) python=3.11 -y; \
		conda activate $(ENV_NAME); \
		conda install --file $(REQ_FILE) -y; \
		conda install --file $(REQ_DEV_FILE) -y; \
	elif [ "$(INSTALL_METHOD)" = "uv" ]; then \
		echo "🚀 Installation avec uv..."; \
		uv venv --python=python3.11; \
		uv pip install -r $(REQ_FILE); \
		uv pip install -r $(REQ_DEV_FILE); \
	else \
		echo "❌ Méthode inconnue. Utilisez INSTALL_METHOD=conda ou INSTALL_METHOD=uv"; \
		exit 1; \
	fi

# 🚀 Lancer le projet
run:
	@if [ "$(INSTALL_METHOD)" = "conda" ]; then \
		conda activate $(ENV_NAME) && python backend/main.py; \
	elif [ "$(INSTALL_METHOD)" = "uv" ]; then \
		uv venv exec python backend/main.py; \
	else \
		echo "❌ Méthode inconnue."; \
		exit 1; \
	fi

# 🛠 Nettoyage des fichiers temporaires
clean:
	@rm -rf __pycache__ .pytest_cache
	@find . -name '*.pyc' -exec rm -r {} +
	@find . -name '__pycache__' -exec rm -r {} +
	@rm -rf build dist
	@find . -name '*.egg-info' -type d -exec rm -r {} +
	@rm -rf .venv  # Supprime l'environnement uv
	@conda remove --name $(ENV_NAME) --all -y || true
	@rm -rf project_structure.json

# 🏗 Construction des containers avec Docker
build:
	@docker-compose up --build -d

# 📦 Arrêter et supprimer les containers Docker
stop:
	@docker-compose down

pre-commit:
	@pre-commit install
	@pre-commit run --all-files
