# Validations from Marshmallow
from marshmallow import Schema, fields
from marshmallow.validate import Regexp, Length, Range, OneOf


def load_data(transfer_db_obj):
    """ Load transfer's data

    Parameters:
    - Transfer db object
    """
    from app.models.schemas import TransferSchema

    transfer_schema = TransferSchema()

    data = transfer_schema.dump(transfer_db_obj)

    return data


class TransferCreateSchema(Schema):
    """ /transfer [POST]

    Parameters:
    - Receiver (Str)
    - Value (Int)
    - Memo (Str)
    """

    receiver = fields.Str(
        required=True,
        validate=[
            Length(min=4, max=15),
            Regexp(
                r"^([A-Za-z0-9_](?:(?:[A-Za-z0-9_]|(?:\.(?!\.))){0,28}(?:[A-Za-z0-9_]))?)$",
                error="Invalid username!",
            ),
        ],
    )
    value = fields.Int(required=True, validate=[Range(min=1)])
    memo = fields.Str(required=False, validate=[Length(max=128)])


class TransferGetSchema(Schema):
    """ /transfer [GET]

    Parameters:
    - Id (Int)
    """

    id = fields.Int(required=False, validate=[Range(min=1)])


class TransferSearchSchema(Schema):
    """ /transfer/search [POST]

    Parameters:
    - Id (Int)
    - Sender (Str)
    - Receiver (Str)
    - Status (Str)
    - Value (Int)
    - Memo (Str)
    """

    id = fields.Int(required=False, validate=[Range(min=1)])
    sender = fields.Str(
        required=False,
        validate=[
            Length(min=4, max=15),
            Regexp(
                r"^([A-Za-z0-9_](?:(?:[A-Za-z0-9_]|(?:\.(?!\.))){0,28}(?:[A-Za-z0-9_]))?)$",
                error="Invalid sender username!",
            ),
        ],
    )
    receiver = fields.Str(
        required=False,
        validate=[
            Length(min=4, max=15),
            Regexp(
                r"^([A-Za-z0-9_](?:(?:[A-Za-z0-9_]|(?:\.(?!\.))){0,28}(?:[A-Za-z0-9_]))?)$",
                error="Invalid receiver username!",
            ),
        ],
    )
    status = fields.Str(
        required=False,
        validate=[OneOf(['APPROVED', 'CANCELLED', 'DENIED', 'PENDING'])]
    )
    value = fields.Int(required=False, validate=[Range(min=1)])
    memo = fields.Str(required=False, validate=[Length(max=128)])



class TransferStatusUpdateSchema(Schema):
    """ /transfer [PUT]

    Parameters:
    - Id (Int)
    - Action (Str)
    """

    id = fields.Int(required=False, validate=[Range(min=1)])
    action = fields.Str(
        required=False,
        validate=[OneOf(['approve', 'cancel', 'deny'])]
    )
