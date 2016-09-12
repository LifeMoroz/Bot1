import time

import api
from ai import go_buisness
from business import BusinessPage
from exceptions import NoEnergyError
from log import debug, warn
from sets import ItemType, UserItem, Equipment


class UserEquipment(Equipment):
    def set_item(self, item):
        if item.equipped_slot in self._items:
            self._items[item.equipped_slot] = item
        else:
            warn("Unexpected slot ", item.equipped_slot)

    def put_on_item(self, item):
        if item.equipped_slot in self._items:
            self._items[item.equipped_slot] = item
        else:
            warn("Unexpected slot ", item.equipped_slot)

    def is_fitted(self, set):
        for slot, item in self._items.items():
            if set._items[slot] is not None and (item is None or item.type != set._items[slot]):
                return False
        return True


class Inventory(object):
    def __init__(self):
        self.equipment = None
        self.storage = self.get_storage()

    def get_storage(self, short_info=None, **kwargs):
        self.equipment = UserEquipment()
        if short_info:
            equipped_items = short_info['equippedItems']
        else:
            equipped_items = api.get("http://api.vircities.com/users/short_infos.json", decode=True)['equippedItems']
        for it in equipped_items:
            type_it = ItemType(**it['ItemType'])
            user_it = UserItem(type=type_it, **it['UserItem'])
            self.equipment.put_on_item(user_it)

        storage_json = api.get("http://api.vircities.com/user_items/storage.json", decode=True)['storage']
        items = {}
        for i in storage_json['itemsArray']:
            it = i['UserItem']
            if not it['equipped']:
                ttype = ItemType(**storage_json['itemTypes'][str(it['item_type_id'])])
                item = UserItem(type=ttype, **it)
                if items.get(item.type.name):
                    items[item.type.name].append(item)
                else:
                    items[item.type.name] = [item]

        return items

    def is_fitted(self, set):
        return self.equipment.is_fitted(set)

    def has_set(self, set):
        storage_type = [item[0].type for item in self.storage.values()]
        for slot, item in set.items():
            if item is not None and item not in storage_type:
                return False
        return True

    def get_item_slot(self, item):
        slot = item.type.slot
        if self.equipment[slot] and self.equipment[slot].type == item.type and item.is_weapon():
            if item.type.slot == 'first_weapon_inventory':
                return 'second_weapon_inventory'
            else:
                return 'first_weapon_inventory'
        return slot

    def fit(self, set):
        if self.is_fitted(set):
            return

        for item_name, items in self.storage.items():
            if items[0] in set:
                for item in items:
                    slot = self.get_item_slot(item)
                    item.put_on(slot)
                    item.equipped_slot = slot
                    self.equipment.set_item(item)

        self.storage = self.get_storage()

    def unfit(self, set=None):
        for item_name, item in self.equipment.items():
            if item is not None and (set is None or item in set):
                item.put_off()
        self.storage = self.get_storage()

    def check_set(self, set):
        if not self.is_fitted(set):
            self.fit(set)

        if set.align:
            return True

        min_strength = 1000
        unevenly = True
        for item_name, item in self.equipment.items():
            if item is not None and (set is None or item in set) and min_strength > item.strength:
                if min_strength != 1000:
                    unevenly = False
                min_strength = item.strength
        return unevenly

    def set_stength(self, set):
        min_strength = 1000
        for item_name, item in self.equipment.items():
            if item is not None and (set is None or item in set) and min_strength > item.strength:
                min_strength = item.strength
        if min_strength == 1000:
            return 0
        return min_strength


