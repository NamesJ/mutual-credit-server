from datetime import datetime
from flask import current_app
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity

from app import db
from app.utils import get_user_by_id, err_resp, message, internal_err_resp
from app.models.user import User
from app.models.offer import Offer
from app.models.schemas import OfferSchema

offer_schema = OfferSchema()


class OfferService:
    @staticmethod
    def create_offer(data):
        ''' Create offer '''

        title = data['title']
        price = data['price']
        description = data['description']

        from .utils import load_data

        try:
            # Get user's ID
            id = get_jwt_identity()

            # Get user info by ID (and check that user exists)
            if not (user := User.query.filter_by(id=id).first()):
                return err_resp('User with this ID does not exist', 'user_404', 404)

            new_offer = Offer(
                seller=user.username,
                title=title,
                price=price,
                description=description,
            )

            db.session.add(new_offer)
            db.session.flush()

            offer_data = load_data(offer)
            offer_data['seller'] = user.username

            db.session.commit()

            resp = message(True, 'Offer create succeeded.')
            resp['offer'] = offer_data
            return resp, 200

        except Exception as error:
            print(error)
            return internal_err_resp()


    @staticmethod
    def get_offer_data(data):
        ''' Get offer data by ID '''

        offer_id = data['id']

        from .utils import load_data

        try:
            # Get user's ID
            id = get_jwt_identity()

            # Get user info by ID (and check that user exists)
            if not (user := User.query.filter_by(id=id).first()):
                return err_resp('User with this ID does not exist', 'user_404', 404)

            # Check if offer exists
            if not (offer := Offer.query.filter_by(id=offer_id).first()):
                return err_resp('Offer does not exist', 'offer_404', 404)

            offer_data = load_data(offer)
            offer_data['seller'] = user.username

            resp = message(True, 'Offer data sent.')
            resp['offer'] = offer_data
            return resp, 200

        except Exception as error:
            print(error)
            return internal_err_resp()


    @staticmethod
    def update_offer_info(data):
        ''' Update offer info by ID '''

        # Required values
        offer_id = data['id']

        # Optional values
        title = data.get('title', None)
        price = data.get('price', None)
        description = data.get('description', None)

        from .utils import load_data

        try:
            # Check that at least one field was provided to update
            if not (title or price or description):
                return err_resp('No fields provided', 'nofields_404', 400)

            # Get user's ID
            id = get_jwt_identity()

            # Get user info by ID (and check that user exists)
            if not (user := User.query.filter_by(id=id).first()):
                return err_resp('User with this ID does not exist', 'user_404', 404)

            # Check if offer exists
            if not (offer := Offer.query.filter_by(id=offer_id).first()):
                return err_resp('Offer does not exist', 'offer_404', 404)

            # Check that user is the seller for this offer
            if offer.seller_id != seller.id:
                return err_resp('You can only edit your own offers', 'auth_404', 404)

            if title: offer.title = title
            if price: offer.price = price
            if description: offer.description = description

            db.session.commit()

            offer_data = load_data(offer)
            offer_data['seller'] = user.username

            resp = message(True, 'Offer update succeeded.')
            resp['offer'] = offer_data
            return resp, 200

        except Exception as error:
            except Exception as error:
                print(error)
                return internal_err_resp()
