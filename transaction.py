from sqlalchemy import text
from sqlalchemy.engine import ResultProxy
from sqlalchemy.sql.elements import TextClause
from pyramid.response import Response
from database import db
from decimal import Decimal
from datetime import datetime
import json


def alchemyencoder(obj):
    """JSON encoder function for SQLAlchemy special classes."""
    if isinstance(obj, datetime):
        return obj.isoformat()
    elif isinstance(obj, Decimal):
        return float(obj)

def get_transactions(request):
    user_id = request.params.get('id', -1)
    if user_id == -1:
        return Response(status=404)
    else:
        try:
            stmt: TextClause = text('SELECT * from Bancoco."Trasaccion" where "Trasaccion"."Cuentahabiente" = :id')
            stmt = stmt.bindparams(id=user_id)
            transaction = db.execute(stmt)
            return Response(status=200, body=json.dumps([dict(r) for r in transaction][0], default=alchemyencoder),
                            content_type='text/json')
        except Exception as e:
            print(e)
            return Response(status=404, content_type='text/plain')


def create_transaction(request):
    try:
        user_data = request.json_body
        stmt: TextClause = text('INSERT into bancoco."Trasaccion"("Monto",'
                                '"Status",'
                                '"Fecha",'
                                '"Descipcion",'
                                '"Institucion",'
                                '"Cuentahabiente") VALUES (:monto, :status, :fecha, '
                                ':desc, :institucion, :cuentahabiente)')
        stmt = stmt.bindparams(monto=user_data['monto'], status=user_data['status'], fecha=user_data['fecha'],
                               desc=user_data['descripcion'],
                               institucion=user_data['institucion'], cuentahabiente=user_data['cuentahabiente'])
        db.execute(stmt)
        return Response(status=200)
    except Exception as e:
        print(e)
        return Response(status=400)


def delete_transaction(request):
    try:
        user_data = request.json_body
        stmt: TextClause = text('Delete from bancoco."Trasaccion" where "Trasaccion"."ID" = :id')
        stmt = stmt.bindparams(id=user_data['id'])
        db.execute(stmt)
        return Response(status=200, content_type='text/json')
    except Exception as e:
        print(e)
        return Response(status=400, content_type='text/plain')


def transaction_request(request):
    if request.method == 'GET':
        return get_transactions(request)
    elif request.method == 'POST':
        return create_transaction(request)
    elif request.method == 'DELETE':
        return delete_transaction(request)
