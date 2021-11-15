from restserver.server import RESTServer
from restserver.handler import RESTHTTPRequestHandler

from controllers.test import TestController

with RESTServer(("", 8080), RESTHTTPRequestHandler) as httpd:
  print("Listen on :", httpd.server_address)

  httpd.add_controller(TestController)

  try:
    httpd.serve_forever()
  except KeyboardInterrupt:
    pass