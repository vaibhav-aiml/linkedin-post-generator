import sys
import os

# Add root directory to sys.path so 'backend' module is discoverable
root_dir = os.path.dirname(os.path.abspath(__file__))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

from backend.app.main import app as fast_app

# Attempt to wrap FastAPI with a2wsgi for WSGI servers if invoked with standard Gunicorn worker
try:
    from a2wsgi import ASGIMiddleware
    wsgi_app = ASGIMiddleware(fast_app)
except Exception:
    wsgi_app = None


class AppWrapper:
    """
    Dual-compatibility ASGI/WSGI wrapper.
    Supports ASGI (Uvicorn / Gunicorn UvicornWorker) and WSGI (default Gunicorn SyncWorker).
    """
    def __init__(self, asgi, wsgi):
        self.asgi = asgi
        self.wsgi = wsgi

    def __getattr__(self, item):
        return getattr(self.asgi, item)

    def __call__(self, scope_or_environ, receive_or_start_response=None, send=None):
        if send is not None:
            # ASGI protocol call: app(scope, receive, send)
            return self.asgi(scope_or_environ, receive_or_start_response, send)
        elif self.wsgi is not None:
            # WSGI protocol call: app(environ, start_response)
            return self.wsgi(scope_or_environ, receive_or_start_response)
        else:
            return self.asgi(scope_or_environ, receive_or_start_response, send)


app = AppWrapper(fast_app, wsgi_app)

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("app:app", host="0.0.0.0", port=port, reload=True)
