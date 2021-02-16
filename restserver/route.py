from restserver.utils import Utils

class ControllerRoute:
  def __init__(self, template: str):
    self._template = template

  def get_template(self) -> str:
    return self._template

  def get_class(self):
    return self._class

  def __call__(self, Class):
    self._class = Class
    return self

class Route:
  def __init__(self, method: str, template: str, function = None, controller = None):
    self._method = method
    if callable(template):
      self._function = template

      route_name = Utils.get_route_name_by_method(method)
      if route_name == template.__name__:
        self._template = ""
      else:
        self._template = template.__name__
    else:
      self._template = template
      self._function = function
    self._controller = controller

  def get_method(self) -> str:
    return self._method

  def get_template(self) -> str:
    return self._template

  def get_function(self):
    return self._function

  def get_controller(self):
    return self._controller

  def __call__(self, function):
    self._function = function
    return self

class Get(Route):
  def __init__(self, template: str):
    super().__init__("GET", template)

class Post(Route):
  def __init__(self, template: str):
    super().__init__("POST", template)

class Put(Route):
  def __init__(self, template: str):
    super().__init__("PUT", template)

class Delete(Route):
  def __init__(self, template: str):
    super().__init__("DELETE", template)