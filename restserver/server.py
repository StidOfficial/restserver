from http.server import HTTPServer
from restserver.controller import BaseController
from restserver.handler import RESTHTTPRequestHandler

import array

class RESTServer(HTTPServer):
  def __init__(self, server_address: str, RequestHandlerClass: RESTHTTPRequestHandler,
                bind_and_activate: bool = True) -> None:
    super().__init__(server_address, RequestHandlerClass, bind_and_activate)

    self._controllers = []
    self._databases = {}

  def get_controllers(self) -> array:
    return self._controllers

  def add_controller(self, controller: BaseController) -> None:
    self._controllers.append(controller)

  def get_database(self, name = "default") -> object:
    return self._databases[name]

  def add_database(self, database, name = "default") -> None:
    self._databases[name] = database