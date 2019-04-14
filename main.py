from wsgiref.simple_server import make_server

from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.response import Response
from pyramid.config import Configurator
from user import user_request
from transaction import transaction_request
from login import login_entry

if __name__ == '__main__':
    with Configurator() as config:
        config.set_authorization_policy(ACLAuthorizationPolicy())
        # Enable JWT authentication.
        config.include('pyramid_jwt')
        config.set_jwt_authentication_policy('secret')

        config.add_route('users', '/usuarios')  # localhost:6543/
        config.add_view(user_request, route_name='users')
        config.add_route('transaction', '/transaccion')
        config.add_view(transaction_request, route_name='transaction')
        config.add_route('login', '/login')
        config.add_view(login_entry, route_name='login')
        app = config.make_wsgi_app()
    server = make_server('0.0.0.0', 6543, app)
    server.serve_forever()
