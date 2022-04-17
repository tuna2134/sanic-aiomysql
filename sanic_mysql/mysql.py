from sanic import Sanic, Request
from aiomysql import create_pool, Pool
from functools import wraps
import asyncio

def cursor():
    def decorator(f):
        @wraps(f)
        async def decorator_function(request, *args, **kwargs):
            connection = await request.ctx.pool.acquire()
            cursor = await connection.cursor()
            response = await f(request, connection, cursor, *args, **kwargs)
            request.ctx.pool.release(connection)
            return response
        return decorator_function
    return decorator

class ConnectionError(Exception):
    pass

class ExtendMySQL:
    """Easy to use MySQL.
    
    Args:
        app (sanic.Sanic): sanic application
        loop (asyncio.AbstractEventLoop): If you want to specify loop, please write a loop here.
        auto (bool): If you want to use request.ctx.connection and request.ctx.cursor, please make it true.
    """
    def __init__(self, app: Sanic, loop: asyncio.AbstractEventLoop=None, auto: bool=False, *args, **kwargs):
        self.auto: bool = auto
        self.loop: asyncio.AbstractEventLoop = loop
        self.setting = (args, kwargs)
        self.app: Sanic = app
        self.__pool: Pool = None
        app.register_listener(self.before_server_start, "before_server_start")
        app.register_middleware(self.on_request, "request")
        app.register_middleware(self.on_response, "response")

    @property
    def pool(self) -> Pool:
        """return aiomysql.Pool
        
        Returns:
           aiomysql.Pool: return pool.
        """
        if self.__pool is not None:
            return self.__pool
        else:
            raise ConnectionError("Please connect to MySQL server")
    
    async def close(self) -> None:
        "close pool"
        self.pool.close()
        await self.pool.wait_closed()
        self.__pool = None

    async def before_server_start(self, app: Sanic, loop: asyncio.AbstractEventLoop) -> None:
        args, kwargs = self.setting
        if self.loop is None:
            kwargs["loop"] = loop
        if self.app is not None:
            self.__pool = await create_pool(*args, **kwargs)
        else:
            raise ConnectionError("Already connected to MySQL server.")

    async def on_request(self, request: Request) -> None:
        request.ctx.pool: Pool = self.pool
        if self.auto:
            request.ctx.connection = await self.pool.acquire()
            request.ctx.cursor = await request.ctx.connection.cursor()

    async def on_response(self, request: Request, response) -> None:
        if hasattr(request.ctx, "connection"):
            self.pool.release(request.ctx.connection)
