import re

import pytest
from playwright.sync_api import expect


@pytest.mark.ads
class TestADS:
    @pytest.mark.category
    @pytest.mark.smoke
    def test_ads_placement(self, category_page):
        page = category_page.get_current_page()

        page.wait_for_function(
            "window.googletag && googletag.apiReady && googletag.pubads().getSlots().length > 0",
            timeout=15_000,
        )
        gpt_slots = page.evaluate("""() => googletag.pubads().getSlots().map(s => ({
            id: s.getSlotElementId(),
            path: s.getAdUnitPath(),
        }))""")
        paths = {s["path"].rsplit("/", 1)[-1] for s in gpt_slots}
        assert {
            "thegoodocs.com_lp_desktop_adaptive_inside_listing_1",
            "thegoodocs.com_lp_desktop_adaptive_inside_listing_2",
            "thegoodocs.com_lp_desktop_leaderboard_970_90",
        } <= paths, f"Не вистачає слотів, є: {paths}"

        # Позиції карток із рекламою в гріді (0-based)
        positions = page.locator("#items-container > *").evaluate_all(
            "els => els.flatMap((e, i) => e.querySelector('.ad-wrapper') ? [i] : [])"
        )
        assert positions == [2, 8], f"Реклама на позиціях {positions}"

        # Який слот на якій позиції
        placement = page.locator("#items-container > *").evaluate_all(
            "els => els.flatMap((e, i) => { const s = e.querySelector(\"[id^='div-gpt-ad']\"); return s ? [[i, s.id]] : []; })"
        )
        by_pos = dict(placement)
        id_by_path = {s["path"].rsplit("/", 1)[-1]: s["id"] for s in gpt_slots}
        assert by_pos[2] == id_by_path["thegoodocs.com_lp_desktop_adaptive_inside_listing_1"]
        assert by_pos[8] == id_by_path["thegoodocs.com_lp_desktop_adaptive_inside_listing_2"]

        # Видимість
        grid_slots = page.locator("#items-container [id^='div-gpt-ad']")
        for i in range(grid_slots.count()):
            slot = grid_slots.nth(i)
            slot.scroll_into_view_if_needed()
            expect(slot).to_be_visible()

    @pytest.mark.category
    @pytest.mark.smoke
    def test_top_leaderboard_ads(self, category_page):
        page = category_page.get_current_page()

        # Обидва лідерборди (970 + 728) вміщуються лише на широкому екрані.
        # Viewport треба задати ДО ініціалізації GPT, тому перезавантажуємо сторінку.
        page.set_viewport_size({"width": 1920, "height": 1080})
        page.reload()

        block = page.locator("#js-block-a")
        leaderboard = block.locator("#div-gpt-ad-1749132984743-0")
        leaderboard_right = block.locator("#div-gpt-ad-1749133303561-0")
        hidden_728 = block.locator("#div-gpt-ad-1749133153201-0")
        hidden_300x250 = block.locator("#div-gpt-ad-1750061284318-0")

        # 1. Блок і підпис
        expect(block).to_be_visible(timeout=15_000)
        expect(block.get_by_text("ADVERTISEMENT", exact=True)).to_be_visible()

        # 2. GPT визначив обидва слоти верхнього блоку
        page.wait_for_function(
            """() => window.googletag && googletag.apiReady &&
                googletag.pubads().getSlots().some(
                    s => s.getAdUnitPath().endsWith('leaderboard_right_728_90'))""",
            timeout=15_000,
        )
        paths = page.evaluate(
            "() => googletag.pubads().getSlots().map(s => s.getAdUnitPath().split('/').pop())"
        )
        assert "thegoodocs.com_lp_desktop_leaderboard_970_90" in paths, paths
        assert "thegoodocs.com_lp_desktop_leaderboard_right_728_90" in paths, paths

        # 3. Слоти реально запитані (GPT проставляє data-google-query-id)
        any_id = re.compile(r".+")
        expect(leaderboard).to_have_attribute("data-google-query-id", any_id)
        expect(leaderboard_right).to_have_attribute("data-google-query-id", any_id)

        # 4. Видимі слоти мають потрібні мінімальні розміри
        expect(leaderboard).to_be_visible()
        expect(leaderboard_right).to_be_visible()
        box_l = leaderboard.bounding_box()
        box_r = leaderboard_right.bounding_box()
        assert box_l["width"] >= 970 and box_l["height"] >= 90, box_l
        assert box_r["width"] >= 728 and box_r["height"] >= 90, box_r

        # 5. Порядок: 970 зліва, 728 праворуч, в одному ряду
        assert box_l["x"] < box_r["x"], (box_l, box_r)

        # 6. Резервні слоти приховані
        expect(hidden_728).to_be_hidden()
        expect(hidden_300x250).to_be_hidden()