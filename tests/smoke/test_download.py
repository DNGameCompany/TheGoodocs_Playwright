import re

import pytest
from playwright.sync_api import expect

from tests.conftest import template_page_old_design


@pytest.mark.download
class TestDownload:
    @pytest.mark.smoke
    def test_download_new_design(self, template_page_new_design, tmp_path):
        download = template_page_new_design.download_template_new_design(platform_name="Microsoft Word")


        save_path = tmp_path / download.suggested_filename
        download.save_as(save_path)

        assert save_path.exists(), f"Файл не зберігся: {save_path}"
        assert save_path.stat().st_size > 0, "Завантажений файл порожній"
        assert download.suggested_filename.endswith((".docx",)), f"Невірне розширення: {download.suggested_filename}"

    @pytest.mark.smoke
    def test_download_old_design(self, template_page_old_design, tmp_path):
        download = template_page_old_design.download_template_old_design()

        save_path = tmp_path / download.suggested_filename

        download.save_as(save_path)

        assert save_path.exists(), f"Файл не зберігся: {save_path}"
        assert save_path.stat().st_size > 0, "Завантажений файл порожній"
        assert download.suggested_filename.endswith((".docx",)), f"Невірне розширення: {download.suggested_filename}"

    @pytest.mark.smoke
    def test_open_in_browser_new_design(self, template_page_new_design):
        new_page = template_page_new_design.open_in_browser_new_design()

        expect(new_page).to_have_url(re.compile(r"https://(docs|accounts)\.google\.com/.*"))
        new_page.close()

    @pytest.mark.smoke
    def test_open_in_browser_old_design(self, template_page_old_design):
        new_page = template_page_old_design.open_in_browser_old_design()

        expect(new_page).to_have_url(re.compile(r"https://(docs|accounts)\.google\.com/.*"))
        new_page.close()
