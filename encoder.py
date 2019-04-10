from datetime import date, datetime
from decimal import Decimal


def Encoder(obj):
    """JSON encoder function for SQLAlchemy special classes."""
    if isinstance(obj, date) | isinstance(obj, datetime):
        return obj.isoformat()
    elif isinstance(obj, Decimal):
        return float(obj)
