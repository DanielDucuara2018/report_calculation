from __future__ import annotations

import logging
from typing import Optional, Union

from report_calculation.model import CurrencyPair as ModelCurrencyPair
from report_calculation.utils import (
    async_get_symbol_ticker,
    async_get_symbol_tickers,
    get_symbol_ticker,
)

logger = logging.getLogger(__name__)

EUR_USDT = "EURUSDT"

investment_euros: float = 16302.52
bank_saving_euros: float = 3020


# Total money on cryptos


async def total_crypto_usd() -> float:
    logger.info("Calculating total crypto money in usd")

    currency_pairs = await async_get_symbol_tickers(ModelCurrencyPair.get())

    total_usd = sum(
        float(currency.price) * currency.quantity
        for currency in currency_pairs
        if currency.quantity
    )

    total = float("{:.2f}".format(total_usd))
    logger.info("Total crypto money: %f usd", total)
    return total


async def total_crypto_euros() -> float:
    logger.info("Calculating total crypto money in euros")

    currency_pair = await async_get_symbol_ticker(EUR_USDT)

    total_euros = float(
        "{:.2f}".format(await total_crypto_usd() / float(currency_pair.price))
    )
    logger.info("Total crypto money: %f euros", total_euros)
    return total_euros


# Total money (total money on cryptos + bank savings)


async def total_usd() -> float:
    logger.info("Calculating total money in usd (total crypto money + bank savings)")

    currency_pair = await async_get_symbol_ticker(EUR_USDT)

    total = float(
        "{:.2f}".format(
            await total_crypto_usd() + bank_saving_euros * float(currency_pair.price)
        )
    )
    logger.info("Total money: %f usd", total)
    return total


async def total_euros() -> float:
    logger.info("Calculating total money in euros (total crypto money + bank savings)")
    total = float("{:.2f}".format(await total_crypto_euros() + bank_saving_euros))
    logger.info("Total money: %f euro", total)
    return total


# Total profit (total money on cryptos - investment)


async def profit_usd() -> float:
    logger.info("Calculating total profit in usd (total crypto money - investment)")

    currency_pair = await async_get_symbol_ticker(EUR_USDT)

    diff = float(
        "{:.2f}".format(
            await total_crypto_usd() - investment_euros * float(currency_pair.price)
        )
    )
    logger.info("Total profit: %f usd", diff)
    return diff


async def profit_euros() -> float:
    logger.info("Calculating total profit in euros (total crypto money - investment)")
    diff = float("{:.2f}".format(await total_crypto_euros() - investment_euros))
    logger.info("Total profit: %f euros", diff)
    return diff


# Total invested money


async def invested_usd() -> float:
    logger.info("Calculating total investment in usd")

    currency_pair = await async_get_symbol_ticker(EUR_USDT)

    invested_usd = float("{:.2f}".format(investment_euros * float(currency_pair.price)))
    logger.info("Investment: %f usd", invested_usd)
    return invested_usd


async def invested_euros() -> float:
    logger.info("Calculating total investment in euros")
    investment = float("{:.2f}".format(investment_euros))
    logger.info("Investment: %f euros", investment)
    return investment


# update Crypto


def update(symbol: str, quantity: str) -> ModelCurrencyPair:
    logger.info("Updating %s with value %s", symbol, quantity)
    result = ModelCurrencyPair.get(symbol).update(quantity=float(quantity))  # type: ignore
    logger.info("Result %s", result)
    return result


# get crypto


def read(
    symbol: Optional[str] = None,
) -> Union[ModelCurrencyPair, list[ModelCurrencyPair]]:
    if symbol:
        logger.info("Reading %s data", symbol)
        result = ModelCurrencyPair.get(symbol)
    else:
        logger.info("Reading all data")
        result = ModelCurrencyPair.get()
    logger.info("Result %s", result)
    return result


# create crypto


def create(symbol: str, quantity: str) -> ModelCurrencyPair:
    logger.info("Adding %s with value %s", symbol, quantity)
    get_symbol_ticker(symbol)
    result = ModelCurrencyPair(symbol=symbol, quantity=float(quantity)).create()
    logger.info("Added %s", result)
    return result


# delete crypto


def delete(symbol: str) -> ModelCurrencyPair:
    logger.info("Deleting %s data", symbol)
    result = ModelCurrencyPair.get(symbol).delete()  # type: ignore
    logger.info("Deleted %s", result)
    return result
