import re

from playwright.sync_api import Page, Locator
from pages.locators.all_templates_locators import AllTemplatesLocators
from pages.locators.category_locators import CategoryLocators
from pages.category_page import CategoryPage
from utils.api_requests import filter_by_template_name
from utils.date_helpers import parse_dt, filter_by_date


class AllTemplatesPage(AllTemplatesLocators, CategoryPage):
    AD_CARD_INDEXES = {2, 8}
    def __init__(self, page: Page):
        super().__init__(page)
        self.__filter_container = page.locator(self.FILTER_CONTAINER)
        self.__filter_dropdown = self.__filter_container.locator(self.FILTER_DROPDOWN)
        self.__dropdown_menu_show = self.__filter_dropdown.locator(self.DROPDOWN_MENU_SHOW)


    def expand_dropdown(self, filter_name: str):
        self.__filter_dropdown.get_by_role("button", name=f"{filter_name}").click()

    def get_dropdown_menu(self) -> Locator:
        return self.__dropdown_menu_show

    def click_filter_parameter(self, parameter_name: str):
        self.get_dropdown_menu().is_visible()
        self.__dropdown_menu_show.locator(self.PARAMETER_FILTER).filter(has_text=re.compile(rf"^\s*{re.escape(parameter_name)}\s*$")).click()

    def click_sort_parameter(self, parameter_name: str):
        self.get_dropdown_menu().is_visible()
        # self.__dropdown_menu_show.locator(self.SORT_PARAMETER).filter(has_text=re.compile(rf"^\s*{re.escape(parameter_name)}\s*$")).click()
        self.__dropdown_menu_show.get_by_role("link", name=re.compile(rf"^\s*{re.escape(parameter_name)}\s*$")).click()

    @staticmethod
    def get_premium_indicator(template_locator: Locator) -> Locator:
        return template_locator.locator(CategoryLocators.PREMIUM_INDICATOR)

    def all_templates_types_is_(self, premium_status: str = "premium") -> bool:
        if premium_status not in ("premium", "free"):
            raise ValueError(f"premium_status має бути 'premium' або 'free', отримано: {premium_status!r}")

        with self.get_current_page().expect_response(
                lambda r: "/ajax/all-templates/load-more" in r.url and r.ok
        ) as resp_info:
            templates = self.get_template_card().all()
        assert templates, "Немає жодного шаблону для перевірки"

        wrong = []
        checked = 0




        for index, template in enumerate(templates):
            if index in self.AD_CARD_INDEXES:
                continue
            checked += 1


            indicator_count = self.get_premium_indicator(template).count()
            match premium_status:
                case "premium":
                    ok = indicator_count > 0
                case "free":
                    ok = indicator_count == 0
            if not ok:
                wrong.append(index)

        assert checked, "Усі картки виключені з перевірки"
        assert not wrong, f"Картки з неправильним статусом '{premium_status}' (індекси, з 0): {wrong}"
        return True


    def all_templates_sorted_by_(self, sort_name, access_token, api_key) -> bool:
        if sort_name not in ("popular", "latest"):
            raise ValueError(f"sort_name має бути 'popular' або 'latest', отримано: {sort_name!r}")

        self.get_template_card().first.wait_for(state="visible", timeout=5000)

        templates = self.get_template_card().all()
        assert templates, "Немає жодного шаблону для перевірки"

        match sort_name:
            case "popular":
                return self.is_sorted_by_popular(template_names_list=self.get_templates_names(),
                                                 access_token=access_token,
                                                 api_key=api_key)
            case "latest":
                return self.is_sorted_by_latest(template_names_list=self.get_templates_names(),
                                                access_token=access_token,
                                                api_key=api_key)
        return False


    def check_date_filter_by_last_(self, parameter_name: str, access_token: str, api_key: str) -> bool:
        if parameter_name not in ("year", "month", "week"):
            raise ValueError(f"parameter_name має бути 'year' або 'month' або 'week', отримано: {parameter_name!r}")

        self.get_template_card().first.wait_for(state="visible", timeout=5000)
        templates_names = self.get_templates_names()
        assert templates_names, "Немає жодного шаблону для перевірки"

        wrong = []
        checked = 0
        for index, template_name in enumerate(templates_names):
            if index in self.AD_CARD_INDEXES:
                continue
            checked += 1
            response = filter_by_template_name(
                template_name=template_name,
                access_token=access_token,
                apikey=api_key
            )
            items = response["data"]["items"]["data"]
            match = next((i for i in items if i["name"] == template_name), None)
            assert match is not None, f"Шаблон '{template_name}' не знайдено серед {len(items)} результатів API"

            template_date = parse_dt(match["published_at"])

            ok = filter_by_date(template_date, parameter_name)
            if not ok:
                wrong.append(index)

        assert checked, "Усі картки виключені з перевірки"
        assert not wrong, f"Картки в неправильному діапазоні: '{parameter_name}' (індекси, з 0): {wrong}"
        return True