import os

class Utils:
  @staticmethod
  def get_route_name_by_method(method: str) -> str:
    if method == "GET":
      return "index"
    elif method == "POST":
      return "create"
    elif method == "PUT":
      return "update"
    elif method == "DELETE":
      return "delete"
    else:
      return None

  @staticmethod
  def get_method_by_route_name(route_name: str) -> str:
    if route_name == "index":
      return "GET"
    elif route_name == "create":
      return "POST"
    elif route_name == "update":
      return "PUT"
    elif route_name == "delete":
      return "DELETE"
    else:
      return None

  @staticmethod
  def get_environment() -> str:
    return os.getenv("APP_ENVIRONMENT", "dev")

  @staticmethod
  def is_development() -> bool:
    return Utils.get_environment() == "dev"

  @staticmethod
  def is_production() -> bool:
    return Utils.get_environment() == "prod"