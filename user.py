from sqlalchemy import text
from sqlalchemy.engine import ResultProxy
from sqlalchemy.sql.elements import TextClause
from pyramid.response import Response
from database import db
from encoder import Encoder
import json


def user_request(request):
    if request.method == 'GET':
        return get_user(request)
    elif request.method == 'POST':
        return create_user(request)
    elif request.method == 'PUT':
        return update_user(request)


def get_user(request):
    user_id = request.params.get('tarjeta', -1)
    if user_id == -1:
        return Response(status=404)
    else:
        try:
            stmt: TextClause = text('SELECT '
                                    '"Nickname",'
                                    '"Correo",'
                                    '"Nombre", '
                                    '"Apellido_paterno", '
                                    '"Apellido_materno",'
                                    '"Municipio",'
                                    '"Tarjeta",'
                                    '"Fecha_Expiracion",'
                                    '"Contrasena",'
                                    '"Fondos" from Bancoco."Cuentahabiente" where "Tarjeta" = :tarjeta')
            stmt = stmt.bindparams(tarjeta=user_id)
            user: ResultProxy = db.execute(stmt)
            result = user.fetchall()
            return Response(status=200, body=json.dumps([dict(r) for r in result], default=Encoder),
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

        stmt = stmt.bindparams(nickname=user_data['nickname'], correo=user_data['correo'],
                               contrasena=user_data['contrasena'],
                               nombre=user_data['nombre'], apellido_paterno=user_data['apellidoPaterno'],
                               apellido_materno=user_data['apellidoMaterno'], tarjeta=user_data['tarjeta'],
                               fecha_expiracion=user_data['fechaExpiracion'], cvv=user_data['cvv'],
                               fondos=user_data['fondos'],
                               cp=user_data['cp'], municipio=user_data['municipio'])
        db.execute(stmt)
        return Response(status=200)
    except Exception as e:
        print(e)
        return Response(status=400)


def update_user(request):
    try:
        user_data = request.json_body

        user_stmt = text('SELECT * from bancoco."Cuentahabiente" where "Tarjeta" = :tarjeta').bindparams(
            tarjeta=user_data['Tarjeta'])
        users = db.execute(user_stmt)
        user = ([dict(r) for r in users][0])
        if 'Nombre' in user_data:
            user['Nombre'] = user_data['Nombre']
        if 'Apellido_paterno' in user_data:
            user['Apellido_paterno'] = user_data['Apellido_paterno']
        if 'Apellido_materno' in user_data:
            user['Apellido_materno'] = user_data['Apellido_materno']
        if 'nickname' in user_data:
            user['nickname'] = user_data['nickname']
        if 'Correo' in user_data:
            user['Correo'] = user_data['Correo']
        if 'Contrasena' in user_data:
            user['Contrasena'] = user_data['Contrasena']
        if 'Nickname' in user_data:
            user['Nickname'] = user_data['Nickname']
        if 'Fondos' in user_data:
            user['Fondos'] = user_data['Fondos']
        if 'Municipio' in user_data:
            user['Municipio'] = user_data['Municipio']
        if 'CP' in user_data:
            user['CP'] = user_data['CP']

        update_stmt = text(
            'UPDATE bancoco."Cuentahabiente" SET "Nickname" = :nickname,'
            '"Correo" = :correo,'
            '"Contrasena" = :contrasena,'
            '"Nombre" = :nombre,'
            '"Apellido_paterno" = :apellidoPaterno,'
            '"Apellido_materno" = :apellidoMaterno,'
            '"Fecha_Expiracion" = :fechaExpiracion,'
            '"CVV" = :cvv,'
            '"Fondos" = :fondos,'
            '"CP" = :cp,'
            '"Municipio" = :municipio where "Tarjeta" = :tarjeta'
        ).bindparams(nickname=user['Nickname'], correo=user['Correo'],
                     contrasena=user['Contrasena'],
                     nombre=user['Nombre'], apellidoPaterno=user['Apellido_paterno'],
                     apellidoMaterno=user['Apellido_materno'], tarjeta=user['Tarjeta'],
                     fechaExpiracion=user['Fecha_Expiracion'], cvv=user['CVV'],
                     fondos=user['Fondos'],
                     cp=user['CP'], municipio=user['Municipio'])
        db.execute(update_stmt)
        return Response(status=200, content_type='text/json')
    except Exception as e:
        print(e)
        return Response(status=404, content_type='text/json')
