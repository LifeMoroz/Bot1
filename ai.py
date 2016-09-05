from api import get, get_best_offer
from log import debug

LONGPOLLING_TIMEOUT = 25

DEFAULT_OP_COST = 120
RESOURCE_OP = {
    'Уголь': {
        'op': 1, 'buy_price': None, "dumping": False
    },
    'Бревно': {
        'op': 2, 'buy_price': None, "dumping": False
    },
    'Драг. руда': {
        'op': 4, 'buy_price': None, "dumping": False
    },
    'Руда': {
        'op': 3, 'buy_price': None, "dumping": True
    },
    'Хлопок': {
        'op': 1, 'buy_price': None, "dumping": False
    },
    'Шкура': {
        'op': 2, 'buy_price': None, "dumping": False
    },
    'Опилки': {
        'op': 1, 'buy_price': None, "dumping": False
    },
    'Драг. камни': {
        'op': 5, 'buy_price': None, "dumping": False
    },
}

MIN_OFFER = 100000



def go_to_trade_center():
    get("http://api.vircities.com/app/scripts/views/trade-center.js")
    get("http://api.vircities.com/app/scripts/templates/trade-center.tmpl")
    time.sleep(0.5)
    get("http://api.vircities.com/exchanges/items_groups_categories_business.json")
    get("http://api.vircities.com/exchanges/items_groups_categories.json")


def go_hospital():
    get("http://api.vircities.com/app/scripts/views/hospital.js")
    get("http://api.vircities.com/app/scripts/templates/hospital.tmpl")


def simulate():
    get("http://api.vircities.com/app/index.html")

    def long_polling():
        while True:
            requests.get("http://api.vircities.com/longpoll?startTime={}".format(int(time.time() * 1000)),
                         headers=HEADERS)
            time.sleep(LONGPOLLING_TIMEOUT)

    t = threading.Thread(target=long_polling)
    t.daemon = True
    t.start()

    time.sleep(1)
    go_to_trade_center()
    time.sleep(1)
    go_hospital()
    time.sleep(1)
    get("http://api.vircities.com/app/scripts/views/trade-center/items-buy-grouped.js")
    get("http://api.vircities.com/app/scripts/templates/trade-center/items-buy-grouped.tmpl")
    time.sleep(1.5)

def sell():
    pass


def check_resources(min_sum=MIN_OFFER):
    # TODO: dumping
    resource_offers = \
    get("http://api.vircities.com/exchanges/lots_by_type_user/resource.json", decode=True)[
        'exchanges']
    interesting_offers = {}
    debug("{:<13} {:5} {:8}".format("Type", "Buy", "BEST"))
    for resource in resource_offers.values():
        if RESOURCE_OP.get(resource['name']) is None:
            continue
        if RESOURCE_OP[resource['name']].get('buy_price') is not None:
            buy_price = RESOURCE_OP[resource['name']]['buy_price']
        else:
            buy_price = RESOURCE_OP[resource['name']]['op'] * DEFAULT_OP_COST
        best_offer = get_best_offer(resource['id'], min_sum=min_sum)
        if best_offer:
            best_offer_price = best_offer['price']
            debug("{:<13} {:5} {:8}".format(resource['name'], buy_price, best_offer_price))
            if buy_price >= float(best_offer_price):
                print(resource['name'], best_offer_price)
                interesting_offers[resource['id']] = buy_price
    return interesting_offers