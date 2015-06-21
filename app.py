from tornado import web, ioloop
from core.db.models import conn
from core.river_service import RiverService


class IndexHandler(web.RequestHandler):

    def get(self):
        with conn() as sess:
            rs = RiverService(_db_sess=sess)
            rivers = rs.find_rivers()
            self.render("index.html", rivers=rivers)


app = web.Application([
    (r'/', IndexHandler),
    (r'/(favicon.ico)', web.StaticFileHandler, {'path': '../'}),
    (r'/(rest_api_example.png)', web.StaticFileHandler, {'path': './'}),
])


if __name__ == '__main__':
    app.listen(8080)
    ioloop.IOLoop.instance().start()
