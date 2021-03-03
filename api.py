import flask
from flask import request, jsonify, make_response
import sqlite3

app = flask.Flask(__name__)
app.config['DEBUG'] = True


db_file = 'credit_system.db'


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
    conn = sqlite3.connect(db_file)
    conn.row_factory = dict_factory
    cur = conn.cursor()
    query = 'SELECT * FROM accounts'
    all_accounts = cur.execute(query).fetchall()

    return make_response(jsonify(all_accounts), 200)


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

    conn = sqlite3.connect(db_file)
    conn.row_factory = dict_factory
    cur = conn.cursor()

    account = cur.execute(query, to_filter)

    return make_response(jsonify(account), 200)


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

    conn = sqlite3.connect(db_file)
    conn.row_factory = dict_factory
    cur = conn.cursor()

    result = cur.execute(query, to_filter).fetchone()

    return make_response(jsonify(account), 200)


@app.route('/api/v1/range', methods=['GET'])
def account_range():
    pass


@app.route('/api/v1/offers/all', methods=['GET'])
def offers_all():
    pass


@app.route('/api/v1/offers', methods=['GET'])
def offers_filter():
    pass


@app.route('/api/v1/transactions/all', methods=['GET'])
def transactions_all():
    pass


@app.route('/api/v1/transactions', methods=['GET'])
def transactions_filter():
    pass
