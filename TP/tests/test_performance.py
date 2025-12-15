import pytest

from triangulator.triangulation import triangulate


# Tests de performance pour la fonction de triangulation
@pytest.mark.performance
def test_triangulation_1k_points():
    points = [(i, i*0.1) for i in range(1000)]
    triangulate(points)

@pytest.mark.performance
def test_triangulation_10k_points():
    points = [(i, i*0.1) for i in range(10000)]
    triangulate(points)

@pytest.mark.performance
def test_triangulation_50k_points():
    points = [(i, i*0.1) for i in range(50000)]
    triangulate(points)
