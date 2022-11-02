from flask import Flask

from storage.bucket import bucket_blueprint
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from prometheus_client import make_wsgi_app


import prometheus_client

prometheus_client.REGISTRY.unregister(prometheus_client.GC_COLLECTOR)
prometheus_client.REGISTRY.unregister(prometheus_client.PLATFORM_COLLECTOR)
prometheus_client.REGISTRY.unregister(prometheus_client.PROCESS_COLLECTOR)

app = Flask(__name__, static_url_path="", static_folder="../static")
app.config.from_object(__name__)
app.register_blueprint(bucket_blueprint, url_prefix="/api")
app.wsgi_app = DispatcherMiddleware(app.wsgi_app, {
    '/metrics': make_wsgi_app()
})
