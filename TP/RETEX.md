# RETEX.md – Retour d’expérience sur le projet *Triangulator*

## 1. Introduction

Ce projet avait pour objectif de développer un micro-service de triangulation en adoptant une démarche *test-first*.
Au-delà de l’implémentation fonctionnelle, l’enjeu principal était d’apprendre à concevoir un projet Python structuré et robuste, intégrant dès le départ des tests unitaires, des tests d’API, des tests de robustesse et de performance, ainsi que des outils de qualité de code (linting, documentation, couverture de tests).

Ce retour d’expérience présente ce qui a bien fonctionné, les difficultés rencontrées tout au long du projet, les compromis réalisés, et ce que je ferais différemment avec davantage de recul.


## 2. Ce qui a bien fonctionné

### Mise en place d’un environnement de tests complet

Dès le début du projet, j’ai mis en place une structure claire et cohérente :

- une arborescence explicite (`triangulator/`, `tests/`)
- une configuration de `pytest` avec des *markers* pour différencier les types de tests
- des mocks permettant d’isoler les dépendances
- un `Makefile` automatisant l’ensemble du workflow (tests, lint, documentation, coverage)

Cette organisation m’a permis de travailler dans un cadre proche de pratiques professionnelles, tout en gardant une vision claire de l’état du projet à chaque étape.

### Approche *test-first*

Avant même d’implémenter le code fonctionnel, l’ensemble des tests était écrit :
tests de triangulation, tests d’encodage/décodage binaire, tests d’API et de gestion d’erreurs.

Cette approche *test-first* m’a permis :

- de clarifier les spécifications dès le départ,
- d’éviter de coder « à l’aveugle »,
- de détecter très rapidement les régressions lors des modifications.

Même si cela demande un effort initial plus important, cela a rendu le développement globalement plus fluide et plus sûr.

### Bonne séparation logique du code

Le projet est structuré autour de trois modules principaux :

- l’API,
- la gestion du format binaire,
- la triangulation.

Cette séparation claire a facilité :

- l’écriture de tests indépendants,
- le mock de l’API sans dépendance externe,
- la compréhension globale du fonctionnement du micro-service.

Chaque module a une responsabilité bien définie, ce qui a limité les effets de bord.

### Utilisation cohérente des mocks

Les tests d’API n’ont jamais dépendu d’un service externe réel.
Grâce à `pytest-mock`, j’ai pu simuler :

- les appels à `requests.get`,
- les erreurs réseau,
- les réponses incorrectes ou incomplètes.

Cela m’a permis de tester des scénarios difficiles à reproduire autrement, tout en gardant des tests rapides et déterministes.

### Qualité de code et outillage

L’utilisation de `ruff`, du typage et de la documentation m’a obligé à maintenir un code propre et lisible tout au long du projet.
La génération automatique de la documentation via `pdoc3` fonctionne correctement et reflète fidèlement l’architecture du projet.


## 3. Difficultés rencontrées
### Difficulté n°1 : tester les tests eux-mêmes

L’une des principales difficultés a concerné la conception des tests, et non le code en lui-même.

Les mocks étant entièrement définis par moi, ils répondaient naturellement aux tests que j’avais écrits. Cela crée un biais :
les tests validaient surtout que le code correspondait à mes hypothèses, et non nécessairement à tous les comportements possibles du système.

Il a donc fallu un réel effort de réflexion pour :

- imaginer des scénarios d’erreur crédibles,
- introduire des incohérences volontaires dans les mocks,
- tester des comportements inattendus.



### Difficulté n°2 : comprendre et implémenter correctement le format binaire

Le format binaire des `PointSet` et des `Triangles` était très strict, et plusieurs erreurs sont apparues au cours du développement :

- mauvaise interprétation de la taille des sections,
- tentative incorrecte de réutilisation de `decode_point_set` dans `decode_triangles`,
- oublis de validation (NaN, tailles incohérentes, données incomplètes).

Ces erreurs n’étaient pas toujours évidentes à identifier sans tests précis.
Les tests de robustesse m’ont permis de localiser exactement les cas problématiques et d’améliorer progressivement la fiabilité du décodage.

### Difficulté n°3 : interactions entre modules

Une difficulté plus globale du projet a été la gestion des interactions entre modules.
Certaines décisions prises dans un module (par exemple le format des données retournées par le binaire) avaient des impacts indirects sur l’API ou sur les tests.

Avec le recul, j’ai parfois sous-estimé ces dépendances, ce qui a entraîné :

- des ajustements tardifs,
- des corrections en cascade,
- des tests à adapter après modification de la logique interne.

# Triangulation : choix d’un algorithme adapté au contexte du TP

Implémenter une triangulation générale et optimale, comme une triangulation de Delaunay, aurait nécessité un investissement algorithmique important et dépassait le cadre temporel et pédagogique du TP.

J’ai donc fait le choix d’un algorithme volontairement simple : une triangulation naïve par éventail (fan triangulation), applicable à des polygones convexes.
Ce choix présente plusieurs avantages dans le contexte du TP :
- il permet de garantir la production de triangles valides,
- l’implémentation est courte, lisible et fiable,
- le comportement est facilement testable, notamment sur les cas limites,
- la complexité algorithmique est maîtrisée (linéaire).

Pour éviter que les lignes ne se croisent, j'ai supposé que:
- les points fournis forment un polygone convexe,
- les points sont triés dans l'ordre (horaire ou antihoraire)


## 4. Ce que j’aurais pu mieux faire
### Mieux anticiper les interactions entre modules

Avec davantage de recul, j’aurais pris plus de temps en amont pour définir précisément :

- les formats d’échange entre modules,
- les responsabilités exactes de chacun,
- les invariants à respecter.

Cela aurait probablement réduit le nombre d’ajustements tardifs et simplifié l’évolution du code.

### Tester davantage les cas extrêmement limites

Même si la couverture de tests est bonne, j’aurais pu aller plus loin en ajoutant :

- des valeurs flottantes extrêmement grandes ou très proches de zéro,
- des fichiers binaires volontairement tronqués ou corrompus,
- des triangles mal formés ou incohérents.

Ces tests auraient renforcé encore davantage la robustesse globale du micro-service.


## 6. Conclusion

Partir d’une page blanche pour concevoir un micro-service complet a été une expérience très formatrice.
Ce projet m’a permis de mieux comprendre :

- l’importance d’une approche *test-first*,
- la difficulté réelle de concevoir de bons tests,
- la nécessité d’une architecture claire et évolutive.

Le résultat final est un système fonctionnel, testé, documenté et automatisé, conforme aux attentes du TP et proche de pratiques professionnelles.
Ce projet constitue une base solide pour aborder des développements plus complexes à l’avenir.
