import math
import random

from triangulator.triangulation import triangulate

# Tests unitaires pour la fonction de triangulation

def test_zero_point():
    assert triangulate([]) == [] # liste vide

def test_one_point():
    assert triangulate([(0,0)]) == []
    # 1 seul point ne peut pas former de triangle

def test_two_points():
    assert triangulate([(0,0), (1,1)]) == []
    # 2 points ne peuvent pas former de triangle

def test_three_points_make_triangle():
    points = [(0,0), (1,0), (0,1)]
    triangles = triangulate(points)
    assert len(triangles) == 1
    # Doit former un triangle

def test_four_points_two_triangles():
    points = [(0,0), (1,0), (1,1), (0,1)]
    triangles = triangulate(points)
    assert len(triangles) == 2
    # 4 points alors doit former excatement deux triangles

def test_colinear_points_no_triangle():
    points = [(0,0), (1,0), (2,0)]
    assert triangulate(points) == []
    # Verifie les points colineaires (ne forment pas de triangle)

def test_duplicate_points_no_triangle():
    points = [(0,0), (1,1), (1,1)]
    assert triangulate(points) == []
    # Verifie les points dupliques (ne forment pas de triangle)

def test_triangle_indices_valid():
    points = [(0,0), (1,0), (0,1)]
    triangles = triangulate(points)
    for t in triangles:
        assert all(0 <= idx < len(points) for idx in t)
        # Verifie que les indices des triangles sont valides

def test_no_duplicate_indices_in_triangle():
    points = [(0,0), (1,0), (0,1)]
    triangles = triangulate(points)
    for t in triangles:
        assert len(set(t)) == 3
        # Verifie qu'il n'y a pas d'indices dupliques dans un triangle

def test_positive_area():
    points = [(0,0), (1,0), (0,1)]
    triangles = triangulate(points)
    for a,b,c in triangles:
        # Aire du triangle > 0
        x1,y1 = points[a]
        x2,y2 = points[b]
        x3,y3 = points[c]
        area = abs((x2-x1)*(y3-y1) - (x3-x1)*(y2-y1))
        assert area > 0 # Verifie que l'aire du triangle est positive

def test_random():
    random.seed(42)

    n = 20
    points = [
        (math.cos(2 * math.pi * i / n), math.sin(2 * math.pi * i / n))
        for i in range(n)
    ]

    triangles = triangulate(points)

    for a, b, c in triangles:
        assert a != b
        assert b != c
        assert a != c
        assert 0 <= a < n
        assert 0 <= b < n
        assert 0 <= c < n
