import pytest

from tests.conftest import all_templates_page


@pytest.mark.all_templates
@pytest.mark.category
class TestAllTemplates:
    @pytest.mark.smoke
    @pytest.mark.parametrize("parameter_name, expected_status", [
        ("Premium", "premium"),
        ("Free", "free"),
    ])
    def test_premium_filter(self, all_templates_page, parameter_name, expected_status):
        all_templates_page.expand_dropdown("Free and Premium")
        all_templates_page.click_filter_parameter(parameter_name)

        assert all_templates_page.all_templates_types_is_(expected_status)


    @pytest.mark.smoke
    @pytest.mark.parametrize("sort_name, expected_sort", [
        ("Popularity", "popular"),
        ("Latest", "latest"),
    ])
    def test_sort(self, all_templates_page, sort_name, expected_sort, auth_credential):
        all_templates_page.expand_dropdown("Latest")
        all_templates_page.click_sort_parameter(sort_name)

        all_templates_page.all_templates_sorted_by_(expected_sort, **auth_credential)

    @pytest.mark.smoke
    @pytest.mark.parametrize("parameter_name, expected_status", [
        ("Last year", "year"),
        ("Last month", "month"),
        ("Last week", "week"),
    ])
    def test_date(self, all_templates_page, parameter_name, expected_status, auth_credential):
        all_templates_page.expand_dropdown("Date Added")
        all_templates_page.click_filter_parameter(parameter_name)

        all_templates_page.check_date_filter_by_last_(expected_status, **auth_credential)



