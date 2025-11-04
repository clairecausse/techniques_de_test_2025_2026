# TODO

### Plan des tests :

## 1.1 Niveau « Triangulation » (tests unitaires)
Objectif : vérifier que l'entrée de points génère bien les bons triangles

Nomenclature :
*italique* = explication
- tiret = test
### titre 3 = type de tests

### Cas limites
- 0, 1, 2 points → 0 triangle *(ne doit pas planter)*
- Points alignés → 0 triangle *(points sur une ligne)*
- Points dupliqués → pas de triangles *(évite bugs / confusion dans l'algo)*

### Cas de base
- 3 points non alignés → 1 triangle *(aire > 0)*
- 4 points (ex: carré) → 2 triangles *(peu importe la diagonale)*
- Plus de 4 points → triangulation possible *(ne pas planter, résultat cohérent)*

### Validations structurelles
- Indices des triangles ∈ [0, n_points − 1]
  *chaque indice pointe vers un vrai point*
- Pas deux fois le même sommet dans un triangle
  *ex: pas (0,0,1)*
- Aire strictement positive
  *éviter triangles plats ou faux*

### Binaire (encode / decode)
*Le Triangulator échange des données en binaire pour les points et les triangles*

- encode → decode des points ≈ identique *(tolérance float)*
- encode → decode des triangles = identique
- Mauvais formats → refus
  *taille tronquée, mauvais compteur, NaN / Inf → erreur attendue*

PyTest : `tests/test_triangulation.py`, `tests/test_binary.py`

---

## 1.2 Niveau « API » (intégration)
Objectif : vérifier que l’API du Triangulator répond bien comme prévu

Nomenclature :
*italique* = explication
- tiret = test
### titre 3 = type de tests

### Happy path
- GET `/triangulate?set_id=ID` → 200
  *réponse OK*
  - Content-Type = `application/octet-stream`
  - renvoie des triangles valides en binaire

### Erreurs d’entrée
- `set_id` manquant → 400
  *ID obligatoire*
- `set_id` invalide (vide, texte, non numérique, négatif…) → 400
  *vérif avant d'appeler le PointSetManager*

### Robustesse
- Ne plante pas avec beaucoup de points
  *grosse entrée = doit répondre*
- Message d’erreur simple *(pas de stack trace Python visible)*

### Sortie binaire
- Toujours renvoyer du binaire
- `Content-Type: application/octet-stream`

### Méthode de test
- fixture client Flask
- mock du PointSetManager
- vérification : code HTTP, headers, contenu binaire

PyTest : `tests/test_api.py`

---

## Tests de Couverture
Objectif : avoir une bonne couverture, mais surtout des tests utiles

Nomenclature :
*italique* = explication
- tiret = test
### titre 3 = type de tests

### Commandes
- coverage run -m pytest -m "not perf"
- coverage html

### Règles
- AAA *(Arrange / Act / Assert)*
- Fixtures pour points + client Flask
- Quand un bug apparaît → ajouter un test
  *éviter le “paradoxe du pesticide”*

---

## Tests de performance
Objectif : voir si le service reste correct avec beaucoup de points

Nomenclature :
*italique* = explication
- tiret = test
### titre 3 = type de tests

### Cas
- traitement 1k → 10k → 50k points
  *temps raisonnable, pas de crash*

### Méthode
- marquage `@pytest.mark.perf`
- `pytest -m "not perf"` → tests normaux
- `pytest -m perf` → tests performance uniquement

---

## Tests de Qualité de code
Objectif : garder un code propre et lisible

Nomenclature :
*italique* = explication
- tiret = test
### titre 3 = type de tests

### Règles
- ruff OK *(style respecté)*
- docstrings simples
- fonctions courtes
- noms clairs, pas de doublons

### Outils
- ruff
- pdoc3
