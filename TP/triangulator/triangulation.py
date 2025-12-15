"""Triangulation d’un ensemble de points en deux dimensions.

Cette implémentation fournit une triangulation simple et déterministe,
adaptée au cadre du TP.

Caractéristiques :
- gestion des cas simples (0, 1, 2, 3 et 4 points),
- triangulation naïve par éventail d’un polygone convexe,
- exclusion explicite des cas dégénérés (points colinéaires, doublons),
- refus des polygones non convexes.
"""


def _area(a: tuple[float, float],
          b: tuple[float, float],
          c: tuple[float, float]) -> float:
    """Calcule l’aire orientée du triangle (a, b, c).

    Une valeur positive indique une orientation directe,
    une valeur négative une orientation indirecte,
    et une valeur nulle correspond à des points colinéaires.

    Args:
        a: Premier point.
        b: Deuxième point.
        c: Troisième point.

    Returns:
        Aire orientée du triangle.

    """
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])


def _is_colinear(a: tuple[float, float],
                 b: tuple[float, float],
                 c: tuple[float, float]) -> bool:
    """Détermine si trois points sont colinéaires.

    Args:
        a: Premier point.
        b: Deuxième point.
        c: Troisième point.

    Returns:
        True si les points sont colinéaires, False sinon.

    """
    return abs(_area(a, b, c)) < 1e-12


def _is_convex_polygon(points: list[tuple[float, float]]) -> bool:
    """Vérifie si un ensemble de points forme un polygone convexe.

    Les points sont supposés ordonnés le long du contour du polygone.

    Args:
        points: Liste ordonnée de points 2D.

    Returns:
        True si le polygone est convexe, False sinon.

    """
    n = len(points)
    if n < 3:
        return False

    sign = None
    for i in range(n):
        a = points[i]
        b = points[(i + 1) % n]
        c = points[(i + 2) % n]
        cross = _area(a, b, c)

        if abs(cross) < 1e-12:
            continue

        if sign is None:
            sign = cross > 0
        elif (cross > 0) != sign:
            return False

    return True


def triangulate(
    points: list[tuple[float, float]],
) -> list[tuple[int, int, int]]:
    """Triangule un ensemble de points formant un polygone convexe.

    L’algorithme repose sur une triangulation par éventail à partir
    du premier sommet. Cette approche est volontairement simple et
    suffisante dans le cadre du TP.

    Args:
        points: Liste ordonnée de points 2D.

    Returns:
        Liste de triangles, chaque triangle étant représenté
        par un triplet d’indices dans la liste des points.

    Raises:
        NotImplementedError: Si le polygone n’est pas convexe.

    """
    n = len(points)

    if n < 3:
        return []

    # Présence de doublons → triangulation impossible
    if len(set(points)) != n:
        return []

    # Cas de trois points
    if n == 3:
        if _is_colinear(points[0], points[1], points[2]):
            return []
        return [(0, 1, 2)]

    # Tous les points sont-ils colinéaires ?
    all_colinear = True
    for i in range(n - 2):
        if not _is_colinear(points[i], points[i + 1], points[i + 2]):
            all_colinear = False
            break

    if all_colinear:
        return []

    # Vérification de la convexité
    if not _is_convex_polygon(points):
        raise NotImplementedError(
            "Triangulation générale non implémentée."
        )

    # Triangulation par éventail
    triangles = []
    for i in range(1, n - 1):
        triangles.append((0, i, i + 1))

    return triangles
