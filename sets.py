import time

import local_settings
from consts import SIMULATE
from exceptions import RequestError, PriceError
from log import debug, warn
from api import put_on, buy, get_item_id, get_best_offer, put_off, item_info, item_type_info


class ItemTypeMeta(type):
    def __init__(cls, *args, **kwargs):
        cls.__cached_type = {}
        super().__init__(*args, **kwargs)

    def __call__(cls, *args, **kwargs):
        if kwargs.get("name") is None:
            raise Exception
        kwargs["name"] = kwargs.get("name").strip().replace("  ", " ")

        if kwargs["name"] in cls.__cached_type:
            return cls.__cached_type[kwargs["name"]]
        else:
            new_type = super(ItemTypeMeta, cls).__call__(*args, **kwargs)
            cls.__cached_type[kwargs["name"]] = new_type
        return new_type


class NoSuchItem(Exception):
    pass


class ItemType(metaclass=ItemTypeMeta):
    def __init__(self, **kwargs):
        self.type = kwargs.get("type")
        self.name = kwargs.get("name")
        self.id = kwargs.get("id")
        self.receipt_id = kwargs.get("receipt_id")
        if kwargs.get("class") and "_items" in kwargs["class"]:
            self.slot = kwargs["class"].replace("_items", "_inventory")
        elif kwargs.get("slot"):
            self.slot = kwargs.get("slot")
        else:
            self.slot = None
        self.category_id = kwargs.get("category_id")
        self.produce_hours = kwargs.get("produce_hours")
        self.strength = kwargs.get("strength")

    def buy(self, quantity=1):
        if not self.id:
            item_id = get_item_id(self.type, self.name)
        else:
            item_id = self.id
        offer = get_best_offer(item_id)
        spend = 0
        bought = 0
        if not offer:
            warn("No such items ", self.name)
            raise NoSuchItem
        while bought < quantity:
            try:
                _buy = offer['number'] if offer['number'] < quantity else quantity
            except TypeError:
                _buy = 1
                pass
            debug("WTB: {} x{}".format(self.name, _buy))
            if local_settings.NOT_MORE_THAN and self.produce_hours and self.produce_hours * local_settings.NOT_MORE_THAN < float(offer['price']):
                debug("Cost too much {}".format(round(float(offer['price']) / self.produce_hours), 2))
                raise PriceError("Cost too much")
            buy(offer['id'], _buy)
            bought += _buy
        spend += float(offer['price'])
        time.sleep(1)
        return spend

    def is_weapon(self):
        return bool(self.slot) and "weapon" in self.slot


class UserItem(object):
    def __init__(self, type, **kwargs):
        self.id = kwargs.get("id")
        self.strength = kwargs.get("strength")
        self.equipped_slot = kwargs.get("equipped_slot")
        self.quantity = kwargs.get("quantity")
        self.type = type

    def is_weapon(self):
        return self.type.is_weapon()

    def simulate(self):
        if SIMULATE:
            if self.id:
                item_info(self.id)
            if self.type.id:
                item_type_info(self.type.id)

    def put_on(self, slot):
        self.simulate()
        try:
            put_on(self.id, slot)
        except RequestError:
            warn("Put \"{}\" FAILED".format(slot))
            return
        debug("Put on: ", slot)
        time.sleep(0.5)

    def put_off(self):
        self.simulate()
        put_off(self.id)
        time.sleep(1)

    def sell(self):  # TODO:
        pass


class Equipment(object):
    def __init__(self, **kwargs):
        self._items = {
            "head_inventory": None,
            "torso_inventory": None,
            "pants_inventory": None,
            "boots_inventory": None,
            "first_weapon_inventory": None,
            "second_weapon_inventory": None,
            "quick_inventory_1": None,
            "quick_inventory_2": None,
            "quick_inventory_3": None,
            "first_ring_inventory": None,
            "second_ring_inventory": None,
        }
        for key in self._items.keys():
            value = kwargs.get(key)
            if value is None:
                continue
            if value.slot is None:
                value.slot = key
            self._items[key] = value

    def items(self):
        return self._items.items()

    def slots(self):
        return self._items.keys()

    def get(self, key, default=None):
        return self._items.get(key, default)

    def __getitem__(self, y):
        return self._items[y]

    def __setitem__(self, key, value):
        if key in self._items:
            self._items[key] = value
        else:
            raise KeyError

    def __iter__(self):
        return self._items.__iter__()

    def __contains__(self, item):
        if isinstance(item, ItemType):
            return item in self._items.values()
        elif isinstance(item, UserItem):
            return item.type in self._items.values()
        else:
            return TypeError


class Set(Equipment):
    def __init__(self, *args, **kwargs):
        self.band = kwargs.pop("band")
        self.align = kwargs.get("align")
        if self.align is not None:
            kwargs.pop("align")
        super().__init__(**kwargs)

    def set_items(self):
        return self._items.values()

    def get_max_strength(self):
        max_strength = None
        for _, item in self.items():
            if item is not None and (max_strength is None or item.strength > max_strength):
                max_strength = item.strength
        return max_strength

    def buy(self):  # TODO: Move to Inventory
        spend = 0
        if self.align:
            max_strength = self.get_max_strength()
        for item in self.set_items():
            if item is None:
                continue
            if self.align and max_strength and item.strength:
                if max_strength % item.strength == 0:
                    quantity = int(max_strength / item.strength)
                else:
                    warn("Cant set quantity of items to align set")
                    quantity = 1
            else:
                quantity = 1

            spend += sum([item.buy() for _ in range(quantity)])

        return spend

    @property
    def op_cost(self):
        return sum([float(item.produce_hours) for _name, item in self.items() if item is not None])
