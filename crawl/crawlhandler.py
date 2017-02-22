class ListHandler:
    def __init__(self, task):
        self.task = task

    def extract_groupon(self):
        tmp = {"grouponid":111,"grouponname":"ttt","shopid":123,"shopname":333,\
                "price":22,"sold_until_now":99}
        return [tmp]

    def extract_page_url(self):
        return []

    def get_current_page_num(self):
        return 0

