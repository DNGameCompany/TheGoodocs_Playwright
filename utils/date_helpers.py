from datetime import datetime, timedelta, timezone


def parse_dt(s: str) -> datetime:
    return datetime.fromisoformat(s.replace("Z", "+00:00"))


PERIOD_DAYS = {"year": 365, "month": 31, "week": 7}

def filter_by_date(pd: datetime, period: str, now: datetime | None = None) -> bool:
    if period not in PERIOD_DAYS:
        raise ValueError(f"Не валідний період перевірки: {period}")

    now = now or datetime.now(timezone.utc)

    # привести до UTC, не затираючи наявну таймзону
    if pd.tzinfo is None:
        pd = pd.replace(tzinfo=timezone.utc)
    else:
        pd = pd.astimezone(timezone.utc)

    start_date = (now - timedelta(days=PERIOD_DAYS[period])).date()
    return start_date <= pd.date() <= now.date()