class User(object):
    def __init__(self):
        self.inventory = Inventory()
        user = api.short_info()["user"]["User"]
        self._energy, self._max_health, self._health = int(user['energy']), int(user['max_health']), int(user['health'])
        self._timestamp = time.time() + 60  # Refresh every 60 seconds

    @property
    def energy(self):
        if self._timestamp < time.time():
            user = api.short_info()["user"]["User"]
            self._energy, self._max_health, self._health = int(user['energy']), int(user['max_health']), int(user['health'])
        return self._energy

    @property
    def health(self):
        if self._timestamp < time.time():
            user = api.short_info()["user"]["User"]
            self._energy, self._max_health, self._health = int(user['energy']), int(user['max_health']), int(user['health'])
        return self._health

    @property
    def max_health(self):
        if self._timestamp < time.time():
            user = api.short_info()["user"]["User"]
            self._energy, self._max_health, self._health = int(user['energy']), int(user['max_health']), int(user['health'])
        return self._max_health

    def heal(self):
        user = api.hospital()['User']
        if user['low_hp']:
            debug("hp: {}/{}".format(user['health'], user['max_health']))
            api.full_heal()

        for trauma_id in user['traumas']:
            debug("Trauma: {}".format(user['traumas'][trauma_id]['type']))
            api.heal_trauma(trauma_id)

    def fit(self, set):
        self.inventory.fit(set)

    def _farm(self, band_id, complexity, rank, finish_if_broken=True, count=None):
        earned = 0
        lose = 0
        if int(self.health) < int(self.max_health):
            self.heal()

        while int(self.energy) >= 5 and (count is None or count > 0) and lose < 3:
            self._energy -= 5
            band_info = api.band_info(band_id)['progress']
            if len(band_info) < complexity:
                print("Mission unavailable")
                break

            if int(rank) > band_info[complexity - 1]['availableRank']:
                print("Mission unavailable")
                break

            result = api.fight(band_id, complexity, rank)
            if count is not None:
                count -= 1
            debug("Got damage: ", result['result']['healthLoss'])
            if int(result['result']['healthLoss']) < 0 or result['result']['traumas']:
                time.sleep(1)
                self.heal()

            if result['userWin']:
                debug("Earned in fight: {}".format(result['result']['vdEarned']))
                earned += float(result['result']['vdEarned'])
                lose = 0
            else:
                lose += 1
                warn("WE lost it :(")

            if finish_if_broken and result['result']['brokenItems']:
                warn("Items were broken =(")
                break

        if count == 0:
            debug("Finished by count=(")
            return earned

        if int(self.energy) < 5:
            warn("No energy =(")
            raise NoEnergyError()
        return earned

    def farm(self, set):
        spend = None
        if not self.inventory.is_fitted(set):
            if not self.inventory.has_set(set):
                if 20 - len(self.inventory.storage) > len(set.items()):
                    spend = set.buy()
                else:
                    raise Exception("Inventory full")
                self.update_inventory()
            self.inventory.fit(set)

        self.update_inventory(no_cache=True)
        if not self.inventory.check_set(set) and not set.align:
            warn("Check strength of items in set")
            return

        if not set.align:
            earned = self._farm(*set.band, count=self.inventory.set_stength(set))
        else:
            earned = 0
            count = self.inventory.set_stength(set)
            while count > 0:
                self.inventory.fit(set)
                earned += self._farm(*set.band, count=count)
                self.update_inventory()
                count = self.inventory.set_stength(set)

        warn("Earned: {}".format(earned))
        warn("Earned per OP: {}".format(earned/set.op_cost))
        if spend is not None:
            warn("Spend: {}".format(spend))
            warn("Profit: {}".format(earned - spend))

        self.update_inventory()

    def update_inventory(self, **kwargs):
        self.inventory.storage = self.inventory.get_storage(**kwargs)

    def unfit(self, set=None):
        self.inventory.unfit(set)

    def has_set(self, set):
        return self.inventory.has_set(set)

    def business(self):
        go_buisness()
        page = BusinessPage.first()
        print([obj.name for obj in page.objects])
        page = page.next_page()
        print([obj.name for obj in page.objects])
        page = page.prev_page()
        print([obj.name for obj in page.objects])
