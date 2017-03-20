from aiohttp.web_reqrep import Response

async def static_builder_middleware(app, handler):
    async def middleware_handler(request):
        if getattr(handler, "static_builder_enable", True):
            #
            # Cache is disabled?
            #
            if getattr(handler, "static_builder_cache_unless", False) is True:
                return await handler(request)
            
            static_builder = app["static_builder"]
            
            key = static_builder.make_key(request)
            
            if await static_builder.has(key):
                cached_response = await static_builder.get(key)
            
                return Response(**cached_response)
            
            #
            # Generate cache
            #
            original_response = await handler(request)
            
            data = dict(status=original_response.status,
                        headers=dict(original_response.headers),
                        body=original_response.body)
            
            await static_builder.set(key, data)
            
            return original_response
        
        # Not cached
        return await handler(request)
    
    return middleware_handler


__all__ = ("cache_middleware", )
