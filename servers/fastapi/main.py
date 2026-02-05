from firebase_functions import https_fn
from firebase_admin import initialize_app
from api.main import app as fast_api_app

initialize_app()

@https_fn.on_request()
def api(req: https_fn.Request) -> https_fn.Response:
    """ Handle all requests to the FastAPI app """
    return https_fn.Response.from_asgi(fast_api_app, req)
