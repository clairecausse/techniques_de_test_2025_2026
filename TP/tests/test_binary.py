import pytest
from triangulator.binary import (
    encode_point_set, decode_point_set,
    encode_triangles, decode_triangles
)

# Tests unitaires pour les fonctions d'encodage/décodage binaire

def test_encode_decode_point_set_roundtrip():
    points = [(1.0, 2.0), (3.0, 4.0)]
    binary = encode_point_set(points)
    decoded = decode_point_set(binary)
    assert decoded == points # Verifie que l'encodage et le decodage sont coherents

def test_encode_decode_triangles_roundtrip():
    points = [(0,0), (1,0), (0,1)]
    triangles = [(0,1,2)]
    binary = encode_triangles(points, triangles)
    dec_points, dec_tris = decode_triangles(binary)
    assert dec_points == points
    assert dec_tris == triangles # Verifie que l'encodage et le decodage des triangles sont coherents

def test_decode_invalid_binary():
    with pytest.raises(Exception):
        decode_point_set(b"invalid") # Verifie que le decodage d'un binaire invalide leve une exception

def test_decode_nan_float():
    bad = b"\x00\x00\x00\x01" + b"\x7f\xc0\x00\x00" + b"\x00\x00\x00\x00"
    with pytest.raises(Exception):
        decode_point_set(bad) # Verifie que le decodage d'un float NaN leve une exception

def test_incorrect_point_count():
    bad = b"\x00\x00\x00\x02" + b"\x00"*8
    with pytest.raises(Exception):
        decode_point_set(bad) # Verifie que le decodage avec un nombre de points incorrect leve une exception
