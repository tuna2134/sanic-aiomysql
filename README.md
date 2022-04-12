# sanic-aioMySQL

## setup

### install

```bash
pip install sanic-aioMySQL
```

### Use

```python
from sanic import Sanic, response
from sanic_mysql import ExtendMySQL

app = Sanic("app")
ExtendMySQL(app, user="root", host=127.0.0.1, password="hello")

@app.get("/")
async def main(request):
    await request.ctx.cursor.execute("CREATE TABLE data(name TEXT, value BIGINT)")
    return response.text("create a table")
    
app.run()
```
