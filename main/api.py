
from ninja import NinjaAPI
from ninja import Schema

api = NinjaAPI()

    


@api.get("/imports")
def hello(request):
    return "Hello world"
