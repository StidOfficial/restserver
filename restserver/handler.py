from http.server import BaseHTTPRequestHandler
from http import HTTPStatus

from restserver.response import Response
from restserver.utils import Utils

import traceback

class RESTHTTPRequestHandler(BaseHTTPRequestHandler):
  def do_response(self, response: Response) -> None:
    self.has_responded = True

    headers = response.get_headers()

    data = response.get_data()
    if data:
      headers["Content-Length"] = len(data)

    content_type = response.get_content_type()
    if content_type:
      headers["Content-Type"] = content_type

    self.send_response(response.get_status())
    for key, value in headers.items():
      self.send_header(key, value)
    self.end_headers()

    if data:
      self.wfile.write(data)

  def do_ok(self, content = None, content_type = None) -> None:
    self.do_response(Response(content, status=HTTPStatus.OK,
                      content_type=content_type))

  def do_bad_request(self, content = None, content_type = None) -> None:
    self.do_response(Response(content, status=HTTPStatus.BAD_REQUEST,
                      content_type=content_type))

  def do_not_found(self, content = None, content_type = None) -> None:
    self.do_response(Response(content, status=HTTPStatus.NOT_FOUND,
                      content_type=content_type))

  def do_internal_server_error(self, content = None, content_type = None) -> None:
    self.do_response(Response(content, status=HTTPStatus.INTERNAL_SERVER_ERROR,
                      content_type=content_type))

  def get_routes(self):
    from restserver.controller import BaseController
    from restserver.route import Route

    routes = []
    for controller in self.server.get_controllers():
      controller_class = controller.get_class()

      for route in dir(controller_class):
          # Ignore private and protected functions
          if route.startswith("_"):
            continue

          #method = Utils.get_method_by_route_name(route)
          route_attribute = getattr(controller_class, route)

          if isinstance(route_attribute, Route):
            route_template = controller.get_template() + "/" + route_attribute.get_template()
            routes.append(Route(method=route_attribute.get_method(),
                                template=route_template,
                                function=route_attribute.get_function(),
                                controller=controller_class))
    return routes

  def find_route(self, method: str):
    for route in self.get_routes():
      if method == route.get_method() and self.path == route.get_template():
        return route.get_controller(), route.get_function()

    return None, None

  def do_request(self, method: str):
    controller, func = self.find_route(method)
    if controller and func:
      Class = controller(self)
      response = func(Class)

      # Check if have already send a response
      if hasattr(self, "has_responded"):
        return

      try:
        if isinstance(response, Response):
          self.do_response(response)
        else:
          self.do_response(Response(response))
      except Exception as e:
        content = None
        content_type = None

        if Utils.is_development():
          content = {
            "exception": "%s: %s" % (type(e).__name__, str(e)),
            "stack": traceback.format_exc().split("\n")
          }
          content_type = "application/json"

          traceback.print_exception(type(e), e, e.__traceback__)

        self.do_internal_server_error(content, content_type)
    else:
      self.do_not_found()

  def do_GET(self):
    self.do_request("GET")

  def do_HEAD(self):
    self.do_request("HEAD")

  def do_POST(self):
    self.do_request("POST")

  def do_PUT(self):
    self.do_request("PUT")

  def do_DELETE(self):
    self.do_request("DELETE")

  def do_CONNECT(self):
    self.do_request("CONNECT")

  def do_OPTIONS(self):
    self.do_request("OPTIONS")

  def do_TRACE(self):
    self.do_request("TRACE")

  def do_PATCH(self):
    self.do_request("PATCH")