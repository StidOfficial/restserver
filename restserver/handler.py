from http.server import BaseHTTPRequestHandler
from http import HTTPStatus

from restserver.response import Response
from restserver.utils import Utils
from restserver.exceptions import InvalidContentTypeError

import traceback
import re
from typing import Callable, Type
from inspect import signature
import json

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

  def do_created(self, content = None, content_type = None) -> None:
    self.do_response(Response(content, status=HTTPStatus.CREATED,
                      content_type=content_type))

  def do_no_content(self, content = None, content_type = None) -> None:
    self.do_response(Response(content, status=HTTPStatus.NO_CONTENT,
                      content_type=content_type))

  def do_bad_request(self, content = None, content_type = None) -> None:
    self.do_response(Response(content, status=HTTPStatus.BAD_REQUEST,
                      content_type=content_type))

  def do_not_found(self, content = None, content_type = None) -> None:
    self.do_response(Response(content, status=HTTPStatus.NOT_FOUND,
                      content_type=content_type))

  def do_unsupported_media_type(self, content = None, content_type = None) -> None:
    self.do_response(Response(content, status=HTTPStatus.UNSUPPORTED_MEDIA_TYPE,
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
            route_template = controller.get_template()
            if route_attribute.get_template():
              route_template += "/" + route_attribute.get_template()

            routes.append(Route(method=route_attribute.get_method(),
                                template=route_template,
                                function=route_attribute.get_function(),
                                controller=controller_class))
    return routes

  def find_route(self, method: str):
    for route in self.get_routes():
      if method != route.get_method():
        continue

      route_template = route.get_template()

      route_param_names = re.findall(r":([a-zA-Z]+)", route_template)

      for route_param_name in route_param_names:
        route_template = route_template.replace(f":{route_param_name}", rf"(?P<{route_param_name}>[a-zA-Z0-9_-]+)")

      route_template = f"^{route_template}$"

      result = re.match(route_template, self.path)
      if result is None:
        continue

      route_params = result.groupdict()

      return route.get_controller(), route.get_function(), route_params

    return None, None, None

  def get_route_arguments(self, controller_class: Type, params: dict, func: Callable):
    args = {}

    for k, v in signature(func).parameters.items():
      if k == "self":
        args[k] = controller_class
      elif k in params:
        args[k] = params[k]
      else:
        args[k] = None

    return args

  def get_content(self):
    if "Content-Length" not in self.headers or "Content-Type" not in self.headers:
      return None

    content_length = int(self.headers["Content-Length"])
    content_type = self.headers["Content-Type"]

    if content_length <= 0:
      return None

    if content_type == "application/json":
      return json.loads(self.rfile.read(content_length))
    else:
      raise InvalidContentTypeError(f"Unsupported type {content_type}")

  def do_request(self, method: str):
    controller, func, params = self.find_route(method)
    if controller and func:
      controller_class = controller(self)

      args = self.get_route_arguments(controller_class, params, func)

      try:
        for k, v in args.items():
          if v is None:
            args[k] = self.get_content()
            break
      except InvalidContentTypeError as e:
        self.do_unsupported_media_type()
        return

      response = func(*args.values())

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