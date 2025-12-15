import pytest

from triangulator.binary import (
    decode_point_set,
    decode_triangles,
    encode_point_set,
    encode_triangles,
)


def test_encode_decode_point_set_roundtrip():
    """Vérifie que l'encodage puis le décodage d'un pointset est cohérent."""
    points = [(1.0, 2.0), (3.0, 4.0)]
    binary = encode_point_set(points)
    decoded = decode_point_set(binary)

    assert decoded == points


def test_encode_decode_triangles_roundtrip():
    """Vérifie que l'encodage puis le décodage des triangles est cohérent."""
    points = [(0.0, 0.0), (1.0, 0.0), (0.0, 1.0)]
    triangles = [(0, 1, 2)]

    binary = encode_triangles(points, triangles)
    decoded_points, decoded_triangles = decode_triangles(binary)

    assert decoded_points == points
    assert decoded_triangles == triangles


def test_decode_invalid_binary():
    """Vérifie qu'un binaire invalide provoque une ValueError."""
    with pytest.raises(ValueError):
        decode_point_set(b"invalid")


def test_decode_nan_float():
    """Vérifie qu'un float NaN dans le binaire provoque une ValueError."""
    bad_binary = (
        b"\x00\x00\x00\x01"
        + b"\x7f\xc0\x00\x00"
        + b"\x00\x00\x00\x00"
    )

    with pytest.raises(ValueError):
        decode_point_set(bad_binary)


def test_incorrect_point_count():
    """Vérifie qu'un nombre de points incohérent provoque une ValueError."""
    bad_binary = b"\x00\x00\x00\x02" + b"\x00" * 8

    with pytest.raises(ValueError):
        decode_point_set(bad_binary)
