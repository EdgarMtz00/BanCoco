from pyramid.response import Response
from pyramid.request import Request
from pyramid.view import view_config
from sqlalchemy import text
from sqlalchemy.engine import ResultProxy
from sqlalchemy.sql.elements import TextClause

from database import db
import json


@view_config(request_method='POST')
def login_entry(request):
    nickname = request.json_body['nombreUsuario']
    pwd = request.json_body['contrasena']

    try:
        stmt: TextClause = text('SELECT "Tarjeta" from bancoco."Cuentahabiente" where "Nickname" = :nickname AND "Contrasena" = :pwd')
        stmt = stmt.bindparams(nickname=nickname, pwd=pwd)
        result: ResultProxy = db.execute(stmt)
        user = [dict(r) for r in result][0]
        print(user)
        if user is not None:
            token = request.create_jwt_token(user['Tarjeta'])
            return Response(status=200, content_type='application/json',
                            body=json.dumps({'token': token}),
                            charset='utf-8')
    except Exception as e:
        return Response(status=404, content_type='application/json')
    return Response(status=404, content_type='application/json')
