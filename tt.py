# encoding": "utf-8
import random

import set_instances
from user import User


def calculate():
    maximum = 215000.
    fights = 10000
    max_profit = 0
    set_price = None
    k = 100
    k_buy = 1
    for x in range(k * 3, k, -1):
        price = maximum * k / x  # clear price 100vD/OP
        medium = 0
        for _ in range(fights):
            r = 1 + random.random() * 2
            if price * r < maximum:
                medium += price * r
            else:
                medium += maximum

        spend = price * fights * k_buy
        profit = medium - spend
        if profit > max_profit:
            tmp = x
            max_profit = profit
            set_price = price * k_buy

    print(tmp, round(max_profit / fights, 2), round(set_price * 10, 2))


if __name__ == '__main__':
    # print(check_resources())
    user = User()
    set = set_instances.g_set
    while user.energy > set.get_max_strength() * 5:
        user.farm(set)
    # calculate()
