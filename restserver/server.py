from http.server import HTTPServer
from restserver.controller import BaseController

import array

class RESTServer(HTTPServer):
  def __init__(self, server_address, RequestHandlerClass, bind_and_activate=True):
    super().__init__(server_address, RequestHandlerClass, bind_and_activate)

    self._controllers = []

  def get_controllers(self) -> array:
    return self._controllers

  def add_controller(self, controller: BaseController) -> None:
    self._controllers.append(controller)