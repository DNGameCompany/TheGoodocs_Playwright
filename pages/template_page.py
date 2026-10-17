from pages.base_page import BasePage
from playwright.sync_api import Page, Download
from pages.locators.template_locators import TemplateLocators


class TemplatePage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self._edit_container = page.locator(TemplateLocators.EDIT_CONTAINER)
        self._format_modal_files = page.locator(TemplateLocators.FILE_MODAL)
        self._format_modal_sizes = page.locator(TemplateLocators.SIZES_MODAL)

    # --- Новий дизайн ---
    def choose_platform_tab_new(self, platform_name: str):
        self._edit_container.locator(TemplateLocators.PLATFORM_TAB).filter(has_text=platform_name).click()

    def click_download_button_new(self):
        self._edit_container.locator(TemplateLocators.DOWNLOAD_BUTTON).click()

    def download_template_new_design(self, platform_name: str = "Microsoft Word", timeout_ms: int = 30000) -> Download:
        self.choose_platform_tab_new(platform_name)

        with self.get_current_page().expect_download(timeout=timeout_ms) as download_info:
            self.click_download_button_new()

        return download_info.value

    def open_in_browser_new_design(self, platform_name: str="Google Docs", timeout_ms: int = 30000) -> Page:
        self.choose_platform_tab_new(platform_name)

        with self.get_current_page().context.expect_page(timeout=timeout_ms) as new_page_info:
            self.click_download_button_new()

        new_page = new_page_info.value
        # Дочікуємося, поки відкрита сторінка почне завантажуватися
        new_page.wait_for_load_state("domcontentloaded")
        return new_page

    # --- Старий дизайн ---
    def choose_platform_tab_old(self):
        """Розкриває випадаючий список."""
        self._edit_container.locator(TemplateLocators.DROPDOWN_TOGGLE_ICON).click()

    def click_download_button_old(self):
        """Натискає на пункт у випадайці."""
        self._edit_container.locator(TemplateLocators.WORD_DROPDOWN_ITEM).click()

    def click_copy_template_button_old(self):
        self._edit_container.locator(TemplateLocators.COPY_IN_BROWSER_BUTTON_OLD).click()

    def click_modal_format_files_button(self, format_name: str = "A4"):
        """Шукає кнопку формату безпосередньо за класом та текстом всередині модалки."""
        # Для надійності використовуємо css-клас кнопки .js-download-button + filter за точним текстом
        button = self._format_modal_files.locator(TemplateLocators.MODAL_DOWNLOAD_BUTTON).filter(has_text=format_name).first
        button.click()

    def click_modal_format_sizes_button(self, format_name: str = "A4"):
        """Шукає кнопку формату безпосередньо за класом та текстом всередині модалки."""
        # Для надійності використовуємо css-клас кнопки .js-download-button + filter за точним текстом
        button = self._format_modal_sizes.locator(TemplateLocators.MODAL_DOWNLOAD_BUTTON).filter(has_text=format_name).first
        button.click()

    def download_template_old_design(
            self,
            paper_format: str = "A4",
            timeout_ms: int = 30000
    ) -> Download:
        # 1. Відкриваємо дропдаун
        self.choose_platform_tab_old()

        # 2. Клікаємо на пункт у дропдауні
        self.click_download_button_old()

        # 3. КРИТИЧНО: Явно чекаємо, поки модалка з'явиться в DOM та стане видимою!
        self._format_modal_files.wait_for(state="visible", timeout=10000)

        # 4. Тепер огортаємо клік у expect_download
        with self.get_current_page().expect_download(timeout=timeout_ms) as download_info:
            self.click_modal_format_files_button(paper_format)

        return download_info.value


    def open_in_browser_old_design(
            self,
            paper_format: str = "A4",
            timeout_ms: int = 30000
    ) -> Page:
        self.click_copy_template_button_old()

        self._format_modal_sizes.wait_for(state="visible", timeout=10000)

        with self.get_current_page().context.expect_page(timeout=timeout_ms) as new_page_info:
            self.click_modal_format_sizes_button(paper_format)

        new_page = new_page_info.value
        # Дочікуємося, поки відкрита сторінка почне завантажуватися
        new_page.wait_for_load_state("domcontentloaded")
        return new_page