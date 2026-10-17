import re
import pytest
from playwright.sync_api import expect

from pages.category_page import CategoryPage
from utils.string_helpers import is_sorted_alphabetically


@pytest.mark.category
class TestCategory:

    @pytest.mark.smoke
    def test_categories_sorted_alphabetically(self, category_page: CategoryPage):
        names = category_page.get_all_category_name_from_sidebar()
        assert names, "Список категорій порожній"
        assert is_sorted_alphabetically(names), f"Категорії не відсортовані: {names}"

    @pytest.mark.smoke
    def test_pagination(self, category_page: CategoryPage):
        page_2 = re.compile(r" - Page 2")
        category_page.click_to_pagination(page_number=2)

        expect(category_page.get_h1()).to_contain_text(page_2)
        expect(category_page.get_current_page()).to_have_title(page_2)
        expect(category_page.get_description()).to_have_attribute("content", page_2)

    @pytest.mark.smoke
    def test_sort_latest(self, category_page: CategoryPage, auth_credential):
        category_page.click_to_sort_button()
        category_page.click_sort_type("Latest")
        assert category_page.is_sorted_by_latest(template_names_list=category_page.get_templates_names(),
                                          **auth_credential) == True

    @pytest.mark.smoke
    def test_sort_popular(self, category_page: CategoryPage, auth_credential):
        assert category_page.is_sorted_by_popular(template_names_list=category_page.get_templates_names(),
                                                 **auth_credential) == True

