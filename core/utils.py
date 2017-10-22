from aiohttp import web


def redirect(request, route_name, ):
    url = request.app.router[route_name].url()
    raise web.HTTPFound(url, )
