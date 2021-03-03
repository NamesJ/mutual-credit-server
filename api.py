import flask
from flask import request, jsonify, make_response

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
    pass


@app.route('/api/v1/accounts', methods=['GET'])
def accounts_filter():
    pass


@app.route('/api/v1/balance', methods=['GET'])
def account_balance():
    pass


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
