import os
from flask import Flask
from flask_restful import Api

from infrastructure import repository
from document_processing import Documents, Upload

repository.create_all()

app = Flask(__name__)
api = Api(app)

api.add_resource(
    Documents,
    *Documents.routes
)
api.add_resource(Documents, "/documents/get_by_ids", endpoint="get_by_ids", methods=['GET'])
api.add_resource(Documents, "/documents/update_ml_documents", endpoint="update_ml_documents", methods=['PATCH'])
api.add_resource(Upload, *Upload.routes)
#api.add_resource(Trigger, *Trigger.routes)


_env = lambda init, key, default=None: init(os.getenv(key, default))
_env.__doc__ = """
A convenice function for expressing typed env config consistently

:param init: Callable, The constructor (usually type) of the env var.
:param key: str, The name of the env var.
:param default: The value to return if the env var is not set.
"""


if __name__ == '__main__':
    app.run(
        host=_env(str, "FLASK_HOST", default="webapp"),
        port=_env(int,"FLASK_PORT", default="8080"),
        debug=_env(bool,"FLASK_DEBUG", default=False),
    )
