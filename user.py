from sqlalchemy import text
from sqlalchemy.engine import ResultProxy
from sqlalchemy.sql.elements import TextClause
from pyramid.response import Response
from database import db
from query_to_json import to_json
import json


def user_request(request):
    if request.method == 'GET':
        return get_user(request)


def get_user(request):
    user_id = request.params.get('id', -1)
    if user_id == -1:
        return Response(status=404)
    else:
        try:
            stmt: TextClause = text('SELECT "ID", '
                                    '"Nickname",'
                                    '"Correo",'
                                    '"Nombre", '
                                    '"Apellido_paterno", '
                                    '"Apellido_materno",'
                                    '"Municipio",'
                                    '"Tarjeta",'
                                    '"Fecha_Expiracion",'
                                    '"Fondos" from Bancoco."Cuentahabiente" where "ID" = :id')
            stmt = stmt.bindparams(id=user_id)

            get_user: ResultProxy = db.execute(stmt)
            result = get_user.fetchall()
            return Response(status=200, body=to_json(result[0]), content_type='text/json')
        except Exception as e:
            print(e)
    return Response(status=404, content_type='text/plain')


def _create_user(request):
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

        stmt = stmt.bindparams(nickname=user_data['nickName'], correo=user_data['correo'], contrasena=user_data['contrasena'],
                               nombre=user_data['nombre'], apellido_paterno=user_data['apellidoPaterno'],
                               apellido_materno=['apellidoMaterno'], tarjeta=['tarjeta'],
                               fecha_expiracion=user_data['fechaExpiracion'], cvv=user_data['ccv'], fondos=user_data['fondos'],
                               cp=user_data['cp'], municipio=user_data['municipio'])
        db.execute(stmt)
        return Response(status=200)
    except Exception:
        return Response(status=400)