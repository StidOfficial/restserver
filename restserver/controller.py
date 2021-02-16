from restserver.handler import RESTHTTPRequestHandler

class BaseController:
  def __init__(self, handler: RESTHTTPRequestHandler):
    self._handler = handler

  def not_found(self):
    self._handler.do_not_found()