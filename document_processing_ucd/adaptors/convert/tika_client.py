from dataclasses import dataclass

import requests


@dataclass
class TikaConnectionParams:
    host: str = 'localhost'
    port: str = '9998'


class TikaClient:

    def __init__(self, http_client = requests, connection_params: TikaConnectionParams = TikaConnectionParams()):
        self.http_client = http_client
        self.connection_params = connection_params
        self.content_types = {
            'pdf': 'application/pdf',
            'png': 'image/png',
            'jpg': 'image/jpg',
            'odt': 'application/vnd.oasis.opendocument.text',
            'doc': 'application/msword',
            'docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        }
        self.return_types = {
            'text': 'text/plain',
            'json': 'application/json'
        }

    def _convert(self, byte_buffer: bytes, content_type: str, accept: str):
        response = self.http_client.put(
            f'http://{self.connection_params.host}:{self.connection_params.port}/tika',
            data=byte_buffer,
            headers={
                'Content-Type': self.content_types[content_type],
                'Accept': self.return_types[accept]
            }
        )

        return response

    def convert_json(self, byte_buffer: bytes, content_type: str):
        response = self._convert(byte_buffer, content_type, 'json')

        return response.json()

    def convert_text(self, byte_buffer: bytes, content_type: str):
        response = self._convert(byte_buffer, content_type, 'text')

        return response.text
