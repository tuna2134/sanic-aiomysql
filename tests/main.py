import pytest
import sanic_mysql
from sanic_testing import TestManager
from sanic import Sanic, response

@pytest.fixture
def app():
    sanic_app = Sanic("TestSanic")
    TestManager(sanic_app)
    sanic_mysql.ExtendMySQL(app, host="", user="", password="")
    
    @sanic_app.get("/")
    @sanic_mysql.cursor()
    async def basic(request, connection, cursor):
        await cursor.execute("SELECT * FROM test")
        return response.text("foo")
    return sanic_app
    
def test_basic_test_client(app):
    request, response = app.test_client.get("/")
    assert request.method.lower() == "get"
    assert response.body == b"foo"
    assert response.status == 200
