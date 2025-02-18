# Default installation method (conda or uv)
INSTALL_METHOD ?= conda

# Virtual environment name
ENV_NAME = rag

# Dependencies
REQ_FILE = requirements/requirements.txt
REQ_DEV_FILE = requirements/requirements.dev.txt

# 🏗 Initialize the virtual environment (Only creates it, dependencies installed separately)
init:
	@if [ "$(INSTALL_METHOD)" = "conda" ]; then \
		echo "📦 Creating Conda environment..."; \
		conda create --name $(ENV_NAME) python=3.11 -y; \
		echo "✅ Activate it with: conda activate $(ENV_NAME)"; \
	elif [ "$(INSTALL_METHOD)" = "uv" ]; then \
		echo "🚀 Creating environment with uv..."; \
		uv venv --python=python3.11; \
		echo "✅ Activate it with: source .venv/bin/activate"; \
	else \
		echo "❌ Unknown method. Use INSTALL_METHOD=conda or INSTALL_METHOD=uv"; \
		exit 1; \
	fi

# 📦 Install dependencies using pip (since some packages are not available in Conda)
.PHONY: requirements
requirements:
	@if [ "$(INSTALL_METHOD)" = "conda" ]; then \
		echo "📦 Installing dependencies with pip inside Conda environment..."; \
		conda run -n $(ENV_NAME) pip install --upgrade pip; \
		conda run -n $(ENV_NAME) pip install -r $(REQ_FILE); \
		conda run -n $(ENV_NAME) pip install -r $(REQ_DEV_FILE); \
	elif [ "$(INSTALL_METHOD)" = "uv" ]; then \
		echo "📦 Installing dependencies with uv..."; \
		uv pip install -r $(REQ_FILE) && uv pip install -r $(REQ_DEV_FILE); \
	else \
		echo "❌ Unknown method."; \
		exit 1; \
	fi

# 🚀 Run the project
.PHONY: run
run:
	@if [ "$(INSTALL_METHOD)" = "conda" ]; then \
		echo "🚀 Running with Conda..."; \
		conda run -n $(ENV_NAME) python backend/main.py; \
	elif [ "$(INSTALL_METHOD)" = "uv" ]; then \
		echo "🚀 Running with uv..."; \
		uv venv exec python backend/main.py; \
	else \
		echo "❌ Unknown method."; \
		exit 1; \
	fi

# 🛠 Clean temporary files
clean:
	@rm -rf __pycache__ .pytest_cache
	@find . -name '*.pyc' -exec rm -r {} +
	@find . -name '__pycache__' -exec rm -r {} +
	@rm -rf build dist
	@find . -name '*.egg-info' -type d -exec rm -r {} +
	@rm -rf project_structure.json
	@rm -rf .mypy_cache
	@rm -rf .pytest_cache
	@rm -rf .ruff_cache
	@rm -rf outputs
	@rm -rf backend/docs
	@rm -rf backend/chroma_db

# ❌ Remove virtual environments (Conda & UV)
clean_env:
	@echo "🧹 Removing virtual environments..."
	@rm -rf .venv  # Remove UV virtual environment
	@conda remove --name $(ENV_NAME) --all -y || true  # Remove Conda environment (if exists)
	@echo "✅ Environments removed successfully."

# 🏗 Build & run Docker containers
build:
	@docker-compose up --build -d

# 📦 Stop and remove Docker containers
stop:
	@docker-compose down

# 🛠 Run pre-commit hooks
pre-commit:
	@pre-commit install
	@pre-commit run --all-files
