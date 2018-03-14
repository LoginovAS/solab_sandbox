import falcon

from controllers.gpolygon import GPolygon
from models import PeeweeConnectionMiddleware
from models import init_tables

app = falcon.API([PeeweeConnectionMiddleware()])

init_tables()

gp = GPolygon()

app.add_route('/gp', gp)
