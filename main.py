from wsgiref.simple_server import make_server
from pyramid.response import Response
from pyramid.config import Configurator
def hello_world(request):
    return Response(
        status=200,
        content_type="text/plain",
        body='hola'
    )


if __name__ == '__main__':
    with Configurator() as config:
        config.add_route('hello', '/')  # localhost:6543/
        config.add_view(hello_world, route_name='hello')
        app = config.make_wsgi_app()
    server = make_server('0.0.0.0', 6543, app)
    server.serve_forever()
