import os

import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("EXCHANGE_RATE_API_KEY")


def currency_converter(amount: float, currency: str) -> float:
    """Функция обеспечивает обращение к внешнему API для получения текущего курса валют
    и конвертации суммы операции в рубли
    """

    url = f"https://api.apilayer.com/exchangerates_data/latest?base={currency}"
    response = requests.get(url, headers={"apikey": API_KEY})
    if response.status_code != 200:
        raise requests.RequestException
    response_data = response.json()
    amount_rub = round(amount * response_data["rates"]["RUB"], 2)
    return float(amount_rub)
