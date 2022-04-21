from flask import Flask
from flask_restful import Api

from infrastructure import repository
from document_processing import Documents, Trigger, Upload


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
api.add_resource(Trigger, *Trigger.routes)

if __name__ == '__main__':
    app.run(host="webapp", port=8080, debug=True)
