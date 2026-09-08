
import math
from decimal import Decimal
from neo4j.time import Date, DateTime, Time, Duration
from neo4j.spatial import Point

def normalize_neo4j(value):
    """
    Convierte tipos Neo4j y otros tipos problemáticos a valores serializables por JSON.
    
    Maneja:
    - Float especiales (inf, -inf, nan)
    - Tipos Neo4j (Date, DateTime, Time, Duration, Point)
    - Decimal
    - Recursivamente dicts, listas y tuplas
    """
    
    # Manejar floats especiales (inf, -inf, nan) que no son JSON compatibles
    if isinstance(value, float):
        if math.isnan(value):
            return None  # Cambiar a "NaN" si prefieres string
        elif math.isinf(value):
            return None  # Cambiar a "Infinity" o "-Infinity" si prefieres string
        return value
    
    # Manejar Decimal
    if isinstance(value, Decimal):
        return float(value) if not (math.isnan(float(value)) or math.isinf(float(value))) else None
    
    if isinstance(value, (Date, DateTime, Time)):
        return str(value)
    
    elif isinstance(value, Duration):
        return str(value)  # ej: "PT1H2M3S"
    
    elif isinstance(value, Point):
        return {
            "x": value.x,
            "y": value.y,
            "z": value.z if hasattr(value, 'z') else None,
            "srid": value.srid if hasattr(value, 'srid') else None
        }
    
    elif isinstance(value, dict):
        return {k: normalize_neo4j(v) for k, v in value.items()}
    
    elif isinstance(value, (list, tuple)):
        return [normalize_neo4j(v) for v in value]
    
    return value
