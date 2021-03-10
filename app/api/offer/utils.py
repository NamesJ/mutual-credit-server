# Validations from Marshmallow
from marshmallow import Schema, fields
from marshmallow.validate import Regexp, Length, Range, OneOf


def load_data(offer_db_obj):
    """ Load offer's data

    Parameters:
    - Offer db object
    """
    from app.models.schemas import OfferSchema

    offer_schema = OfferSchema()

    data = offer_schema.dump(offer_db_obj)

    return data



class OfferCreateSchema(Schema):
    """ /offer [POST]

    Parameters:
    - Title (Str)
    - Price (Int)
    - Description (Str)
    """

    title = fields.Str(required=False, validate=[Length(max=128)])
    price = fields.Int(validate=[Range(min=1)])
    description = fields.Str(required=False, validate=[Length(max=4000)])


class OfferDeleteSchema(Schema):
    """ /offer [DELETE]

    Parameters:
    - Id (Int)
    """

    id = fields.Int(required=True, validate=[Range(min=1)])


class OfferGetSchema(Schema):
    """ /offer [GET]

    Parameters:
    - Id (Int)
    """

    id = fields.Int(required=False, validate=[Range(min=1)])



class OfferUpdateSchema(Schema):
    """ /offer [PUT]

    Parameters:
    - Title (Str)
    - Price (Int)
    - Description (Str)
    """

    title = fields.Str(required=False, validate=[Length(max=128)])
    price = fields.Int(validate=[Range(min=1)])
    description = fields.Str(required=False, validate=[Length(max=4000)])
