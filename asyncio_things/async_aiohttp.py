import asyncio

from aiohttp import web

try:
    import uvloop
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
except ImportError:
    pass

async def handle(request):
    return web.Response(text="Hola Mundo")

app = web.Application()
app.router.add_get('/', handle)

web.run_app(app, host="127.0.0.1", port=9999)