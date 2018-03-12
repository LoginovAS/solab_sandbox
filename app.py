import falcon

from controllers.gpolygon import GPolygon
from models import PeeweeConnectionMiddleware

app = falcon.API([PeeweeConnectionMiddleware()])

gp = GPolygon()

app.add_route('/gp', gp)
