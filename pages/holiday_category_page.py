from pages.base_page import BasePage
from pages.group_page import GroupPage

class HolidayCategoryPage(BasePage, GroupPage):
    def __init__(self, page):
        super().__init__(page)