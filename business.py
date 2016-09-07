import time

from api import company_list, raw_get, short_info, company_info, company_effects
from log import warn


class Company(object):
    def __init__(self, **kwargs):
        self.id = kwargs.get("id")
        self.name = kwargs.get("name")
        self.name = kwargs.get("name")
        self.city = kwargs.get("city")
        self.type = kwargs.get("type")
        self.type_name = kwargs.get("type_name")
        self.employees = kwargs.get("employees")
        self.employees_limit = kwargs.get("employees_limit")
        self.foreign_employees = kwargs.get("foreign_employees")
        self.foreign_employees_limit = kwargs.get("foreign_employees_limit")
        if self.foreign_employees < self.foreign_employees_limit:
            warn("Not full company {}". format(kwargs.get("name")))
        self.current_production = kwargs.get("current_production")
        self.storage = kwargs.get("storage")
        self.is_hiring = kwargs.get("is_hiring")

    def info(self):
        company_info(self.id)
        company_effects(self.id)
        short_info()
        raw_get("http://api.vircities.com/app/images")

    def storage(self):
        self.info()



class BusinessPage(object):
    _page_cache = {}

    def __init__(self, **kwargs):
        self._update(**kwargs)

    def _update(self, **kwargs):
        self.page = int(kwargs.get("page", 1))
        self.current = kwargs.get("current")
        self.count = kwargs.get("count")
        self.has_next = kwargs.get("nextPage")
        self.has_prev = kwargs.get("prevPage")
        self.page_count = kwargs.get("pageCount")
        self.limit = kwargs.get("limit")
        self.objects = kwargs.get("objects", [])

    @staticmethod
    def first():
        if BusinessPage._page_cache.get(1):
            return BusinessPage._page_cache.get(1)
        data = company_list(1)
        objects = [Company(**cmp) for cmp in data['companies']]
        page = BusinessPage(objects=objects, **data['paging']['Company'])
        BusinessPage._page_cache[1] = page
        return page

    def __iter__(self):
        return self.objects.__iter__

    def next_page(self):
        if BusinessPage._page_cache.get(self.page + 1):
            return BusinessPage._page_cache.get(self.page + 1)

        if self.has_next:
            data = company_list(self.page + 1)
        else:
            warn("No next page")
            return None
        objects = [Company(**cmp) for cmp in data['companies']]
        page = BusinessPage(objects=objects, **data['paging']['Company'])
        BusinessPage._page_cache[page.page] = page
        time.sleep(1)
        return page

    def prev_page(self):
        if BusinessPage._page_cache.get(self.page - 1):
            return BusinessPage._page_cache.get(self.page - 1)

        if self.has_prev:
            data = company_list(self.page - 1)
        else:
            warn("No prev page")
            return None
        objects = [Company(**cmp) for cmp in data['companies']]
        page = BusinessPage(objects=objects, **data['paging']['Company'])
        BusinessPage._page_cache[page.page] = page
        time.sleep(1)
        return page
