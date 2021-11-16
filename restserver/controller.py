from restserver.handler import RESTHTTPRequestHandler

class BaseController:
  def __init__(self, handler: RESTHTTPRequestHandler):
    self._handler = handler

  def ok(self, content=None, content_type=None):
    self._handler.do_ok(content, content_type)

  def bad_request(self, content=None, content_type=None):
    self._handler.do_bad_request(content, content_type)

  def not_found(self, content=None, content_type=None):
    self._handler.do_not_found(content, content_type)

  def internal_server_error(self, content=None, content_type=None):
    self._handler.do_internal_server_error(content, content_type)