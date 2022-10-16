import restserver.server as server
from restserver.handler import RESTHTTPRequestHandler

from examples.database.controllers.movie import MovieController

import sqlite3

db = sqlite3.connect("database.db")

def dict_factory(cursor, row):
  col_names = [col[0] for col in cursor.description]
  return {key: value for key, value in zip(col_names, row)}

db.row_factory = dict_factory

cur = db.cursor()
cur.execute("""CREATE TABLE IF NOT EXISTS movies(
  id INTEGER PRIMARY KEY,
  title TEXT,
  year INTEGER,
  score INTEGER
);""")

db.commit()

with server.RESTServer(("", 8080), RESTHTTPRequestHandler) as httpd:
  print("Listen on :", httpd.server_address)

  httpd.add_database(db)

  httpd.add_controller(MovieController)

  try:
    httpd.serve_forever()
  except KeyboardInterrupt:
    pass

db.close()