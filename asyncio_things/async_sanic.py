from sanic import Sanic
from sanic.response import text, json

app = Sanic(__name__)


@app.route("/")
async def query(request):
    return json(dict(message="hola mundo"))


if __name__ == '__main__':
    app.run(port=7777)
