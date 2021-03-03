import db
from api import app


def init_db():
    with db.connect() as conn:
        db.init_accounts_table(conn)
        db.init_offers_table(conn)
        db.init_offer_categories_table(conn)
        db.init_transactions_table(conn)


if __name__ == '__main__':
    init_db()
    app.run()
