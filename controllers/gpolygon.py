from ujson import encode as json_dumps
from falcon import HTTP_200, HTTP_204, HTTP_404, HTTP_400, HTTPForbidden
from webargs import fields
from webargs.falconparser import use_args
from datetime import datetime

from models import *

class GPolygon(object):

    json_args = {
        'product_id': fields.Str(),
        'VisualizationParameter': fields.Str(),
        'polarization': fields.Str(),
        'granule_uid': fields.Str(),
        'granule_name': fields.Str(),
        'coords': fields.List(fields.Str()),
        'user_id': fields.Str(),
        'date': fields.Str(),
        'tag_name': fields.Str()
    }

    def gp_to_dict(gp):
        if gp.product_id is not None:
            product_id = gp.product_id
        else:
            product_id = None

        if gp.polarization is not None:
            polarization = gp.polarization
        else:
            polarization = None

        if gp.granule_uid is not None:
            granule_uid = gp.granule_uid
        else:
            granule_uid = None

        dc = {
            'product_id': product_id,
            'VisualizationParameter': gp.visualizationparameter,
            'polarization': polarization,
            'granule_uid': granule_uid,
            'granule_name': gp.granule_name,
            'coords': gp.coords,
            'user_id': gp.user_id,
            'add_date': gp.add_date,
            'date': gp.date,
            'tag_name':gp.tag_name
        }

        return dc

    @use_args(json_args, locations=('json',))
    def on_post(self, req, resp, args):
        print(args)
        add_date = datetime.now()
        date = args['date']

        user_id = args['user_id']
        tag_name = args['tag_name']

        # Create new entities:
        #   Create new Granule polygon record
        gp = GranulePolygon.create(
            visualizationparameter = args['VisualizationParameter'],
            polarization = args['polarization'],
            granule_name = args['granule_name'],
            coords = args['coords'],
            user_id = user_id,
            add_date = add_date,
            date = date,
            tag_name = tag_name
        )

        if (args.get('product_id') is not None):
            gp.product_id = args.get('product_id')
        if args.get('polarization') is not None:
            gp.polarization = args.get('polarization')
        if args.get(granule_uid) is not None:
            gp.granule_uid = agrs.get('granule_uid')

        #   Create new user tag record
        userTag = UserTag.create(
            user_id = user_id,
            tag_name = tag_name
        )

        # Save new entities
        gp.save()
        userTag.save()

        gp = gp_to_dict(gp)
        resp.status = HTTP_200
        resp.body = json_dumps(gp)
