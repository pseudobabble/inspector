from marshmallow import Schema, fields

class RawDocument(Schema):
    """
    This class represents documents posted
    from external sources.
    """
    filename = fields.String()
    content = fields.String()

class MLDocument(Schema):
    """
    This class represents the data
    associated with a document in the
    pipeline document store
    """
    id = fields.UUID()
    document_id = fields.Integer()
    content = fields.String()
    content_type = fields.String()
    meta = fields.Dict()
    score = fields.Float()
    embedding = fields.Method('get_embedding')
    id_hash_keys = fields.Method('get_id_hash_keys')

    def get_embedding(self, obj):
        return str(list(obj))

    def get_id_hash_keys(self, obj):
        return str(obj)

class Document(Schema):
    """
    This class represents a
    Document
    """
    id = fields.Integer()
    filename = fields.String()
    raw_content = fields.String()
    content_hash = fields.String()
    ml_documents = fields.Nested(MLDocument)

class DocumentToPipeline(Schema):
    """
    This class converts Documents to
    the dict to post to the pipelines
    """
    document_id = fields.Method('get_document_id')
    content = fields.Method('get_content')
    content_type = fields.String(dump_default="text")

    def get_content(self, obj):
        return obj.raw_content

    def get_document_id(self, obj):
        return obj.id

class PipelineToMLDocument(Schema):
    """
    This class converts processed pipeline documents
    to MLDocument format data
    """
    id = fields.String()
    document_id = fields.Integer()
    content = fields.String()
    content_type = fields.String()
    meta = fields.Dict()
    # add embedded etc
