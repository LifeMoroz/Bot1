# encoding": "utf-8

from set_instances import js_t_set
from user import User


if __name__ == '__main__':
    user = User()
    while user.energy > js_t_set.get_max_strength() * 5:
        user.farm(js_t_set)
    # time.sleep(1)
