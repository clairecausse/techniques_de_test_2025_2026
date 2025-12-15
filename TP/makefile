
PY              := ./.venv/bin/python
PIP             := ./.venv/bin/pip
PYTEST          := $(PY) -m pytest
COVERAGE        := $(PY) -m coverage

# Marker utilisé pour isoler les tests de performance
PERF_MARK       := performance

# PYTHONPATH local pour l'import des modules
PYTHONPATH      := .

.PHONY: help venv install install-dev test test-verbose unit_test perf_test coverage lint doc run clean



help:
	@echo "Commandes disponibles :"
	@echo "  make venv          -> crée un environnement virtuel Python (.venv)"
	@echo "  make install       -> installe les dépendances runtime"
	@echo "  make install-dev   -> installe les dépendances de développement"
	@echo "  make test          -> lance les tests unitaires (hors performance)"
	@echo "  make test-verbose  -> lance les tests avec affichage détaillé"
	@echo "  make unit_test     -> alias de 'test' (consigne du TP)"
	@echo "  make perf_test     -> lance uniquement les tests de performance"
	@echo "  make coverage      -> génère un rapport de couverture HTML"
	@echo "  make lint          -> vérifie la qualité du code avec ruff"
	@echo "  make doc           -> génère la documentation HTML avec pdoc"
	@echo "  make run           -> lance l'API Flask pour tests manuels"
	@echo "  make clean         -> nettoie l'environnement et fichiers temporaires"


# Alias demandé par l'énoncé du TP
unit_test: test

venv:
	python3 -m venv .venv
	. .venv/bin/activate && $(PIP) install --upgrade pip setuptools wheel


install: venv
	. .venv/bin/activate && $(PIP) install -r requirements.txt

install-dev: venv
	. .venv/bin/activate && $(PIP) install -r dev_requirements.txt


# Tests unitaires
test:
	PYTHONPATH=$(PYTHONPATH) $(PYTEST) -v -ra


test-wp:
	PYTHONPATH=$(PYTHONPATH) $(PYTEST) -v -ra -m "not $(PERF_MARK)"


# Tests de performance uniquement
perf:
	PYTHONPATH=$(PYTHONPATH) $(PYTEST) -v -m "$(PERF_MARK)"

coverage:
	PYTHONPATH=$(PYTHONPATH) $(COVERAGE) run -m pytest -m "not $(PERF_MARK)"
	$(COVERAGE) html -d htmlcov

lint:
	. .venv/bin/activate && $(PY) -m ruff check triangulator tests

doc:
	PYTHONPATH=$(PYTHONPATH) $(PY) -m pdoc --html triangulator --output-dir docs --force

run:
	PYTHONPATH=$(PYTHONPATH) FLASK_APP=triangulator.api flask run --port=5001

clean:
	rm -rf .venv __pycache__ htmlcov docs .pytest_cache .coverage
