from apiclient import (
    APIClient,
    JsonRequestFormatter,
    JsonResponseHandler
)
import random



def seed_db_accounts(client):
    print('Creating some accounts...', end=' ')
    accounts = []

    for i in range(10):
        account = { 'id': str(i) }
        if i % 3 == 0:
            account['allowance'] = max(100, 100*i)

        client.add_account(account)
        accounts.append(account)

    print('Done')
    return accounts


def seed_db_offers(client, accounts):
    print('Creating some offers for accounts...', end=' ')
    offers = []

    price_range = (2, 40)
    services = ['dog walking', 'cleaning', 'computer repair', 'tailoring']
    goods = ['loaves of bread', 'carrots', 'pickles', 'bars of soap', 'candles']
    offer_types = [goods, services]

    for account in accounts:
        for i in range(5):
            offer_class = random.randint(0, 1)
            offer_type = random.choice(offer_types[offer_class])

            if offer_class == 0: # goods
                qty = random.randint(1, 10)
                description = f'{qty} {offer_type}'
                unit_price = random.randint(1, 5) # credits
                price = unit_price * qty # credits
            else: # service
                duration = random.randint(1, 4) # hours
                description = f'{duration} hours of {offer_type}'
                wage_rate = random.randint(15, 30) # credits/hour
                price = wage_rate * duration # credits


            offer = {
                'seller_id': account['id'],
                'description': description,
                'price': price,
                'title': offer_type
            }

            client.add_offer(offer)
            offers.append(offer)

    print('Done')
    return offers


def seed_db_pending_txs(client, accounts, offers):
    print('Creating new pending transactions...', end=' ')
    txs = []

    for i in range(len(accounts)):
        buyer = accounts[i]

        ''' Ad-hoc transactions '''
        if i % 7 == 0: # half of accounts make txs w/o offer
            for j in range(5):
                seller = None

                while seller is None:
                    _ = random.choice(accounts)
                    if _['id'] == buyer['id']: # can't buy from self
                        continue
                    seller = _

                amount = random.randint(1, 5) # anywhere from 1 to 5 of max

                tx = {
                    'buyer_id': buyer['id'],
                    'seller_id': seller['id'],
                    'amount': amount
                }
                client.add_transaction(tx)
                txs.append(tx)

        ''' Offer-based transactions '''
        for j in range(3): # init 3 txs by offer
            offer = None

            while offer is None:
                _ = random.choice(offers)
                if _['seller_id'] == buyer['id']: # can't buy from self
                    continue
                offer = _

            tx = {
                'buyer_id': buyer['id'],
                'seller_id': offer['seller_id'],
                'amount': offer['price']
            }
            client.add_transaction(tx)
            txs.append(tx)

    print('Done')
    return txs


def seed_db_approved_txs(client, txs):
    print('Approving some transactions...', end=' ')
    for tx in txs:
        client.approve_transaction(tx['id'])
    print('Done')


def seed_db_cancelled_txs(client, txs):
    print('Cancelling some transactions...', end=' ')
    for tx in txs:
        client.cancel_transaction(tx['id'])
    print('Done')


def seed_db_denied_txs(client, txs):
    print('Denying some transactions...', end=' ')
    for tx in txs:
        client.deny_transaction(tx['id'])
    print('Done')



class TestClient(APIClient):

    def __init__(self, base_url, *args, **kwargs):
        self.base_url = base_url
        super().__init__(
            request_formatter=JsonRequestFormatter,
            response_handler=JsonResponseHandler,
            *args, **kwargs)

    def _compose_url(self, path, params=None):
        if params is not None:
            params = dict((key, json.dumps(val))
                           for (key, val) in params.iteritems())
        return super()._compose_url(self, path, params=params)

    def add_account(self, account):
        url = self.base_url + '/accounts'
        self.post(url, data=account)

    def add_offer(self, offer):
        url = self.base_url + '/offers'
        self.post(url, data=offer)

    def add_transaction(self, tx):
        url = self.base_url + '/transactions'
        self.post(url, data=tx)

    def approve_transaction(self, tx_id):
        url = self.base_url + '/transactions'
        tx = { 'id': tx_id, 'action': 'approve' }
        self.put(url, tx)

    def get_transactions_all(self):
        url = self.base_url + '/transactions/all'
        return self.get(url)

    def cancel_transaction(self, tx_id):
        url = self.base_url + '/transactions'
        tx = { 'id': tx_id, 'action': 'cancel' }
        self.put(url, tx)

    def deny_transaction(self, tx_id):
        url = self.base_url + '/transactions'
        tx = { 'id': tx_id, 'action': 'deny' }
        self.put(url, tx)



if __name__ == '__main__':
    client = TestClient('http://127.0.0.1:5000/api/v1')

    accounts = seed_db_accounts(client)
    offers = seed_db_offers(client, accounts)
    txs_data = seed_db_pending_txs(client, accounts, offers)

    txs = client.get_transactions_all()

    one_fourth = int(len(txs)/4)
    approved_txs = txs[:one_fourth]
    cancelled_txs = txs[one_fourth:one_fourth*2]
    denied_txs = txs[one_fourth*2:one_fourth*3]
    pending_txs = txs[one_fourth*3:]

    seed_db_approved_txs(client, approved_txs)
    seed_db_cancelled_txs(client, cancelled_txs)
    seed_db_denied_txs(client, denied_txs)
