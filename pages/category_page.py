from pages.base_page import BasePage
from playwright.sync_api import Page, Locator, expect
from pages.locators.category_locators import CategoryLocators
from utils.api_requests import filter_by_template_name
from utils.date_helpers import parse_dt

class CategoryPage(BasePage, CategoryLocators):
    def __init__(self, page: Page):
        super().__init__(page)
        self.__templates_container = page.locator(self.TEMPLATES_CONTAINER)
        self.__template_card = page.locator(self.TEMPLATE_CARD)
        self.__menu_category = page.locator(self.MENU_CATEGORY)
        self.__pagination_block = page.locator(self.PAGINATION_BLOCK)
        self.__sort_block = page.locator(self.SORT_BLOCK)

    def get_templates_container(self) -> Locator:
        return self.__templates_container

    def get_template_card(self) -> Locator:
        return self.__template_card

    def click_template_card(self):
        self.get_templates_container().locator(".category__col-items.template-items.mb-3.grid-item").first.click()

    def get_template_attributes(self, template_card: Locator = None):
        template_locator = self.__template_card
        if template_card:
            template_locator = template_card

        return template_locator.locator(".template-card__items").all()

    def get_all_category_name_from_sidebar(self) -> list[str]:
        elements = self.__menu_category.locator(self.CATEGORY_IN_MENU).all()
        return [el.inner_text().strip().lower() for el in elements]

    def click_to_pagination(self, page_number: int = None, next_prev: str = any(["prev", "next"])):
        if not page_number and next_prev:
            if next_prev == "prev":
                self.__pagination_block.locator(self.PAGINATION_BUTTON_PREV).click()
            elif next_prev == "next":
                self.__pagination_block.locator(self.PAGINATION_BUTTON_NEXT).click()
            else:
                raise ValueError("Не валідне значення кнопки пагінації")
            return
        self.__pagination_block.locator(self.PAGINATION_BUTTON, has_text=f"{page_number}").click()

    def click_to_sort_button(self):
        self.__sort_block.locator(self.SORT_DROPDOWN).click()

    def get_templates_names(self):
        headings = self.get_templates_container().get_by_role("heading", level=3)
        headings.first.wait_for(state="visible")
        return [t.strip() for t in headings.all_text_contents()]

    def click_sort_type(self, sort_type: str):
        page = self.get_current_page()
        with page.expect_response(
                lambda r: "/ajax/category/load-more" in r.url and r.ok
        ) as resp_info:
            page.locator(".special.sort .dropdown-item.js-set-filter.select", has_text=sort_type).click()

        first_name = resp_info.value.json()["templates"][0]["name"]
        headings = self.get_templates_container().get_by_role("heading", level=3)
        expect(headings.first).to_have_text(first_name, timeout=10_000)

    @staticmethod
    def is_sorted_by_latest(template_names_list, access_token, api_key) -> bool:
        last_date = None
        for name in template_names_list:
            response = filter_by_template_name(
                template_name=name,
                access_token=access_token,
                apikey=api_key,
            )
            items = response["data"]["items"]["data"]
            match = next((i for i in items if i["name"] == name), None)
            assert match is not None, f"Шаблон '{name}' не знайдено серед {len(items)} результатів API"

            template_date = parse_dt(match["published_at"])
            # print(f"{match['published_at']} : {name}")

            if last_date is not None and last_date < template_date:
                return False
            last_date = template_date
        return True

    @staticmethod
    def is_sorted_by_popular(template_names_list, access_token, api_key) -> bool:
        groups = {0: [], 1: []}  # 0 = free, 1 = premium

        for name in template_names_list:
            response = filter_by_template_name(
                template_name=name,
                access_token=access_token,
                apikey=api_key,
            )
            items = response["data"]["items"]["data"]
            match = next((i for i in items if i["name"] == name), None)
            assert match is not None, f"Шаблон '{name}' не знайдено серед {len(items)} результатів API"

            groups[match["premium"]].append((name, match["downloads"]))

        is_ok = True
        for premium, templates in groups.items():
            downloads = [d for _, d in templates]
            if downloads != sorted(downloads, reverse=True):
                is_ok = False
        return is_ok




