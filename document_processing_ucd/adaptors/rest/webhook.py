from __future__ import annotations

from typing import List

import requests
from resourceez.api_object import ApiObject


class Answer(ApiObject):
    index: int
    score: float
    snippet: str
    run_id: str


class AnswerClient:
    url = "http://172.17.0.1:42069/ans-hook"

    @classmethod
    def configure(cls, url=None) -> AnswerClient:
        if url is not None:
            cls.url = url
        return cls

    @classmethod
    def post(cls, answers: List[Answer]) -> None:
        requests.post(cls.url, json=[a.raw for a in answers])
