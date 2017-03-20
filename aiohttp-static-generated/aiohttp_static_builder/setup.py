import logging

from aiohttp import web

from .backends import *
from .middleware import *
from .exceptions import *

log = logging.getLogger("aiohttp")


def setup_static_builder(app: web.Application,
                         static_builder_type: str = "local"):
    app.middlewares.append(cache_middleware)
    
    _static_builder_backend = None
    if static_builder_type.lower() == "local":
        _static_builder_backend = MemoryStaticBuilder()
    else:
        raise HTTPCache("Invalid cache type selected")
    
    app["static_builder"] = _static_builder_backend


__all__ = ("setup_static_builder", )
