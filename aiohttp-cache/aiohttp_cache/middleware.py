from aiohttp.web_reqrep import Response

async def cache_middleware(app, handler):
    async def middleware_handler(request):
        if getattr(handler, "cache_enable", True):
            #
            # Cache is disabled?
            #
            if getattr(handler, "cache_unless", False) is True:
                return await handler(request)
            
            cache_backend = app["cache"]
            
            key = cache_backend.make_key(request)
            
            if await cache_backend.has(key):
                cached_response = await cache_backend.get(key)
            
                return Response(**cached_response)
            
            #
            # Generate cache
            #
            original_response = await handler(request)
            
            data = dict(status=original_response.status,
                        headers=dict(original_response.headers),
                        body=original_response.body)
            
            await cache_backend.set(key, data)
            
            return original_response
        
        # Not cached
        return await handler(request)
    
    return middleware_handler


__all__ = ("cache_middleware", )
