#commandes de base (évite les répétitions)
PY        := python3
PIP       := $(PY) -m pip
PYTEST    := $(PY) -m pytest
COVERAGE  := $(PY) -m coverage

# Ce marker servira à isoler les tests de performance
PERF_MARK := performance

# chemin du Python dans le dossier courant
PYTHONPATH := .

# Les cibles ci-dessous ne créent pas de fichiers. C'est une bonne pratique de les déclarer comme .PHONY
.PHONY: help venv install install-dev test unit_test perf_test coverage lint doc run clean


help:
	@echo "Commandes disponibles :"
	@echo "  make venv         -> crée un environnement virtuel Python (.venv)"
	@echo "  make install      -> installe les dépendances runtime"
	@echo "  make install-dev  -> installe les dépendances de développement"
	@echo "  make test         -> lance tous les tests sauf les tests de performance"
	@echo "  make unit_test    -> alias de 'test'"
	@echo "  make perf_test    -> lance uniquement les tests de performance"
	@echo "  make coverage     -> génère un rapport de couverture HTML"
	@echo "  make lint         -> vérifie la qualité du code avec ruff"
	@echo "  make doc          -> génère la documentation HTML avec pdoc"
	@echo "  make run          -> lance l'API Flask pour des tests manuels"
	@echo "  make clean        -> supprime les fichiers temporaires"


# environnement virtuel local
venv:
	$(PY) -m venv .venv
	. .venv/bin/activate && $(PIP) install --upgrade pip setuptools wheel


# install les dependences
install: venv
	. .venv/bin/activate && $(PIP) install -r requirements.txt

install-dev: venv
	. .venv/bin/activate && $(PIP) install -r dev_requirements.txt


# Lance tous les tests qui ne sont pas des tests de performance
# Les tests de performance sont exclus car ils peuvent être longs
test:
	PYTHONPATH=$(PYTHONPATH) $(PYTEST) -q -m "not $(PERF_MARK)"


# Alias de test pour respecter les consignes du TP
unit_test: test


# Lance uniquement les tests marqués comme tests de performance
perf_test:
	PYTHONPATH=$(PYTHONPATH) $(PYTEST) -q -m "$(PERF_MARK)"


# Exécute les tests sous coverage puis génère un rapport HTML dans htmlcov/
coverage:
	PYTHONPATH=$(PYTHONPATH) $(COVERAGE) run -m pytest
	$(COVERAGE) html -d htmlcov
	@echo "Rapport de couverture disponible dans htmlcov/index.html"


# Vérifie la qualité du code Python avec ruff
lint:
	. .venv/bin/activate && $(PY) -m ruff check triangulator tests


# Génère la doc HTML via pdoc dans un dossier docs/
doc:
	PYTHONPATH=$(PYTHONPATH) $(PY) -m pdoc --html triangulator --output-dir docs --force


# Lance le serveur Flask pour des essais manuels
run:
	PYTHONPATH=$(PYTHONPATH) FLASK_APP=triangulator.api flask run --port=5000


# Nettoie l'environnement et les fichiers générés
clean:
	rm -rf .venv __pycache__ htmlcov docs .pytest_cache .coverage
