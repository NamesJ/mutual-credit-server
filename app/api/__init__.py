from flask_restx import Api
from flask import Blueprint

from .offer.controller import api as offer_ns
from .transfer.controller import api as transfer_ns
from .user.controller import api as user_ns

# Import controller APIs as namespaces.
api_bp = Blueprint("api", __name__)

api = Api(api_bp, title="API", description="Main routes.")

# API namespaces
api.add_namespace(offer_ns)
api.add_namespace(transfer_ns)
api.add_namespace(user_ns)
