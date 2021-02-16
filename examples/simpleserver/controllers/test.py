from restserver.controller import BaseController
from restserver.route import ControllerRoute, Get, Post, Put, Delete

@ControllerRoute("/test")
class TestController(BaseController):
  @Get
  def index(self):
    #self.not_found()
    return "hello"

  @Get
  def test(self):
    return "ok"

  @Get("ok")
  def lol(self):
    return "lol"

  @Post
  def create(self):
    pass

  @Put
  def update(self):
    pass

  @Delete
  def delete(self):
    pass