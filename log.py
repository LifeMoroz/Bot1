__author__ = 'ruslan_galimov'


def debug(*args):
    print(*args, file=DEBUG_LOG)


def warn(*args):
    print(*args)
    debug(*args)


DEBUG_LOG = open("log", 'a', encoding='UTF-8')
