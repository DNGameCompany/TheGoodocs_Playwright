class MembershipsLocators:
    MEMBERSHIPS_BLOCK = ".membership-subscribe.NY"
    CHECKOUT_MODAL = ".checkout__modal"
    JS_FAST_REG = ".js-fast-reg"
    JS_FAST_LOGIN = ".js-fast-login"

    def plan_card(self, plan: str = None) -> str:
        if not plan:
            raise ValueError("Відсутня назва плану")
        return f"button.js-member-button[data-type='{plan}']"