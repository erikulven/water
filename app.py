from tornado import web, ioloop
from core.db.models import conn
from core.river_service import RiverService


class IndexHandler(web.RequestHandler):

    def get(self):
        with conn() as sess:
            rs = RiverService(_db_sess=sess)
            rivers = rs.find_rivers()
            self.render("index.html", rivers=rivers, start=0, rows=100)


class MeasureHandler(web.RequestHandler):

    def get(self):
        with conn() as sess:
            rs = RiverService(_db_sess=sess)
            start = self.get_query_argument('start', 0)
            rows = self.get_query_argument('rows', 100)
            river_id = self.get_query_argument('river_id')
            river = rs.get_river(river_id=river_id)
            measures = rs.find_measures(river_id, start=start, rows=rows)
            self.render("measures.html", river=river, measures=measures,
                        start=start, rows=rows)


app = web.Application([
    (r'/', IndexHandler),
    (r'/measures', MeasureHandler),
    (r'/(favicon.ico)', web.StaticFileHandler, {'path': '../'}),
    (r'/(rest_api_example.png)', web.StaticFileHandler, {'path': './'}),
])


if __name__ == '__main__':
    app.listen(8080)
    ioloop.IOLoop.instance().start()
