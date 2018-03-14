from peewee import *
from peewee import _BaseFormattedField
from playhouse.postgres_ext import *

import arrow

psql_db = PostgresqlDatabase(
    'sandbox_db',
    user='sandbox',
    password='sandbox',
    host='127.0.0.1'
)

def _date_part(date_part):
    def dec(self):
        return self.model_class._meta.database.extract_date(date_part, self)
    return dec

class ArrowField(_BaseFormattedField):
    db_field = 'datetime'
    formats = [
        '%Y-%m-%d %H:%M:%S.%f',
        '%Y-%m-%d %H:%M:%S',
        '%Y-%m-%d',
    ]

    def python_value(self, value):
        # if value and isinstance(value, basestring):
        #    return format_date_time(value, self.formats)
        return arrow.get(value)

    def db_value(self, value):
        if isinstance(value, arrow.arrow.Arrow):
            return value.to('UTC').naive
        else:
            return value

    year = property(_date_part('year'))
    month = property(_date_part('month'))
    day = property(_date_part('day'))
    hour = property(_date_part('hour'))
    minute = property(_date_part('minute'))
    second = property(_date_part('second'))

class PeeweeConnectionMiddleware(object):
    def __init__(self):
        pass

    def process_request(self, req, resp):
        psql_db.connect()

    def process_response(self, req, resp, resource):
        if not psql_db.is_closed():
            psql_db.close()

def init_tables():
    print("init_tables meshod creates tables")
    psql_db.create_tables([GranulePolygon, UserTag], safe=True)

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
    add_date = ArrowField()
    date = ArrowField()
    tag_name = CharField()

    class Meta:
        db_table = 'granule_polygons'

class UserTag(BaseModel):
    user_id = CharField()
    tag_name = CharField()

    class Meta:
        indexes = (
            (('user_id', 'tag_name'), True),
        )
        db_table = 'user_tags'
