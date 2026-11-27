# TO DO додати тест сортування, фільтрації load more ри ajax з get параметром в урлі на групах та holiday
import pytest

@pytest.mark.category
@pytest.mark.regression
class TestCategory:
    @pytest.mark.holiday
    @pytest.mark.positive
    def test_holiday_sorting_with_get_parameters(self, holiday_page):
        holiday_page.add_get_parameters_in_url(parameters="?test=test")
        holiday_page.apply_sorting_by_latest()
        holiday_page.templates_sorted(soft=True)

    @pytest.mark.group
    @pytest.mark.positive
    def test_group_sorting_with_get_parameters(self, group_page):
        group_page.add_get_parameters_in_url(parameters="?test=test")
        group_page.apply_sorting_by_latest()
        group_page.templates_sorted(soft=True)

