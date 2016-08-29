# encoding": "utf-8
import threading

import requests
import json

import time

HEADERS = {
    "Host": "api.vircities.com",
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0",
    "Accept" "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
    "Accept-Language": "ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3",
    "Accept-Encoding": "gzip, deflate",
    "Content-Type": "application/x-www-form-urlencoded",
    "Referer": "http://api.vircities.com/app/index.html",
    "Cookie": "__cfduid=d8043380e229f3261673456376450dac31471467230; _ym_uid=1471467228187734207; _ga=GA1.2.1615719236.1471467228; __utma=94353562.1615719236.1471467228.1471467229.1471553673.2; __utmz=94353562.1471553673.2.2.utmcsr=yandex|utmccn=(organic)|utmcmd=organic; _ga=GA1.1.1615719236.1471467228; CAKEPHP=c70o8tusk3nad5ls75t40cdka5; CakeCookie[lang]=rus; _gat=1"
}

POST_HEADERS = {
    "Host": "api.vircities.com",
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3",
    "Accept-Encoding": "gzip, deflate",
    "Content-Type": "application/x-www-form-urlencoded",
    "Referer: http": "//api.vircities.com/app/index.html",
    "Cookie:": "__cfduid=d8043380e229f3261673456376450dac31471467230; _ym_uid=1471467228187734207; _ga=GA1.2.1615719236.1471467228; __utma=94353562.1615719236.1471467228.1471467229.1471553673.2; __utmz=94353562.1471553673.2.2.utmcsr=yandex|utmccn=(organic)|utmcmd=organic; _ga=GA1.1.1615719236.1471467228; CAKEPHP=c70o8tusk3nad5ls75t40cdka5; CakeCookie[lang]=rus; _gat=1",
    "Connection": "keep-alive",
}

LONGPOLLING_TIMEOUT = 25
MENU_ITEMS = ["armorHead", "armorLegs", "armorBoots", "armorBody", "closeRangeWeapon"]
JUMMY_MSET = [("armorHead", "JimmySet Helmet", 1),
              ("armorLegs", "JimmySet Pants", 1),
              ("armorBoots", "JimmySet Boots", 1),
              ("armorBody", "JimmySet Vest", 1),
              ("closeRangeWeapon", "Jimmy medium", 2)
              ]
JUMMY_MSET1 = [("armorHead", "JimmySet Helmet", 1),
               ("armorLegs", "JimmySet Pants", 1),
               ("armorBoots", "JimmySet Boots", 1),
               ("armorBody", "JimmySet Vest", 1),
               ("closeRangeWeapon", "Justice Ring ", 4)
               ]
JUMMY_MSET1_ITEMS = [x[1] for x in JUMMY_MSET1]
JUMMY_MSET_ITEMS = [x[1] for x in JUMMY_MSET]

JUMMY_LSET = [("armorHead", "JimmySet Helmet", 1),
              ("armorLegs", "JimmySet Pants", 1),
              ("armorBoots", "JimmySet Boots", 1),
              ("armorBody", "JimmySet Vest", 1),
              ("closeRangeWeapon", "Jimmy lite", 2)
              ]
JUMMY_LSET_ITEMS = [x[1] for x in JUMMY_LSET]

FITTABLE_TYPES = ['clothes', 'ammunition', 'weapon']

CLOSE_WEAPON = 'closeRangeWeapon'  # close weapon

DEFAULT_OP_COST = 105
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

DEBUG_LOG = open("log", 'a', encoding='UTF-8')
DEBUG_LOG.write("*" * 16 + "NEW CYCLE" + "*" * 16 + "\n")


class RequestError(Exception):
    pass


class NoEnergyError(Exception):
    pass


def debug(*args):
    print(*args, file=DEBUG_LOG)


def warn(*args):
    print(*args)
    debug(*args)


def get(url, decode=False):
    data = json.loads(requests.get(url, headers=HEADERS).content.decode("utf-8"))
    if data.get('setFlash') and data['setFlash'][0]['class'] != 'flash_success':
        warn(data)
        raise RequestError
    if decode:
        return data


def post(url, data, decode=False):
    data = json.loads(requests.post(url, headers=POST_HEADERS, data=data).content.decode("utf-8"))
    if data.get('setFlash') and data['setFlash'][0]['class'] != 'flash_success':
        warn(data)
        raise RequestError
    if decode:
        return data


def buy(item_id, number=1):
    post("http://api.vircities.com/exchanges/user_buy.json?os=unknown&v=3.00",
         {"data[Exchange][id]": item_id, "data[Exchange][number]": number, "data[Corporation][id]": 0}, decode=True)


def put(item_id, slot):
    post("http://api.vircities.com/user_items/put_item_on.json?os=unknown&v=3.00",
         {"data[UserItem][id]": item_id, "data[UserItem][slot_id]": slot})


