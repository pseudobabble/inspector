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
    embedding = fields.Method("get_embedding")
    id_hash_keys = fields.Method("get_id_hash_keys")

    def get_embedding(self, obj) -> str:
        return str(list(obj))

    def get_id_hash_keys(self, obj) -> str:
        return str(obj)


class Document(Schema):
    """
    This class represents a
    Document
    """

    id = fields.Integer()
    filename = fields.String()
    raw_content = fields.Method("get_raw_content", deserialize="load_raw_content")
    content_hash = fields.String()
    ml_documents = fields.Nested(MLDocument)

    def get_raw_content(self, obj) -> list:
        return list(obj.raw_content)

    def load_raw_content(self, value) -> bytes:
        return bytes(value)


class DocumentToPipeline(Schema):
    """
    This class converts Documents to
    the dict to post to the pipelines
    """

    filename = fields.String()
    document_id = fields.Method("get_document_id", deserialize="load_document_id")
    content = fields.Method("get_content", deserialize="load_content")
    content_type = fields.String(dump_default="text")

    def get_content(self, obj) -> list:
        """
        Serialize bytes by converting to a 'list':

            >>> b = b'some_bytes'
            >>> list(b)
            [115, 111, 109, 101, 95, 98, 121, 116, 101, 115]
            >>> bytes(list(b))
            b'some_bytes'

        """
        return list(obj.raw_content)

    def load_content(self, value):
        """Deserialize"""
        return bytes(value)

    def get_document_id(self, obj):
        """Serialize"""
        return obj.id

    def load_document_id(self, value):
        return value


class PipelineToMLDocument(Schema):
    """
    This class converts processed pipeline documents
    to MLDocument format data
    """

    id = fields.String()
    document_id = fields.Method("get_document_id", deserialize="load_document_id")
    content = fields.String()
    meta = fields.Dict()

    def get_document_id(self, obj):
        return obj["meta"]["document_id"]

    def load_document_id(self, value) -> str:
        return value
