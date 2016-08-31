# encoding": "utf-8

import set_instances
from ai import check_resources
from user import User


if __name__ == '__main__':
    # print(check_resources())
    print(set_instances.js_max_set.buy())
    user = User()
    while user.energy > set_instances.js_max_set.get_max_strength() * 5:
        user.farm(set_instances.js_max_set)
