"""Task 2 - Prototype pricing model for a natural gas storage contract.

Value = revenue from withdrawals - cost of injected gas
        - injection/withdrawal fees - storage rent over the contract life.
"""
from pathlib import Path

import pandas as pd

DATA = Path(__file__).parent / "data" / "Nat_Gas.csv"


def load_prices(path=DATA) -> pd.DataFrame:
    df = pd.read_csv(path)
    df["Dates"] = pd.to_datetime(df["Dates"], format="mixed")
    return df.set_index("Dates").sort_index()


def price_gas_storage(
    injection_dates,
    withdrawal_dates,
    prices: pd.DataFrame,
    injection_rate,
    withdrawal_rate,
    max_storage,
    storage_cost_per_day,
    inj_withdraw_cost_per_unit,
):
    """Return the contract value (positive = profit).

    injection_rate / withdrawal_rate: max volume moved on each listed date.
    max_storage: capacity of the facility.
    storage_cost_per_day: fixed rent per day from first injection to last withdrawal.
    inj_withdraw_cost_per_unit: handling fee per unit injected or withdrawn.
    """
    injection_dates = sorted(pd.to_datetime(injection_dates))
    withdrawal_dates = sorted(pd.to_datetime(withdrawal_dates))
    if max(injection_dates) > min(withdrawal_dates):
        raise ValueError("All injections must happen before the first withdrawal.")

    level, value = 0.0, 0.0
    for d in injection_dates:
        vol = min(injection_rate, max_storage - level)
        value -= vol * (prices.loc[d, "Prices"] + inj_withdraw_cost_per_unit)
        level += vol

    for d in withdrawal_dates:
        vol = min(withdrawal_rate, level)
        value += vol * (prices.loc[d, "Prices"] - inj_withdraw_cost_per_unit)
        level -= vol

    total_days = (withdrawal_dates[-1] - injection_dates[0]).days
    value -= total_days * storage_cost_per_day
    return value


if __name__ == "__main__":
    prices = load_prices()
    value = price_gas_storage(
        injection_dates=["2023-05-31", "2023-06-30"],
        withdrawal_dates=["2023-08-31", "2023-09-30"],
        prices=prices,
        injection_rate=500_000,
        withdrawal_rate=500_000,
        max_storage=1_000_000,
        storage_cost_per_day=1_000,
        inj_withdraw_cost_per_unit=0.01,
    )
    print(f"Contract value: {value:,.2f}")
