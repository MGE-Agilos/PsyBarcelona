"""Douglas-Peucker simplification for GeoJSON polygons (rings split in two so closed rings simplify)."""
import math


def dp(pts, eps):
    if len(pts) < 3:
        return pts
    a, b = pts[0], pts[-1]
    dx, dy = b[0] - a[0], b[1] - a[1]
    L = math.hypot(dx, dy) or 1e-12
    md, mi = 0, 0
    for i in range(1, len(pts) - 1):
        p = pts[i]
        d = abs(dy * p[0] - dx * p[1] + b[0] * a[1] - b[1] * a[0]) / L
        if d > md:
            md, mi = d, i
    if md > eps:
        return dp(pts[:mi + 1], eps)[:-1] + dp(pts[mi:], eps)
    return [a, b]


def ring(r, eps):
    m = len(r) // 2
    pts = dp(r[:m + 1], eps)[:-1] + dp(r[m:], eps)
    return [[round(x, 5), round(y, 5)] for x, y in pts]


def geom(g, eps):
    if g['type'] == 'Polygon':
        return {'type': 'Polygon', 'coordinates': [ring(r, eps) for r in g['coordinates']]}
    return {'type': 'MultiPolygon', 'coordinates': [[ring(r, eps) for r in p] for p in g['coordinates']]}


def _area(r):
    return sum(r[i][0] * r[i + 1][1] - r[i + 1][0] * r[i][1] for i in range(len(r) - 1)) / 2


def rewind_d3(g):
    """d3-geo expects clockwise exterior rings (the reverse of RFC 7946)."""
    def fix(rings):
        return [r[::-1] if (_area(r) > 0) == (i == 0) else r for i, r in enumerate(rings)]
    if g['type'] == 'Polygon':
        return {'type': 'Polygon', 'coordinates': fix(g['coordinates'])}
    return {'type': 'MultiPolygon', 'coordinates': [fix(p) for p in g['coordinates']]}
