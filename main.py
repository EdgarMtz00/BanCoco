from wsgiref.simple_server import make_server
from pyramid.response import Response
from pyramid.config import Configurator
from user import user_request

if __name__ == '__main__':
    with Configurator() as config:
        config.add_route('users', '/usuarios/')  # localhost:6543/
        config.add_view(user_request, route_name='users')
        app = config.make_wsgi_app()
    server = make_server('0.0.0.0', 6543, app)
    server.serve_forever()
