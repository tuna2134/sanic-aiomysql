# sanic-aiomysql
[![Downloads](https://pepy.tech/badge/sanic-aiomysql)](https://pepy.tech/project/sanic-aiomysql)
[![Downloads](https://pepy.tech/badge/sanic-aiomysql/month)](https://pepy.tech/project/sanic-aiomysql)
[![Downloads](https://pepy.tech/badge/sanic-aiomysql/week)](https://pepy.tech/project/sanic-aiomysql)

## setup

### install

```bash
pip install sanic-aiomysql
```

or

```bash
pip install git+https://github.com/tuna2134/sanic-aiomysql.git
```

### Use

```python
from sanic import Sanic, response
from sanic_mysql import ExtendMySQL

app = Sanic("app")
ExtendMySQL(app, auto=True, user="root", host=127.0.0.1, password="hello", autocommit=True)

@app.get("/")
async def main(request):
    await request.ctx.cursor.execute("CREATE TABLE data(name TEXT, value BIGINT)")
    return response.text("create a table")
    
app.run()
```

or

```python
from sanic import Sanic, response
from sanic_mysql import ExtendMySQL

app = Sanic("app")
ExtendMySQL(app, user="root", host=127.0.0.1, password="hello", autocommit=True)

@app.get("/")
async def main(request):
    async with request.ctx.pool.acquire() as conn:
        async with conn.cursor() as cursor:
            await cursor.execute("CREATE TABLE data(name TEXT, value BIGINT)")
    return response.text("create a table")
    
app.run()
```

or

```python
from sanic import Sanic, response
from sanic_mysql import ExtendMySQL, cursor

app = Sanic("app")
ExtendMySQL(app, user="root", host=127.0.0.1, password="hello", autocommit=True)

@app.get("/")
@cursor()
async def main(request, connection, cursor):
    await cursor.execute("CREATE TABLE data(name TEXT, value BIGINT)")
    return response.text("create a table")
    
app.run()
```
