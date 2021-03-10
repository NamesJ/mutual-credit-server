from datetime import datetime
from flask import current_app
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity

from app import db
from app.utils import get_user_by_id, err_resp, message, internal_err_resp
from app.models.user import User
from app.models.transfer import Transfer
from app.models.schemas import TransferSchema

transfer_schema = TransferSchema()


class TransferService:
    @staticmethod
    def create_transfer(data):
        ## Required values
        username = data['receiver'] # receiver username
        value = data['value']

        # Optional
        memo = data.get('memo', None)

        from .utils import load_data

        try:
            # Check if receiver user exists
            if not (receiver := User.query.filter_by(username=username).first()):
                return err_resp('Username does not exist', 'username_404', 404)

            # Get sender username by ID
            id = get_jwt_identity()

            # Get sender info
            if not (sender := User.query.filter_by(id=id).first()):
                return err_resp('Sender user does not exist', 'user_404', 404)

            # Check if receiver is the same username as sender (self-transact)
            if receiver.id == sender.id:
                return err_resp('Receiver is sender', 'username_404', 404)

            new_transfer = Transfer(
                sender=sender.id,
                receiver=receiver.id,
                value=value,
                memo=memo,
                status='PENDING',
                opened_on=datetime.utcnow(),
                closed_on=None,
            )

            db.session.add(new_transfer)
            db.session.flush()

            # Load the new transfer's info
            transfer_data = load_data(new_transfer)

            # Commit changes to DB
            db.session.commit()

            # return transfer data with usernames instead of ids
            resp = message(True, 'Transfer has been created.')
            resp['transfer'] = transfer_data
            resp['transfer']['sender'] = sender.username
            resp['transfer']['receiver'] = receiver.username
            return resp, 200

        except Exception as error:
            current_app.logger.error(error)
            return internal_err_resp()


    @staticmethod
    def get_transfer_data(data):
        ''' Get transfer data by ID '''
        transfer_id = data['id']

        from .utils import load_data

        try:

            # Check if transfer exists
            if not (transfer := Transfer.query.filter_by(id=transfer_id).first()):
                return err_resp('Transfer does not exist', 'transfer_404', 404)

            # Get sender user
            if not(sender := User.query.filter_by(id=transfer.sender).first()):
                return err_resp('Sender user does not exist', 'user_404', 404)

            # Get receiver user
            if not (receiver := User.query.filter_by(id=transfer.receiver).first()):
                return err_resp('Receiver user does not exist', 'user_404', 404)

            transfer_data = load_data(transfer)

            resp = message(True, 'Transfer data sent.')
            transfer_data['sender'] = sender.username
            transfer_data['receiver'] = receiver.username
            resp['transfer'] = transfer_data
            return resp, 200

        except Exception as error:
            print(error)
            return internal_err_resp()


    @staticmethod
    def search_transfers_data(data):
        ''' Get transfers data by attributes '''
        # Optional values
        id = data.get('id')
        sender = data.get('sender')
        receiver = data.get('receiver')
        status = data.get('status')
        value = data.get('value')
        memo = data.get('memo')

        if not (id or sender or receiver or status or value or memo):
            return err_resp('No valid search data provided', 'transfer_404', 404)

        # Convert `sender` user to User object
        if sender:
            if not (sender := User.query.filter_by(username=sender).first()):
                return err_resp('Sender does not exist', 'username_404', 404)

        # Convert `sender` user to User object
        if receiver:
            if not (receiver := User.query.filter_by(username=receiver).first()):
                return err_resp('Receiver does not exist', 'username_404', 404)

        search_data = {}
        if id: search_data['id'] = id
        if sender: search_data['sender'] = sender.id
        if receiver: search_data['receiver'] = receiver.id
        if status: search_data['status'] = status
        if value: search_data['value'] = value
        if memo: search_data['memo'] = memo

        transfers = Transfer.query.filter_by(**search_data).all()

        ## TODO (maybe): replace the user/ID swap loop below with an advanced query

        from .utils import load_data

        try:
            transfers_data = []

            for transfer in transfers:
                # Load data
                transfer_data = load_data(transfer)

                # replace user IDs with usernames in response data
                sender = User.query.filter_by(id=transfer.sender).first()
                receiver = User.query.filter_by(id=transfer.receiver).first()
                transfer_data.update({
                    'sender': sender.username,
                    'receiver': receiver.username
                })

                transfers_data.append(transfer_data)

            resp = message(True, 'Search succeeded')
            resp['transfers'] = transfers_data
            return resp, 200

        except Exception as error:
            current_app.logger.error(error)
            return internal_err_resp()


    @staticmethod
    def update_transfer_status(data):
        ''' Update transfer status by ID and action '''
        ## Required values
        transfer_id = data['id'] # receiver username
        action = data['action']

        id = get_jwt_identity()

        from .utils import load_data

        # Check if user exists
        if not (user := User.query.filter_by(id=id).first()):
            # It would be very strange if this error happened ;/
            return err_resp('User with calling ID does not exist', 'user_404', 404)

        # Check if transfer exists
        if not (transfer := Transfer.query.filter_by(id=transfer_id).first()):
            return err_resp('Transfer does not exist', 'id_404', 404)

        # Check if transfer status is 'PENDING' (only one that can change)
        if not transfer.status == 'PENDING':
            return err_resp(f'Transfer has status of {transfer.status}', 'status_404', 404)

        # Get sender user
        if not (sender := User.query.filter_by(id=transfer.sender).first()):
            return err_resp('User with sender ID of transfer does not exist', 'user_404', 404)

        # Get receiver user
        if not (receiver := User.query.filter_by(id=transfer.receiver).first()):
            return err_resp('User with receiver ID of transfer does not exist', 'user_404', 404)

        try:

            if action == 'approve':
                # Only the receiver can approve a pending transfer
                if id != receiver.id:
                    return err_resp('Only the receiver can approve a pending transfer', 'auth_404', 404)
                transfer.status = 'APPROVED'
                transfer.closed_on = datetime.utcnow()
                # Update balances for sender and receiver
                sender.balance = sender.balance - transfer.value
                receiver.balance = receiver.balance + transfer.value

            elif action == 'cancel':
                # Only the sender can cancel a pending transfer
                if id != sender.id:
                    return err_resp('Only the sender can cancel a pending transfer', 'auth_404', 404)
                transfer.status = 'CANCELLED'
                transfer.closed_on = datetime.utcnow()

            elif action == 'deny':
                # Only the receiver can deny a pending transfer
                if id != receiver.id:
                    return err_resp('Only the receiver can deny a pending transfer', 'auth_404', 404)
                transfer.status = 'DENIED'
                transfer.closed_on = datetime.utcnow()

            else:
                return err_resp('Invalid update action provided', 'status_404', 404)

            transfer_data = load_data(transfer)

            db.session.commit()

            resp = message(True, 'Status update succeeded.')
            transfer_data['sender'] = sender.username
            transfer_data['receiver'] = receiver.username
            resp['transfer'] = transfer_data
            return resp, 200

        except Exception as error:
            print(error)
            return internal_err_resp()
