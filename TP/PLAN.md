# Plan de tests — Projet Triangulator

## Objectif général

L’objectif de ce plan de tests est de vérifier que le service Triangulator fonctionne correctement à tous les niveaux :
- calcul de la triangulation,
- gestion des cas limites et des erreurs,
- échange de données binaires,
- exposition d’une API fiable,
- stabilité et performances du service.

Les tests ont été conçus pour accompagner le développement et éviter les régressions.


## 1. Niveau Triangulation (tests unitaires)

Fichier concerné : tests/test_triangulation.py

Objectif : vérifier que la fonction de triangulation produit des triangles valides à partir d’un ensemble de points 2D.

### 1.1 Cas limites

Ces tests permettent de vérifier que l’algorithme ne plante pas sur des entrées simples ou invalides.

- 0 point → aucun triangle
- 1 point → aucun triangle
- 2 points → aucun triangle
Un triangle nécessite au minimum trois points.

- Points colinéaires → aucun triangle
Évite la création de triangles plats.

- Points dupliqués → aucun triangle
Évite les incohérences géométriques.



### 1.2 Cas de base

Ces tests valident le comportement attendu dans des situations classiques.

- 3 points non alignés → 1 triangle avec une aire strictement positive
- 4 points formant un carré → 2 triangles
Le choix de la diagonale n’est pas imposé.

- Plus de 4 points convexes → triangulation possible
L’objectif est de vérifier que l’algorithme retourne un résultat cohérent et ne plante pas.



### 1.3 Validations structurelles

Ces tests vérifient des propriétés qui doivent toujours être vraies, indépendamment de l’algorithme utilisé.

- Les indices des triangles sont compris entre 0 et n_points − 1
Chaque indice référence un point existant.

- Aucun triangle ne contient deux fois le même sommet
Exemple interdit : (0, 0, 1).

- L’aire de chaque triangle est strictement positive
Cela évite les triangles dégénérés.



### 1.4 Tests avec points générés

Des ensembles de points convexes sont générés (par exemple sur un cercle).

Les tests vérifient uniquement les invariants :
- indices valides,
- sommets distincts.

Le but est d’augmenter la robustesse sans dépendre d’un résultat exact.



## 2. Niveau Binaire (tests unitaires)

Fichier concerné : tests/test_binary.py

Objectif : vérifier la cohérence des fonctions d’encodage et de décodage binaire.

### 2.1 Cas nominal

- Encodage puis décodage d’un ensemble de points → données identiques
- Encodage puis décodage des triangles → données identiques

Ces tests garantissent la réversibilité du format binaire.



### 2.2 Cas d’erreur

- Binaire trop court → erreur levée
- Nombre de points incohérent → erreur levée
- Valeurs invalides (NaN) → erreur levée

Ces tests évitent les comportements silencieux ou incohérents.



## 3. Niveau API (tests d’intégration)

Fichier concerné : tests/test_api.py

Objectif : vérifier que l’API HTTP se comporte correctement du point de vue client.

### 3.1 Cas nominal

- Requête GET /triangulate?set_id=ID → code 200
- Content-Type application/octet-stream
- Réponse contenant des triangles encodés en binaire



### 3.2 Gestion des erreurs d’entrée

- set_id manquant → code 400
- set_id invalide (texte, vide, négatif) → code 400

La validation est effectuée avant tout traitement métier.



### 3.3 Robustesse

- Le service ne plante pas avec un grand nombre de points
- Les messages d’erreur sont simples et contrôlés
- Aucune stack trace Python n’est exposée



### 3.4 Méthodologie

- Utilisation du client Flask de test
- Mock du PointSetManager
- Vérification du code HTTP, des headers et du contenu de la réponse



## 4. Tests de performance

Fichier concerné : tests/test_performance.py

Objectif : vérifier la stabilité du service avec des entrées volumineuses.

### Cas testés

- 1 000 points
- 10 000 points
- 50 000 points

L’objectif est de vérifier que :
- l’algorithme ne plante pas,
- le temps de calcul reste raisonnable.

### Méthode

- Marquage des tests avec @pytest.mark.performance
- Exécution sélective :
  - pytest -m "not performance" pour les tests classiques
  - pytest -m performance pour les tests de charge


## 5. Couverture de tests

Objectif : obtenir une couverture pertinente, sans chercher le 100 % artificiel.

Commandes utilisées :
- coverage run -m pytest -m "not performance"
- coverage html

Principes appliqués :
- structure Arrange / Act / Assert
- tests ciblés sur les cas à risque
- ajout d’un test lors de la découverte d’un bug


## 6. Qualité de code

Objectif : maintenir un code lisible et maintenable.

Règles appliquées :
- respect du style avec ruff
- fonctions courtes
- noms explicites
- docstrings simples et utiles

Outils utilisés :
- ruff
- pdoc
