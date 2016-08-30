from sets import Set, ItemType

js_helmet = ItemType(type="armorHead", name="JimmySet Helmet")
js_body = ItemType(type="armorBody", name="JimmySet Vest")
js_legs = ItemType(type="armorLegs", name="JimmySet Pants")
js_boots = ItemType(type="armorBoots", name="JimmySet Boots")
js_light_weapon = ItemType(type="closeRangeWeapon", name="Jimmy lite")
js_medium_weapon = ItemType(type="closeRangeWeapon", name="Jimmy medium")

js_medium_set = Set(band=(17, 5, 1), head_inventory=js_helmet, torso_inventory=js_body, pants_inventory=js_legs,
                    boots_inventory=js_boots, first_weapon_inventory=js_medium_weapon, second_weapon_inventory=js_medium_weapon)
js_light_set = Set(band=(17, 4, 2), head_inventory=js_helmet, torso_inventory=js_body, pants_inventory=js_legs,
                   boots_inventory=js_boots, first_weapon_inventory=js_light_weapon, second_weapon_inventory=js_light_weapon)
