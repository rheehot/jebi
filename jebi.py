import sys

__version__ = '0.1-dev'

from types import SimpleNamespace

from handy import makelist

try:
    _stdout, _stderr = sys.stdout.write, sys.stderr.write
except IOError:
    _stdout = lambda x: sys.stdout.write(x)
    _stderr = lambda x: sys.stderr.write(x)


def _cli_parse(args):
    from argparse import ArgumentParser

    parser = ArgumentParser(prog=args[0], usage="%(prog)s [options] package.module:app")
    opt = parser.add_argument
    opt("-b", "--bind", metavar="ADDRESS", help="bind socket to ADDRESS.")
    opt("-s", "--server", default='wsgiref', help="use SERVER as backend.")
    opt('app', help='WSGI app entry point.', nargs='?')

    cli_args = parser.parse_args(args[1:])

    return cli_args, parser


class Route:
    def __init__(self, app, rule, method, callback, name=None, **config):
        self.app = app
        pass


class Router:
    def __init__(self):
        pass

    def add(self):
        pass

    def match(self):
        pass


class Jebi:
    def __init__(self, **kwargs):
        self.routes = []
        self.router = Router()
        self.error_handler = {}

        pass

    def mount(self):
        pass

    def run(self, **kwargs):
        run(self, **kwargs)

    def get_url(self, route_name, **kwargs):
        pass

    def add_route(self, route):
        self.routes.append(route)
        pass

    def route(self, path=None, method='GET', callback=None, name=None, **config):
        """
        A decorator to bind a function to a request URL

        @app.route('/hello/<name>')
        def hello(name):
            return 'world'
        :param path:
        """

        def decorator(callback):
            for rule in makelist(path):
                for verb in makelist(method):
                    verb = verb.upper()
                    route = Route(self, rule, verb, callback, name=name, **config)
                    self.add_route(route)
            return callback

        return decorator(callback) if callback else decorator

    def get(self, path=None, method='GET', **options):
        return self.route(path, method, **options)

    def post(self, path=None, method='POST', **options):
        return self.route(path, method, **options)

    def wsgi(self, environ, start_response):
        pass


def run(app=None, server='wsgiref', host='127.0.0.1', port=8080, **kwargs):
    """
    start a server instance
    :param app: WSGI application
    :param server: Server
    :param host: Server address to bind
    :param port: Server port to bind

    """
    server = server(host=host, port=port, **kwargs)
    server.run(app)


#########################
# HTTP and WSGI Tools   #
#########################

class BaseRequest:
    """
    A wrapper for WSGI environment dictionaries that adds new attributes to request
    """
    __slots__ = ('environ',)

    # TODO: set buffer size

    def __init__(self, environ=None):
        self.environ = {} if environ is None else environ
        self.environ['jebi.request'] = self


class BaseResponse:
    """
    A class for a response body, headers and cookies.
    :param body: The response body
    :param status: An HTTP code
    :param headers: A dict like name-value pairs
    """
    default_status = 200
    default_content_type = 'text/html; charset=UTF-8'

    def __init__(self, body='', status=None, headers=None, **kwargs):
        self._headers = {}
        self.body = body
        self.status = status


#########################
# Constants and Globals #
#########################

DEBUG = False


def _main(argv):
    args, parser = _cli_parse(argv)

    if args.version:
        _stdout(f'jebi {__version__}\n')
        sys.exit(0)

    sys.path.insert(0, '.')
    sys.modules.setdefault('bottle', sys.modules['__main__'])

    host, port = (args.bind or 'localhost'), 8080
    if ':' in host and host.rfind(']') < host.rfind(':'):
        host, port = host.rsplit(':', 1)
    host = host.strip('[]')

    run(args.app,
        host=host,
        port=int(port))


if __name__ == '__main__':
    _main(sys.argv)