def go_to_trade_center():
    get("http://api.vircities.com/app/scripts/views/trade-center.js")
    get("http://api.vircities.com/app/scripts/templates/trade-center.tmpl")
    time.sleep(0.5)
    get("http://api.vircities.com/exchanges/items_groups_categories_business.json?os=unknown&v=3.00")
    get("http://api.vircities.com/exchanges/items_groups_categories.json?os=unknown&v=3.00")


def go_hospital():
    get("http://api.vircities.com/app/scripts/views/hospital.js")
    get("http://api.vircities.com/app/scripts/templates/hospital.tmpl")


def get_short_info():
    return get("http://api.vircities.com/users/short_infos.json?os=unknown&v=3.00", decode=True)['user']['User']


def get_item_id(type, name):
    heads = get("http://api.vircities.com/exchanges/lots_by_type_user/{type}.json?os=unknown&v=3.00".format(type=type),
                decode=True)['exchanges']
    myheads = [x for x in heads.values() if x['name'] == name]
    return myheads[0]['id'] if myheads else None


def get_best_offers(item_id, min_n=0, min_sum=0):
    try:
        offers = get("http://api.vircities.com/exchanges/lot_offers/vdollars/{head_id}/price/asc.json?os".format(head_id=item_id),
            decode=True)['offers']
    except RequestError:
        warn("No such items")
        return []
    offers = [of for of in offers if
              float(of['number']) >= min_n and float(of['price']) * float(of['number']) >= min_sum]
    return sorted(offers, key=lambda k: float(k['price']))


def get_best_offer(item_id, min_n=0, min_sum=0):
    offers = get_best_offers(item_id, min_n, min_sum)
    if offers:
        return offers[0]


def buy_set(items):
    spend = 0
    for type, name, value in items:  # {'infos': {'user_id': 63563, 'lang': 'ru', 'city_id': 3}, 'inFightInfo': None, 'userLevel': 35, 'title_for_layout': 'LifeMoroz, VirCities - город твоей мечты', 'userContext': {'male   ': True, 'username': 'LifeMoroz'}, 'userId': 63563, 'error': 1, 'currentLevel': 35, 'setFlash': [{'msg': 'Столько нет на складе у продавца', 'class': 'flash_error'}], 'locale': 'rus'}
        item_id = get_item_id(type, name)
        offer = get_best_offer(item_id)
        if not offer:
            return 0
        bought = 0
        while bought < value:
            _buy = offer['number'] if offer['number'] < value else value
            debug("WTB: {} x{}".format(name, _buy))
            buy(offer['id'], _buy)
            bought += _buy
        spend += float(offer['price'])
        time.sleep(1)
    return spend


class ItemType(object):
    def __init__(self, id, name, category_id, item_class):
        self.id = id
        self.name = name
        self.c_id = category_id
        self.slot_name = '_'.join(item_class.split('_')[:-1]) + "_inventory" if item_class else ""

    @staticmethod
    def get_from_dict(d):
        return ItemType(d['id'], d['name'], d['category_id'], d['class'])


class Item(object):
    WEAPONS = {  # Inventory class
        "first": None,
        "second": None
    }

    def __init__(self, id, type, quantity, slot):
        self.id = id
        self.type = type
        self.quantity = quantity
        self.slot = slot

    def buy(self, number):
        buy(self.id, number)

    def put(self, slot):
        if self.slot:
            return

        # Second weapon hack
        if slot == CLOSE_WEAPON:
            if self.WEAPONS['first']:
                if self.WEAPONS['second']:
                    return
                self.type.slot_name = self.type.slot_name.replace("first", "second")
            self.WEAPONS[self.type.slot_name.split("_")[0]] = self

        if self.type.slot_name:
            put(self.id, self.type.slot_name)
        else:
            warn("Smth wrong")
            raise Exception
        self.slot = self.type.slot_name

        debug("Put on: ", self.slot)

    @staticmethod
    def clear():
        Item.WEAPONS = {  # Inventory class
            "first": None,
            "second": None
        }


def get_storage():
    get("http://api.vircities.com/users/short_infos.json?os=unknown&v=3.00")
    storage_json = get("http://api.vircities.com/user_items/storage.json?os=unknown&v=3.00", decode=True)['storage']
    item_types = storage_json['itemTypes']
    items = storage_json['itemsArray']
    item_arr = []
    for i in items:
        it = i['UserItem']
        ttype = ItemType.get_from_dict(item_types[str(it['item_type_id'])])
        item = Item(it['id'], ttype, it['quantity'], it['equipped_slot'])
        item_arr.append(item)
    return item_arr


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

    time.sleep(1.5)
    go_to_trade_center()
    time.sleep(1.5)
    go_hospital()
    time.sleep(1.5)
    get("http://api.vircities.com/app/scripts/views/trade-center/items-buy-grouped.js")
    get("http://api.vircities.com/app/scripts/templates/trade-center/items-buy-grouped.tmpl")
    time.sleep(1.5)


