# Task 2 – Gas Storage Contract Pricing

**Goal:** Prototype a pricing model for a storage contract: buy gas when cheap, store it, sell it when expensive, net of storage and handling costs.

## Inputs
| Parameter | Meaning |
|-----------|---------|
| `injection_dates` / `withdrawal_dates` | Dates gas is bought / sold (must exist in the price data) |
| `injection_rate` / `withdrawal_rate` | Max volume moved per date |
| `max_storage` | Facility capacity |
| `storage_cost_per_day` | Rent from first injection to last withdrawal |
| `inj_withdraw_cost_per_unit` | Handling fee per unit moved |

## Files
- `gas_storage_pricing.ipynb` – original notebook (example value: 108,000).
- `gas_storage_pricing.py` – clean version of the same function with input validation.
- `data/` – put `Nat_Gas.csv` here.

## Run
```bash
python gas_storage_pricing.py
```

## Notes
The `.py` version raises an error if an injection date falls after the first withdrawal date, and requires dates to be present in the price table (month-end dates). Task 1's `estimate_price` can be used to price arbitrary dates.
