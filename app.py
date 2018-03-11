import falcon

from controllers.GranulePolygon import GranulePolygonController
from models import PeeweeConnectionMiddleware

dbConfig = ""

app = falcon.API([PeeweeConnectionMiddleware(dbConfig)])

gp = GranulePolygonController()

app.add_route('/gp', gp)
