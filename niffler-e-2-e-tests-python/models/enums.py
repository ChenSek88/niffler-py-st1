from dataclasses import dataclass
from datetime import datetime, timezone

from models.spend import SpendAdd

now_utc = datetime.now(timezone.utc)
spend_date = now_utc.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'


@dataclass
class Category:
    SCHOOL = "QAGURU"
    INTERNET = "ROSTELECOM"
    CARSHARING = "YANDEX DRIVE"
    PHARMACY = "STOLICHKI"
    FAST_FOOD = "ROSTICKS"
    SUPERMARKET = "BILLA"
    TELECOM = "MTS"
    BANK = "SBERBANK"
    OVER_LIMITS = "OVER LIMITS"


@dataclass
class Spend:
    AMOUNT = 50000
    DESCRIPTION = "QA-GURU PYTHON ADVANCED"
    CURRENCY = 'RUB'
    SPEND_DATE = spend_date
    TEST_DATA = SpendAdd(
                    amount=AMOUNT,
                    description=DESCRIPTION,
                    category=Category.SCHOOL,
                    spendDate=SPEND_DATE,
                    currency=CURRENCY)
