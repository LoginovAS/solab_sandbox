from peewee import *
from playhouse.postgres_ext import *

psql_db = PostgresqlDatabase(
    'sandbox_db',
    user='sandbox',
    password='sandbox',
    host='127.0.0.1'
)

class PeeweeConnectionMiddleware(object):
    def __init__(self):
        pass

    def process_request(self, req, resp):
        psql_db.connect()

    def process_response(self, req, resp, resource):
        if not psql_db.is_closed():
            psql_db.close()

class BaseModel(Model):
    class Meta:
        database=psql_db

class GranulePolygon(BaseModel):
    product_id = CharField(null=True)
    visualizationparameter = CharField()
    polarization = CharField(null=True)
    granule_uid = CharField(null=True)
    granule_name = CharField()
    coords = ArrayField(IntegerField)
    user_id = CharField()
    add_date = DateField()
    date = DateField()
    tag_name = CharField()

    class Meta:
        db_table = 'granule_polygons'

def init_tables():
    psql_db.create_tables([GranulePolygon], safe=True)
