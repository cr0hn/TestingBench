import time
import pickle
import asyncio
import warnings

import aiohttp.web

try:
    import aioredis
except ImportError:
    warnings.showwarning("aioredis library not found. Redis cache client not available")


class BaseStaticBuilder(object):
    
    def __init__(self, expiration: int = 300, base_path: str = None):
        self.base_path = base_path
        self.expiration = expiration
    
    async def write(self, content: str, path: str) -> object:
        raise NotImplementedError()
    
    def make_key(self, request: aiohttp.web.Request) -> str:
        key = "{method}{host}{path}{postdata}{ctype}".format(method=request.method,
                                                             path=request.path_qs,
                                                             host=request.host,
                                                             postdata="".join(request.post()),
                                                             ctype=request.content_type)
        
        return key


class _Config:
    def __init__(self,
                 expiration: int = 300):
        self.expiration = expiration


# --------------------------------------------------------------------------
# MEMORY BACKEND
# --------------------------------------------------------------------------
class LocalStaticBuilder(BaseStaticBuilder):
    
    def __init__(self,
                 *,
                 expiration=300):
        super().__init__(expiration=expiration)
        
        #
        # Cache format:
        # (cached object, expire date)
        #
        self._cache = {}
    
    async def write(self, content: str, path: str):
        # Update the keys
        self._update_expiration_key(key)
        
        try:
            cached = self._cache[key]
            
            return cached[0]
        except KeyError:
            return None

__all__ = ("LocalStaticBuilder", )
