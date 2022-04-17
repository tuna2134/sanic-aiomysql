from sanic import Sanic, Request
from aiomysql import create_pool, Pool

class ConnectionError(Exception):
    pass

class ExtendMySQL:
    def __init__(self, app: Sanic, loop=None, auto=False, *args, **kwargs):
        self.auto: bool = auto
        self.loop = loop
        self.setting = (args, kwargs)
        self.app: Sanic = app
        self.__pool: Pool = None
        app.register_listener(self.before_server_start, "before_server_start")
        app.register_middleware(self.on_request, "request")
        app.register_middleware(self.on_response, "response")

    @property
    def pool(self) -> Pool:
        if self.__pool is not None:
            return self.__pool
        else:
            raise ConnectionError("Please connect to MySQL server")
    
    async def close(self) -> None:
        self.pool.close()
        await self.pool.wait_closed()
        self.__pool = None

    async def before_server_start(self, app: Sanic, loop) -> None:
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