def heal(hp=True, t=True):
    user = get("http://api.vircities.com/hospitals/heal.json?os=unknown&v=3.00", decode=True)['User']
    if hp and user['low_hp']:
        debug("hp: {}/{}".format(user['health'], user['max_health']))
        post("http://api.vircities.com/hospitals/heal_full_hp.json?os=unknown&v=3.00", {})

    if not t:
        return

    for trauma_id in user['traumas']:
        debug("Trauma: {}".format(user['traumas'][trauma_id]['type']))
        post("http://api.vircities.com/hospitals/trauma_heal.json?os=unknown&v=3.00",
             data={"data[Trauma][id]": trauma_id})


def _fight(band_id, complexity, rank):
    data = post(
        "http://api.vircities.com/military/pve/gangs/{band_id}/{complexity}/ranks/{rank}/fight?os=unknown&v=3.00".format(
            band_id=band_id, complexity=complexity, rank=rank), data={}, decode=True)
    get("http://api.vircities.com/military/info?os=unknown&v=3.00")
    get("http://api.vircities.com/military/pve/gangs/13?os=unknown&v=3.00")
    return data


def farm(band_id, complexity, rank, heal_hp=True, heal_t=True, finish_if_broken=True, count=None):
    earned = 0
    try:
        user_info = get_short_info()
        if int(user_info['health']) < int(user_info['max_health']):
            heal()

        while int(user_info['energy']) >= 5 and (count is None or count > 0):
            band_info = get("http://api.vircities.com/military/pve/gangs/info/{id}?os=unknown&v=3.00".format(id=band_id),
                            decode=True)['progress']
            if len(band_info) < complexity:
                print("Mission unavailable")
                break

            if int(rank) > band_info[complexity - 1]['availableRank']:
                print("Mission unavailable")
                break

            result = _fight(band_id, complexity, rank)
            if count is not None:
                count -= 1
            debug("Got damage: ", result['result']['healthLoss'])
            if int(result['result']['healthLoss']) < 0 or result['result']['traumas']:
                time.sleep(1)
                heal(hp=heal_hp, t=heal_t)

            if result['userWin']:
                debug("Earned: {}".format(result['result']['vdEarned']))
                earned += float(result['result']['vdEarned'])
            else:
                debug("WE lost it :(")
            user_info = get_short_info()
            time.sleep(1)
            if int(user_info['health']) == 0:
                warn("No health =(")
                break
            if finish_if_broken and result['result']['brokenItems']:
                warn("Items were broken =(")
                break

        if int(user_info['energy']) < 5:
            warn("No energy =(")
            raise NoEnergyError()

        if count == 0:
            warn("Finished by count=(")
    finally:
        return earned


def sell():
    pass


def check_resources(min_sum=MIN_OFFER):
    # TODO: dumping
    resource_offers = \
    get("http://api.vircities.com/exchanges/lots_by_type_user/resource.json?os=unknown&v=3.00", decode=True)[
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
                interesting_offers[resource['id']] = buy_price
    return interesting_offers


def farm_mset():
    spend = buy_set(JUMMY_MSET)
    time.sleep(2)
    storage = get_storage()
    put_items = [item for item in storage if item.type.name in JUMMY_MSET_ITEMS]
    for item in put_items:
        slot = [it[0] for it in JUMMY_MSET if it[1] == item.type.name][0]
        item.put(slot)
        time.sleep(1.5)
    earned = farm(17, 5, 1, count=30)
    Item.clear()
    warn("Spend: {}".format(spend))
    warn("Earned: {}".format(earned))
    warn("Profit: {}".format(earned - spend))


def farm_mset1():
    spend = buy_set(JUMMY_MSET1)
    earned = 0
    time.sleep(2)
    for i in range(3):
        storage = get_storage()
        put_items = [item for item in storage if item.type.name in JUMMY_MSET1_ITEMS]
        for item in put_items:
            slot = [it[0] for it in JUMMY_MSET1 if it[1] == item.type.name][0]
            item.put(slot)
            time.sleep(1.5)
        earned += farm(17, 4, 2, count=10)
        Item.clear()
    warn("Spend: {}".format(spend))
    warn("Earned: {}".format(earned))
    warn("Profit: {}".format(earned - spend))

if __name__ == '__main__':
    # simulate()
    # print(check_resources())
    # time.sleep(180)
    earned = farm(17, 4, 1, count=30)
    warn("Earned: {}".format(earned))
    try:
        for i in range(1):
            time.sleep(3)
            farm_mset()
    except NoEnergyError:
        pass
    DEBUG_LOG.write("*" * 16 + "END CYCLE" + "*" * 16 + "\n")
    DEBUG_LOG.close()
