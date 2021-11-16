from http import HTTPStatus

import json

class Response:
    def __init__(self, content = None, headers: dict = None, status: int = HTTPStatus.OK, content_type = "application/json"):
        if headers is None:
          headers = {}

        self._content = content
        self._headers = headers
        self._status = status
        self._content_type = content_type

    def get_headers(self) -> dict:
      return self._headers

    def get_status(self) -> int:
      return self._status

    def get_content_type(self) -> str:
      return self._content_type

    def get_data(self) -> bytes:
      if self._content is None:
        return None

      if self._content_type == "application/json":
        return json.dumps(self._content).encode()

      if isinstance(self._content, str):
        return self._content.encode()
      elif isinstance(self._content, bytes):
        return self._content
      else:
        raise Exception(f"Unsupported content format ({self._content_type}/{type(self._content)})")