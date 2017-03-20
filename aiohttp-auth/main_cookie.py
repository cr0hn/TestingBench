import asyncio

import jwt
import json

from collections import defaultdict
from typing import Union, Dict, Callable

from aiohttp import web
from aiohttp_session import get_session, setup as setup_session
from aiohttp_session.cookie_storage import EncryptedCookieStorage
from booby import Model, String, Boolean, Collection

KEY = "asdfñksajdfpoiasfhpasnfiasubfiasufgdhiasufhasiu"
AUTH = dict(asdfsa="asdf")


class Role(Model):
    __ignore_missing__ = True
    
    name = String()

    read = Boolean(default=True)
    write = Boolean(default=False)
    modify = Boolean(default=False)
    grant = Boolean(default=False)
    is_admin = Boolean(default=False)


class Group(Model):
    __ignore_missing__ = True
    
    name = String()
    roles = Collection(Role)


class User(Model):
    __ignore_missing__ = True
    
    username = String()
    password = String()
    is_active = Boolean(default=False)
    
    groups = Collection(Group)


class QuerySet:
    
    def __init__(self, connection):
        pass
    
    def get_user(self, username: str, password: str = None) -> Union[ValueError, User]:
        """
        Get an User instance
        """
        r = Role(name="view")
        
        g = Group(name="admin", roles=[r])
        
        user = User(username=username,
                    password=password,
                    groups=[g])

        if not user.is_valid:
            raise ValueError("Invalid format")
        
        return user
    
    def dump_jwt(self, user: User, key) -> str:
        return jwt.encode(json.loads(user.to_json()), key)


# --------------------------------------------------------------------------
# Decorators
# --------------------------------------------------------------------------
class login_required(object):
    """
    Decorator for the views. By applying this, the view is marked as authenticated
    """
    def __init__(self, groups=None, roles=None):
        self.groups = groups or []
        self.roles = roles or []
    
    def __call__(self, f):
        f.login_required = True
        f.login_roles = self.roles
        f.login_groups = self.groups
        
        return f


class permissions_required(object):
    """
    Decorator for the views. By applying this, the view is marked as authenticated
    """
    def __init__(self, permissions=None):
        self.permissions = permissions or []
    
    def __call__(self, f):
        f.login_required = True
        f.login_permissions = self.permissions
        
        return f


# --------------------------------------------------------------------------
# Aux
# --------------------------------------------------------------------------
def get_auth(app: web.Application) -> QuerySet:
    return app["AUTH"]


def get_paths(request: web.Request) -> Dict[str, Callable]:
    """
    return a dict with all the view path and their handler
    
    :return: return a dict with all the view path and their handler
    :rtype: dict(str, callable)
    """
    return {x.url(): x.handler for x in request.app.router.routes()}


async def get_user_from_session(request: web.Request) -> Union[ValueError, User]:
    """
    Get an JWT token an return a User object instance
    
    :return: User Instance
    :rtype: User
    
    :raise ValueError: Some error appear
    """

    session = await get_session(request)
    
    user = User(**json.loads(session["USER"]))
    
    if not user.is_valid:
        raise ValueError("Invalid user information")
    
    return user


def has_valid_groups_or_roles(path: str, handler: Callable, user: User) -> Union[ValueError, None]:
    """
    Check if an user has permissions for access to the requested URL
    
    :raise ValueError: Permissions are not correct
    """
    roles = handler.login_roles
    groups = handler.login_groups
    
    # Check if user is in an any valid group
    if groups and not any(x.name in groups for x in user.groups):
        raise ValueError("User '{}' is not in any valid group for '{}' view".format(user.username, path))

    # Check if User has a valid role
    if roles and groups:
        for group in user.groups:
            if not any(role.name in roles for role in group.roles):
                raise ValueError("User '{}' is has not a valid role for '{}' view".format(user.username, path))
                
    return


def has_required_permissions(path: str, handler: Callable, user: User) -> Union[ValueError, None]:
    """
    Check if an user has permissions for access to the requested URL
    
    :raise ValueError: Permissions are not correct
    """
    permissions = handler.login_permissions
    
    # Split groups / permissions
    groups = defaultdict(list)
    for permission in permissions:
        try:
            group, perm = permission.split(".")
            
            if perm == "*":
                groups[group] = perm
            else:
                groups[group].append(perm)
        except ValueError:
            # Too many value to unpack
            group = permission
            perm = "*"
            groups[group] = perm
        
    # Check if user is in an any valid group
    if groups and not any(x.name in groups for x in user.groups):
        raise ValueError("User '{}' is not in any valid group for '{}' view".format(user.username, path))

    # Check if User has a valid role
    if groups:
        for group in user.groups:
            if not any(role.name in groups[group.name] or groups[group.name] == "*" for role in group.roles if groups.get(group.name, None)):
                raise ValueError("User '{}' is has valid role for '{}' view".format(user.username, path))
                
    return

# --------------------------------------------------------------------------
# Middlewares
# --------------------------------------------------------------------------
async def login_middleware_cookie(app, handler):  # TODO
    async def middleware_handler_login(request):
        # Check if current request is authorized
        current_path = request.path
    
        try:
            # The view has authentication?
            _view_handler = get_paths(request)[current_path]
    
        except KeyError:
            # View has not authentications
            pass
    
        else:
            if getattr(_view_handler, "login_required", False):
            
                # Get User from Session Token
                try:
                    user = await get_user_from_session(request)
                except ValueError as e:
                    return web.Response(body=e, status=400)
            
                try:
                    # Select permissions function to use
                    if getattr(_view_handler, "login_permissions", False):
                        has_required_permissions(current_path, _view_handler, user)
                    else:
                        has_valid_groups_or_roles(current_path, _view_handler, user)
                except ValueError as e:
                    return web.Response(text=str(e), status=403)
            
                # Check Permissions
                request.user = user
    
        return await handler(request)

    return middleware_handler_login


# --------------------------------------------------------------------------
# Routes
# --------------------------------------------------------------------------
@login_required()
async def example_basic_login(request):
    return web.Response(text="Hello world!")


@permissions_required(permissions=["admin.*"])
async def example_group(request):
    
    return web.Response(text="Admin view!")


@login_required(groups=["admin"], roles=["view"])
async def example_group_with_role(request):
    return web.Response(text="Admin view!")


async def login(request: web.Request):
    
    # Get user info
    user = request.GET.get("user")
    password = request.GET.get("password")
    
    auth = get_auth(request.app)
    
    # Try to get from DB
    user = auth.get_user(user, password)
    
    session = await get_session(request)
    session["USER"] = user.to_json()
    
    return web.Response(body=b'Oks!')


# --------------------------------------------------------------------------
# Setup functions
# --------------------------------------------------------------------------
def setup_auth(app: web.Application):
    app.middlewares.append(login_middleware_cookie)

    app["AUTH"] = QuerySet(None)


def main():
    app = web.Application()
    
    app.router.add_route('GET', "/", example_basic_login)
    app.router.add_route('GET', "/admin/view", example_group_with_role)
    app.router.add_route('GET', "/admin", example_group)
    app.router.add_route('GET', "/login", login)
    
    setup_session(app,
                  EncryptedCookieStorage(b'Thirty  two  length  bytes  key.',
                                         cookie_name="JSESSION_ID"))
    # setup auth
    setup_auth(app)
    
    web.run_app(app, host="127.0.0.1")


if __name__ == '__main__':
    main()
