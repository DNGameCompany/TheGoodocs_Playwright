import pytest

from utils.docx_colors import get_accent_color


@pytest.mark.regression
@pytest.mark.download
class TestDownload:
    @pytest.mark.positive
    def test_download_template_color(self, template_page_new_design_with_color, tmp_path):
        expected_hex = template_page_new_design_with_color.get_actual_color()

        download = template_page_new_design_with_color.download_template_new_design(platform_name="Microsoft Word")

        save_path = tmp_path / download.suggested_filename
        download.save_as(save_path)

        actual_hex = get_accent_color(save_path)
        assert actual_hex == expected_hex, (
            f"Колір не збігається: на сайті #{expected_hex}, у файлі #{actual_hex}"
        )



