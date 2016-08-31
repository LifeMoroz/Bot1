from sets import Set, ItemType

js_helmet = ItemType(type="armorHead", name="JimmySet Helmet", strength=30)
js_body = ItemType(type="armorBody", name="JimmySet Vest", strength=30)
js_legs = ItemType(type="armorLegs", name="JimmySet Pants", strength=30)
js_boots = ItemType(type="armorBoots", name="JimmySet Boots", strength=30)
js_light_weapon = ItemType(type="closeRangeWeapon", name="Jimmy lite", strength=30)
js_medium_weapon = ItemType(type="closeRangeWeapon", name="Jimmy medium", strength=30)
insoles = ItemType(type="closeRangeWeapon", name="Titanium insoles", strength=10)

js_medium_set = Set(band=(17, 5, 1), head_inventory=js_helmet, torso_inventory=js_body, pants_inventory=js_legs,
                    boots_inventory=js_boots, first_weapon_inventory=js_medium_weapon, second_weapon_inventory=js_medium_weapon)
js_t_set = Set(align=True, band=(17, 5, 1), head_inventory=js_helmet, torso_inventory=js_body, pants_inventory=js_legs,
               boots_inventory=js_boots, first_weapon_inventory=insoles, second_weapon_inventory=insoles)
js_light_set = Set(band=(17, 4, 2), head_inventory=js_helmet, torso_inventory=js_body, pants_inventory=js_legs,
                   boots_inventory=js_boots, first_weapon_inventory=js_light_weapon, second_weapon_inventory=js_light_weapon)
