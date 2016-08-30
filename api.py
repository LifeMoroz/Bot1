import json
import requests
from local_settings import HEADERS, POST_HEADERS
from log import warn
from exceptions import RequestError

__author__ = 'ruslan_galimov'


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


def item_info(item_id):
    return get("http://api.vircities.com/user_items/get_info/{}.json?os=unknown&v=3.10".format(item_id), decode=True)


def item_type_info(type_id):
    return get("http://api.vircities.com/user_items/get_type_info/{}.json?os=unknown&v=3.10".format(type_id), decode=True)


def put_on(item_id, slot):
    post("http://api.vircities.com/user_items/put_item_on.json?os=unknown&v=3.00",
         {"data[UserItem][id]": item_id, "data[UserItem][slot_id]": slot})


def put_off(item_id):
    post("http://api.vircities.com/user_items/put_item_off.json?os=unknown&v=3.10", {"data[UserItem][item_id]": item_id})


def buy(item_id, number=1):
    post("http://api.vircities.com/exchanges/user_buy.json?os=unknown&v=3.00",
         {"data[Exchange][id]": item_id, "data[Exchange][number]": number, "data[Corporation][id]": 0}, decode=True)


def hospital():
    return get("http://api.vircities.com/hospitals/heal.json?os=unknown&v=3.00", decode=True)


def full_heal():
    post("http://api.vircities.com/hospitals/heal_full_hp.json?os=unknown&v=3.00", {})


def heal_trauma(trauma_id):
    post("http://api.vircities.com/hospitals/trauma_heal.json?os=unknown&v=3.00", data={"data[Trauma][id]": trauma_id})


def band_info(band_id):
    return get("http://api.vircities.com/military/pve/gangs/info/{id}?os=unknown&v=3.00".format(id=band_id), decode=True)


def fight(band_id, complexity, rank):
    data = post(
        "http://api.vircities.com/military/pve/gangs/{band_id}/{complexity}/ranks/{rank}/fight?os=unknown&v=3.00".format(
            band_id=band_id, complexity=complexity, rank=rank), data={}, decode=True)
    get("http://api.vircities.com/military/info?os=unknown&v=3.00")
    get("http://api.vircities.com/military/pve/gangs/13?os=unknown&v=3.00")
    return data


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


def short_info():
    return get("http://api.vircities.com/users/short_infos.json?os=unknown&v=3.00", decode=True)