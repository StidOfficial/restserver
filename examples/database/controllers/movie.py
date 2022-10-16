from restserver.controller import BaseController
from restserver.route import ControllerRoute, Get, Post, Put, Delete

@ControllerRoute("/movies")
class MovieController(BaseController):
  @Get
  def index(self):
    db = self.get_database()

    cur = db.cursor()

    cur.execute("SELECT * FROM movies")

    return cur.fetchall()

  @Post
  def create(self, movie: dict):
    db = self.get_database()

    cur = db.cursor()

    cur.execute("INSERT INTO movies(title, year, score) VALUES (?, ?, ?);",
                  (movie["title"], movie["year"], movie["score"]))

    db.commit()

    movie["id"] = cur.lastrowid

    self.created(movie, "application/json")

  def exists(self, id: int):
    db = self.get_database()

    cur = db.cursor()

    cur.execute("SELECT id FROM movies WHERE id = ?", id)

    return cur.fetchone()

  @Put(":id")
  def update(self, id: int, movie: dict):
    if id != movie["id"]:
      self.bad_request()
      return

    if not self.exists(id):
      self.not_found()
      return

    movie["id"] = id

    db = self.get_database()

    cur = db.cursor()

    cur.execute("UPDATE movies SET title = ?, year = ?, score = ? WHERE id = ?;",
                  (movie["title"], movie["year"], movie["score"], movie["id"]))

    db.commit()

    self.ok(movie, "application/json")

  @Delete(":id")
  def delete(self, id: int):
    if not self.exists(id):
      self.not_found()
      return

    db = self.get_database()

    cur = db.cursor()

    cur.execute("DELETE FROM movies WHERE id = ?;", id)

    db.commit()

    self.no_content()