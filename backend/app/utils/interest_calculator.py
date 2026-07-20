from decimal import Decimal, ROUND_HALF_UP
from datetime import date

TWOPLACES = Decimal("0.01")


def months_between(start_date: date, end_date: date) -> Decimal:
    if end_date <= start_date:
        return Decimal("0")

    year_diff = end_date.year - start_date.year
    month_diff = end_date.month - start_date.month

    months = Decimal(year_diff * 12 + month_diff)

    if end_date.day > start_date.day:
        months += Decimal(end_date.day - start_date.day) / Decimal("30")
    elif end_date.day < start_date.day:
        months -= Decimal(start_date.day - end_date.day) / Decimal("30")

    return months


def calculate_interest(
    principal: Decimal,
    rate: Decimal,
    method: str,
    start_date: date,
    end_date: date,
) -> Decimal:
    """
    Supports:
    - PERCENTAGE
    - RUPEES_PER_100
    """

    months = months_between(start_date, end_date)

    if months <= 0 or principal <= 0:
        return Decimal("0.00")

    if method == "PERCENTAGE":
        interest = principal * (rate / Decimal("100")) * months

    elif method == "RUPEES_PER_100":
        interest = (principal / Decimal("100")) * rate * months

    else:
        raise ValueError("Invalid interest method")

    return interest.quantize(
        TWOPLACES,
        rounding=ROUND_HALF_UP
    )