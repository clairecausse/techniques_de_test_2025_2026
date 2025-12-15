"""Encodage et décodage binaires des structures PointSet et Triangles.

Ce module implémente le format binaire défini dans la spécification du TP.

Format PointSet :
- 4 octets : entier non signé (nombre de points)
- pour chaque point :
    - 4 octets : float32 X
    - 4 octets : float32 Y

Format Triangles :
- section PointSet
- 4 octets : entier non signé (nombre de triangles)
- pour chaque triangle :
    - 4 octets : uint32 index1
    - 4 octets : uint32 index2
    - 4 octets : uint32 index3
"""

import math
import struct


def encode_point_set(points: list[tuple[float, float]]) -> bytes:
    """Encode un ensemble de points 2D en binaire.

    Args:
        points: Liste de couples (x, y).

    Returns:
        Représentation binaire du PointSet.

    """
    data = struct.pack(">I", len(points))  # big endian uint32
    for x, y in points:
        data += struct.pack(">ff", x, y)
    return data



def decode_point_set(data: bytes):
    """Encode un ensemble de points 2D en binaire.

    Args:
        points: Liste de couples (x, y).

    Returns:
        Représentation binaire du PointSet.

    """
    if len(data) < 4:
        raise ValueError("Binary too short for point count")

    count = struct.unpack(">I", data[:4])[0]
    expected_len = 4 + count * 8
    if len(data) != expected_len:
        raise ValueError("Invalid pointset length")

    points = []
    offset = 4

    for _ in range(count):
        x = struct.unpack(">f", data[offset:offset+4])[0]
        y = struct.unpack(">f", data[offset+4:offset+8])[0]

        # NEW CHECK (fix the failing test)
        if math.isnan(x) or math.isnan(y):
            raise ValueError("Invalid float value (NaN)")

        points.append((x, y))
        offset += 8

    return points

def encode_triangles(points: list[tuple[float, float]],
                     triangles: list[tuple[int, int, int]]) -> bytes:
    """Encode un ensemble de points et de triangles en binaire.

    Args:
        points: Liste des points 2D.
        triangles: Liste de triplets d’indices formant les triangles.

    Returns:
        Représentation binaire de la triangulation.

    """
    data = encode_point_set(points)
    data += struct.pack(">I", len(triangles))

    for a, b, c in triangles:
        data += struct.pack(">III", a, b, c)

    return data

def decode_triangles(binary: bytes):
    """Décode une structure binaire Triangles.

    Args:
        binary: Données binaires représentant une triangulation.

    Returns:
        Un tuple (points, triangles).

    Raises:
        ValueError: Si le format binaire est invalide.

    """
    if len(binary) < 4:
        raise ValueError("Binary too short")

    point_count = struct.unpack(">I", binary[:4])[0]
    point_section_len = 4 + point_count * 8

    if len(binary) < point_section_len + 4:
        raise ValueError("Binary too short for triangles section")

    # On décode *seulement* la partie pointset
    points = decode_point_set(binary[:point_section_len])

    # ----- 2. Lire la partie triangles -----
    offset = point_section_len

    triangle_count = struct.unpack(">I", binary[offset:offset+4])[0]
    offset += 4

    expected_len = point_section_len + 4 + triangle_count * 12
    if len(binary) != expected_len:
        raise ValueError("Invalid binary length for triangles")

    triangles = []
    for _ in range(triangle_count):
        i1 = struct.unpack(">I", binary[offset:offset+4])[0]
        i2 = struct.unpack(">I", binary[offset+4:offset+8])[0]
        i3 = struct.unpack(">I", binary[offset+8:offset+12])[0]
        triangles.append((i1, i2, i3))
        offset += 12

    return points, triangles

