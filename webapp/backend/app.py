from flask import Flask
from flask_restful import Api

from infrastructure import repository
from document_processing import Documents, Trigger


repository.create_all()

app = Flask(__name__)
api = Api(app)

api.add_resource(
    Documents,
    *Documents.routes
)
api.add_resource(Trigger, *Trigger.routes)

if __name__ == '__main__':
    app.run(host="webapp", port=8080, debug=True)
