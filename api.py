import db

import flask
from flask import request, jsonify, make_response
import time
from uuid import uuid4


app = flask.Flask(__name__)
app.config['DEBUG'] = True


def dict_factory(cursor, row):
    d = {}

    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]

    return d


@app.errorhandler(404)
def page_not_found(e):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.route('/', methods=['GET'])
def home():
    return '''<h1>Mutual Credit System</h1>
<p>API for mutual credit system</p>'''


@app.route('/api/v1/accounts/all', methods=['GET'])
def accounts_all():
    with db.connect() as conn:
        conn.row_factory = dict_factory
        cur = conn.cursor()
        query = 'SELECT * FROM accounts'
        results = cur.execute(query).fetchall()

    return make_response(jsonify(results), 200)


@app.route('/api/v1/accounts', methods=['GET', 'POST'])
def accounts_filter():
    if request.method == 'GET':
        query_parameters = request.args

        id = query_parameters.get('id')

        query = 'SELECT * FROM accounts WHERE id=?'
        to_filter = []

        if id:
            to_filter.append(id)
        if not id:
            return page_not_found(404)

        with db.connect() as conn:
            conn.row_factory = dict_factory
            cur = conn.cursor()
            result = cur.execute(query, to_filter).fetchone()

        return jsonify(result)
    else:
        data = request.get_json()

        try:
            id = data['id']
            #balance = data['balance']
        except KeyError:
            return make_response(400)

        try:
            allowance = int(data['allowance'])
        except KeyError:
            allowance = 100


        #id = uuid4().hex
        account = (id, 0, allowance)

        query = ''' INSERT INTO accounts(
                        id,
                        balance,
                        allowance)
                    VALUES (?, ?, ?)'''

        with db.connect() as conn:
            conn.execute(query, account)

        return make_response(jsonify('Success'), 200)


@app.route('/api/v1/balance', methods=['GET'])
def account_balance():
    query_parameters = request.args

    id = query_parameters.get('id')

    query = 'SELECT balance FROM accounts WHERE id=?'
    to_filter = []

    if id:
        to_filter.append(id)
    if not id:
        return page_not_found(404)

    with db.connect() as conn:
        conn.row_factory = dict_factory
        cur = conn.cursor()
        result = cur.execute(query, to_filter).fetchone()

    return jsonify(result)


@app.route('/api/v1/allowance', methods=['GET'])
def account_range():
    query_parameters = request.args

    id = query_parameters.get('id')

    query = 'SELECT allowance FROM accounts WHERE id=?'
    to_filter = []

    if id:
        to_filter.append(id)
    if not id:
        return page_not_found(404)

    with db.connect() as conn:
        conn.row_factory = dict_factory
        cur = conn.cursor()
        result = cur.execute(query, to_filter).fetchone()

    return jsonify(result)


@app.route('/api/v1/offers/all', methods=['GET'])
def offers_all():
    with db.connect() as conn:
        conn.row_factory = dict_factory
        cur = conn.cursor()
        query = 'SELECT * FROM offers'
        results = cur.execute(query).fetchall()

    return jsonify(results)


@app.route('/api/v1/offers', methods=['GET', 'POST'])
def offers_filter():
    if request.method == 'GET':
        query_parameters = request.args

        id = query_parameters.get('id')
        seller_id = query_parameters.get('seller_id')

        query = 'SELECT * FROM offers WHERE'
        to_filter = []

        if id:
            query += ' id=? AND'
            to_filter.append(id)
        if seller_id:
            query += ' seller_id=? AND'
            to_filter.append(seller_id)
        if not (id or seller_id):
            return page_not_found(404)

        query = query[:-4] + ';'

        with db.connect() as conn:
            conn.row_factory = dict_factory
            cur = conn.cursor()
            results = cur.execute(query, to_filter).fetchall()

        return jsonify(results)
    else:
        data = request.get_json()

        try:
            seller_id = data['seller_id']
            description = data['description']
            price = int(data['price'])
            title = data['title']
        except AttributeError:
            return make_response(400)

        id = uuid4().hex
        offer = (id, seller_id, description, price, title)

        query = ''' INSERT INTO offers(
                        id,
                        seller_id,
                        description,
                        price,
                        title)
                    VALUES (?, ?, ?, ?, ?)'''

        with db.connect() as conn:
            conn.execute(query, offer)

        return make_response(jsonify('Success'), 200)


@app.route('/api/v1/transactions/all', methods=['GET'])
def transactions_all():
    with db.connect() as conn:
        conn.row_factory = dict_factory
        cur = conn.cursor()
        query = 'SELECT * FROM transactions'
        results = cur.execute(query).fetchall()

    return jsonify(results)


@app.route('/api/v1/transactions', methods=['GET', 'POST', 'PUT'])
def transactions():
    if request.method == 'GET':
        query_parameters = request.args

        id = query_parameters.get('id')
        buyer_id = query_parameters.get('buyer_id')
        offer_id = query_parameters.get('offer_id')
        status = query_parameters.get('status')
        start_timestamp = query_parameters.get('start_timestamp')
        end_timestamp = query_parameters.get('end_timestamp')

        query = 'SELECT * FROM transactions WHERE'
        to_filter = []

        if id:
            query += ' id=? AND'
            to_filter.append(id)
        if buyer_id:
            query += ' seller_id=? AND'
            to_filter.append(buyer_id)
        if offer_id:
            query += ' offer_id=? AND'
            to_filter.append(offer_id)
        if status:
            query += ' status=? AND'
            to_filter.append(status)
        if start_timestamp:
            query += ' start_timestamp=? AND'
            to_filter.append(start_timestamp)
        if end_timestamp:
            query += ' end_timestamp=? AND'
            to_filter.append(buyer_id)
        if not (id or buyer_id or offer_id or status or start_timestamp or
                end_timestamp):
            return page_not_found(404)

        query = query[:-4] + ';'

        with db.connect() as conn:
            conn.row_factory = dict_factory
            cur = conn.cursor()
            results = cur.execute(query, to_filter).fetchall()

        return jsonify(results)
    elif request.method == 'POST':
        data = request.get_json()

        try:
            buyer_id = data['buyer_id']
            offer_id = data['offer_id']
            #status = int(data['status'])
            #start_timestamp = data['start_timestamp']
            #end_timestamp = data['end_timestamp']
        except AttributeError:
            return make_response(400)

        id = uuid4().hex
        tx = (id, buyer_id, offer_id, 'PENDING', int(time.time()), None)

        query = ''' INSERT INTO transactions(
                        id,
                        buyer_id,
                        offer_id,
                        status,
                        start_timestamp,
                        end_timestamp)
                    VALUES (?, ?, ?, ?, ?, ?)'''

        with db.connect() as conn:
            conn.execute(query, tx)

        return make_response(jsonify('Success'), 200)
    else: # request.method == 'PUT'
        pass
