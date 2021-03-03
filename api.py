import db

import flask
from flask import request, jsonify, make_response
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


@app.route('/api/v1/accounts', methods=['GET'])
def accounts_filter():
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


@app.route('/api/v1/range', methods=['GET'])
def account_range():
    query_parameters = request.args

    id = query_parameters.get('id')

    query = 'SELECT max_balance, min_balance FROM accounts WHERE id=?'
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


@app.route('/api/v1/transactions', methods=['GET'])
def transactions_filter():
    pass
