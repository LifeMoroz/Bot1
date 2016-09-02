from sets import Set, ItemType

# JUMMY SET
js_helmet = ItemType(type="armorHead", name="JimmySet Helmet", strength=30)
js_body = ItemType(type="armorBody", name="JimmySet Vest", strength=30)
js_legs = ItemType(type="armorLegs", name="JimmySet Pants", strength=30)
js_boots = ItemType(type="armorBoots", name="JimmySet Boots", strength=30)
js_light_weapon = ItemType(type="closeRangeWeapon", name="Jimmy lite", strength=30)
js_medium_weapon = ItemType(type="closeRangeWeapon", name="Jimmy medium", strength=30, produce_hours=3848)

# JUMMY MAX
js_max_helmet = ItemType(type="armorHead", name="JimmyMax Helmet", strength=10, produce_hours=1261)
js_max_body = ItemType(type="armorBody", name="JimmyMax Vest", strength=10, produce_hours=1274)
js_max_legs = ItemType(type="armorLegs", name="JimmyMax Pants", strength=10, produce_hours=1261)
js_max_boots = ItemType(type="armorBoots", name="JimmyMax Boots", strength=10, produce_hours=1261)
js_max_weapon = ItemType(type="closeRangeWeapon", name="JimmyMax", strength=10, produce_hours=1261)

# A POWER SET
apower_max_helmet = ItemType(id=2316, type="armorHead", name="Advanced Power Armor Helmet", strength=10, produce_hours=1024)
apower_max_body = ItemType(id=2318, type="armorBody", name="Advanced Power Armor Body", strength=10, produce_hours=1024)
apower_max_legs = ItemType(id=2322, type="armorLegs", name="Advanced Power Armor Front Legs", strength=10, produce_hours=1024)
apower_max_boots = ItemType(id=2320, type="armorBoots", name="Advanced Power Armor Rear Legs", strength=10, produce_hours=1024)

power_max_helmet = ItemType(id=2298, type="armorHead", name="Power Armor Helmet", strength=10, produce_hours=1024)
power_max_body = ItemType(id=2300, type="armorBody", name="Power Armor Body", strength=10, produce_hours=1024)
power_max_legs = ItemType(id=2304, type="armorLegs", name="Armor Front Legs", strength=10, produce_hours=1024)
power_max_boots = ItemType(id=2302, type="armorBoots", name="Power Armor Rear Legs", strength=10, produce_hours=1024)

# WEAPON
insoles = ItemType(type="closeRangeWeapon", name="Titanium insoles", strength=10)
razor_blade = ItemType(id=2159, type="closeRangeWeapon", name="RazorBlade", strength=10, produce_hours=2904)
balisong = ItemType(id=2219, type="closeRangeWeapon", name="Balisong", strength=10, produce_hours=1302)
gold_kastet = ItemType(id=2219, type="closeRangeWeapon", name="Gold kastet", strength=10)
justice_ring = ItemType(id=1422, type="closeRangeWeapon", name="Justice Ring ", strength=10, produce_hours=1549)

js_medium_set = Set(band=(17, 5, 1), head_inventory=js_helmet, torso_inventory=js_body, pants_inventory=js_legs,
                    boots_inventory=js_boots, first_weapon_inventory=js_medium_weapon, second_weapon_inventory=js_medium_weapon)
js_t_set = Set(align=True, band=(17, 5, 1), head_inventory=js_helmet, torso_inventory=js_body, pants_inventory=js_legs,
               boots_inventory=js_boots, first_weapon_inventory=insoles, second_weapon_inventory=insoles)

js_align_set = Set(band=(17, 4, 3), align=True, head_inventory=js_helmet, torso_inventory=js_body, pants_inventory=js_legs,
                   boots_inventory=js_boots, first_weapon_inventory=balisong, second_weapon_inventory=balisong)

js_max_set = Set(band=(18, 5, 4), head_inventory=js_max_helmet, torso_inventory=js_max_body, pants_inventory=js_max_legs,
                 boots_inventory=js_max_boots, first_weapon_inventory=js_light_weapon, second_weapon_inventory=js_max_weapon)

js_max_light_set = Set(band=(17, 5, 2), head_inventory=js_max_helmet, torso_inventory=js_max_body, pants_inventory=js_max_legs,
                       boots_inventory=js_max_boots, first_weapon_inventory=js_light_weapon, second_weapon_inventory=js_light_weapon)

apower_set = Set(band=(18, 5, 4), head_inventory=js_max_helmet, torso_inventory=power_max_body, pants_inventory=power_max_legs,
                 boots_inventory=js_max_boots, first_weapon_inventory=justice_ring, second_weapon_inventory=justice_ring)

power_set = Set(band=(18, 5, 4), head_inventory=power_max_helmet, torso_inventory=power_max_body, pants_inventory=power_max_legs,
                boots_inventory=power_max_boots, first_weapon_inventory=justice_ring, second_weapon_inventory=justice_ring)