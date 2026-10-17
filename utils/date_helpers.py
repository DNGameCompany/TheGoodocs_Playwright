from datetime import datetime, timedelta, timezone


def parse_dt(s: str) -> datetime:
    return datetime.fromisoformat(s.replace("Z", "+00:00"))


def filter_by_date(pd: datetime, period: str) -> bool:
    current_date = datetime.now(timezone.utc)
    pd = pd.replace(tzinfo=timezone.utc)

    periods = {
        "year": 365,
        "month": 31,
        "week": 7
    }

    if period in periods:
        res = current_date - timedelta(days=periods[period])
        return res <= pd <= current_date
    else:
        raise ValueError(f"Не валідний період перевірки: {period}")