class static_generator(object):
    def __init__(self, expires: int = 3600, unless: bool = False):
        self.expires = expires
        self.unless = unless
    
    def __call__(self, f):
        f.static_builder_enable = True
        f.static_builder_cache_expires = self.expires
        f.static_builder_cache_unless = self.unless
        
        return f
    
    
__all__ = ("cache", )
