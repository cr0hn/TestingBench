from aiohttp import web


async def anti_fingerprinting_middleware(app, handler):
    async def middleware_handler_middleware(request):
        response = await handler(request)
        response.headers["Server"] = "Apache"
        
        return response
    
    return middleware_handler_middleware


# --------------------------------------------------------------------------
# Routes
# --------------------------------------------------------------------------
async def example_basic_login(request):
    return web.Response(text="Hello world!")


def setup_anti_fingerprint(app: web.Application):
    app.middlewares.append(anti_fingerprinting_middleware)


def main():
    app = web.Application()
    
    app.router.add_route('GET', "/", example_basic_login)
    
    # setup auth
    setup_anti_fingerprint(app)
    
    web.run_app(app, host="127.0.0.1")


if __name__ == '__main__':
    main()
