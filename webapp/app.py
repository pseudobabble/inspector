from logging import config

from flask import Flask
from flask_restful import Api

from document_processing import utils
from document_processing.resources import AnswerHook, Documents, Upload, UserQuery
from infrastructure import repository

# TODO: Move this and any other configuration to its own package.
config.dictConfig(
    {
        "version": 1,
        "root": {"handlers": ["console"], "level": "DEBUG"},
        "handlers": {
            "console": {
                "formatter": "std_out",
                "class": "logging.StreamHandler",
                "level": "DEBUG",
            }
        },
        "formatters": {
            "std_out": {
                "format": "%(asctime)s : %(levelname)s : %(module)s : %(funcName)s : %(message)s",
                "datefmt": "%d-%m-%Y %I:%M:%S",
            }
        },
    }
)


repository.create_all()

app = Flask(__name__)
api = Api(app)


# Routing
api.add_resource(Documents, *Documents.routes)
api.add_resource(
    Documents, "/documents/get_by_ids", endpoint="get_by_ids", methods=["GET"]
)
api.add_resource(
    Documents,
    "/documents/update_ml_documents",
    endpoint="update_ml_documents",
    methods=["PATCH"],
)
api.add_resource(Upload, *Upload.routes)
api.add_resource(AnswerHook, *AnswerHook.routes, methods=["POST"])
api.add_resource(UserQuery, *UserQuery.routes, methods=["POST", "GET"])


# Run the flask app
if __name__ == "__main__":
    app.run(
        host=utils.env(str, "FLASK_HOST", default="webapp"),
        port=utils.env(int, "FLASK_PORT", default="8080"),
        debug=utils.env(bool, "FLASK_DEBUG", default=False),
    )
