import ast
from decimal import Decimal
from sqlalchemy import text
from sqlalchemy.engine import ResultProxy
from sqlalchemy.sql.elements import TextClause
from pyramid.response import Response
from database import db
from query_to_json import to_json
from datetime import datetime
from datetime import date
import json


def alchemyencoder(obj):
    """JSON encoder function for SQLAlchemy special classes."""
    if isinstance(obj, datetime):
        return obj.isoformat()
    elif isinstance(obj, Decimal):
        return float(obj)


def date_hook(json_dict, format='%Y-%m-%d'):
    d = {}
    for k, v in json_dict:
        if isinstance(v, datetime):
            try:
                d[k] = datetime.strptime(v, format).date()
            except ValueError:
                d[k] = v
        else:
            d[k] = v
    return d


def get_user(request):
    user_id = request.params.get('id', -1)
    if user_id == -1:
        return Response(status=404)
    else:
        try:
            stmt: TextClause = text('SELECT "ID",'
                                    '"Nickname",'
                                    '"Correo",'
                                    '"Nombre",'
                                    '"Apellido_paterno",'
                                    '"Apellido_materno",'
                                    '"Municipio",'
                                    '"Tarjeta",'
                                    '"Fecha_Expiracion",'
                                    '"Fondos" from Bancoco."Cuentahabiente" where "ID" = :id')
            stmt = stmt.bindparams(id=user_id)

            user = db.execute(stmt)
            return Response(status=200, body=json.dumps([dict(r) for r in user][0], default=alchemyencoder),
                            content_type='text/json')
        except Exception as e:
            print(e)
    return Response(status=404, content_type='text/plain')


def create_user(request):
    try:
        user_data = request.json_body
        stmt: TextClause = text('INSERT into bancoco."Cuentahabiente"("Nickname",'
                                '"Correo",'
                                '"Contrasena",'
                                '"Nombre",'
                                '"Apellido_paterno",'
                                '"Apellido_materno",'
                                '"Tarjeta",'
                                '"Fecha_Expiracion",'
                                '"CVV",'
                                '"Fondos",'
                                '"CP",'
                                '"Municipio") VALUES (:nickname, :correo, :contrasena, '
                                ':nombre, :apellido_paterno, :apellido_materno, :tarjeta, :fecha_expiracion, :cvv, :fondos, :cp, :municipio)')

        stmt = stmt.bindparams(nickname=user_data['nickName'], correo=user_data['correo'],
                               contrasena=user_data['contrasena'],
                               nombre=user_data['nombre'], apellido_paterno=user_data['apellidoPaterno'],
                               apellido_materno=['apellidoMaterno'], tarjeta=user_data['tarjeta'],
                               fecha_expiracion=user_data['fechaExpiracion'], cvv=user_data['ccv'],
                               fondos=user_data['fondos'],
                               cp=user_data['cp'], municipio=user_data['municipio'])
        db.execute(stmt)
        return Response(status=200)
    except Exception as e:
        print(e)
        return Response(status=400)


def modify_user(request):
    #try:
        user_data = request.json_body
        user_stmt = text('SELECT * from bancoco."Cuentahabiente" where "ID" = :id').bindparams(id=user_data['id'])
        users = db.execute(user_stmt)
        user: dict = [dict(r) for r in users][0]
        if 'nickName' in user_data:
            user['nickName'] = user_data['nickName']
        if 'correo' in user_data:
            user['correo'] = user_data['correo']
        if 'contrasena' in user_data:
            user['contrasena'] = user_data['contrasena']
        if 'correo' in user_data:
            user['Correo'] = user_data['correo']
        if 'nombre' in user_data:
            user['nombre'] = user_data['nombre']
        if 'apellidoPaterno' in user_data:
            user['apellidoPaterno'] = user_data['apellidoPaterno']
        if 'fechaExpiracion' in user_data:
            user['fechaExpiracion'] = user_data['fechaExpiracion']
        if 'ccv' in user_data:
            user['ccv'] = user_data['ccv']
        if 'fondos' in user_data:
            user['fondos'] = user_data['fondos']
        if 'cp' in user_data:
            user['cp'] = user_data['cp']
        if 'municipio' in user_data:
            user['municipio'] = user_data['municipio']

        update_stmt = text(
            'UPDATE bancoco."Cuentahabiente" SET '
            '"Nickname" = :nickname, '
            '"Correo" = :correo, '
            '"Contrasena" = :contrasena, '
            '"Nombre" = :nombre, '
            '"Apellido_paterno" = :apellido_paterno, '
            '"Apellido_materno" = :apellido_materno, '
            '"Tarjeta" = :tarjeta, '
            '"Fecha_Expiracion" = :fecha_expiracion, '
            '"CVV" = :cvv, '
            '"Fondos" = :fondos, '
            '"CP" = :cp, '
            '"Municipio" = :municipio where "ID" = :id'
        ).bindparams(nickname=user['Nickname'], correo=user['correo'], contrasena=user['Contrasena'],
                     nombre=user['Nombre'], apellido_paterno=user['Apellido_paterno'],
                     apellido_materno=['Apellido_materno'], tarjeta=user['Tarjeta'],
                     fecha_expiracion=user['Fecha_Expiracion'], cvv=user['CVV'], fondos=user['Fondos'],
                     cp=user['CP'], municipio=user['Municipio'], id=user_data['id'])
        db.execute(update_stmt)
        return Response(status=200)
    #except Exception as e:
        #print(e)
        #return Response(status=404, content_type='text/json')


def user_request(request):
    if request.method == 'GET':
        return get_user(request)
    elif request.method == 'POST':
        return create_user(request)
    elif request.method == 'PUT':
        return modify_user(request)
