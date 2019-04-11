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


#
# TODO:fix update_user
#
def update_user(request):
    # try:
    user_data = request.json_body

    user_stmt = text('SELECT * from bancoco."Cuentahabiente" where "Tarjeta" = :tarjeta').bindparams(
        tarjeta=user_data['tarjeta'])
    users = db.execute(user_stmt)
    user = ([dict(r) for r in users][0])
    if 'nombre' in user_data:
        user['nombre'] = user_data['nombre']
    if 'apellidoPaterno' in user_data:
        user['apellidoPaterno'] = user_data['apellidoPaterno']
    if 'apellidoMaterno' in user_data:
        user['apellidoMaterno'] = user_data['apellidoMaterno']
    if 'nickname' in user_data:
        user['nickname'] = user_data['nickname']
    if 'correo' in user_data:
        user['correo'] = user_data['correo']
    if 'contrasena' in user_data:
        user['contrasena'] = user_data['contrasena']

    update_stmt = text(
        'UPDATE bancoco."Cuentahabiente" SET "Nickname" = :nickname,'
        '"Correo" = :correo,'
        '"Contrasena" = :contrasena,'
        '"Nombre" = :nombre,'
        '"Apellido_paterno" = :apellidoPaterno,'
        '"Apellido_materno" = :apellidoMaterno,'
        '"Tarjeta" = :tarjeta,'
        '"Fecha_Expiracion" = :fechaExpiracion,'
        '"CVV" = :cvv,'
        '"Fondos" = :fondos,'
        '"CP" = :cp,'
        '"Municipio" = :municipio where "Tarjeta" = :tarjeta'
    ).bindparams(nickname=user['nickname'], correo=user['correo'],
                 contrasena=user['contrasena'],
                 nombre=user['nombre'], apellido_paterno=user['apellidoPaterno'],
                 apellido_materno=user['apellidoMaterno'], tarjeta=user['tarjeta'],
                 fecha_expiracion=user['fechaExpiracion'], cvv=user['ccv'],
                 fondos=user['fondos'],
                 cp=user['cp'], municipio=user['municipio'])
    db.execute(update_stmt)

# except Exception as e:
# print(e)
# return Response(status=404, content_type='text/json')
