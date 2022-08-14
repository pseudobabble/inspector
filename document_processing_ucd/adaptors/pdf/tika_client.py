import requests

class TikaClient:

    def __init__(self, http_client = requests):
        self.http_client = requests

    def convert(byte_buffer: bytes):
        response = self.http_client.put(
            'localhost:9998/tika',
            data=byte_buffer,
            headers={
                'Content-Type': 'application/pdf',
                'Accept': 'application/json'
            }
        )
