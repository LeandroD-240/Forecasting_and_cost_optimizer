# Data Dictionary

**Dataset grain:** one row = one product on one day. The combination `date` + `product_id` must be unique.

| Field | Type | Description |
|---|---|---|
| `date` | Date (YYYY-MM-DD) | Calendar day of the record. One row per product per day, with no gaps in the date range. |
| `product_id` | String | Unique identifier of the product (SKU). Cannot be null. Each product belongs to exactly one category. |
| `category` | Categorical (string) | Product group the SKU belongs to (e.g., storage, cookware, small appliances, décor, seasonal). Fixed set of values that does not change over time for a given product. |
| `units_sold` | Integer | Number of units sold that day. Must be ≥ 0 and cannot exceed the units available. It is recorded sales, not true demand: on stockout days it understates demand. |
| `unit_price` | Decimal (currency) | Selling price per unit that day, in USD. Must be > 0. Can drop during promotions. |
| `stock_on_hand` | Integer | Units in inventory at the end of the day. Must be ≥ 0. |
| `holding_cost_per_unit` | Decimal (currency) | Cost of keeping one unit in inventory for one day, in USD. Must be > 0 and is usually constant per product. |
| `promotion_active` | Binary (0/1) | 1 if a promotion was running for the product that day, 0 otherwise. |
| `is_holiday` | Binary (0/1) | 1 if the date is a public holiday, 0 otherwise. Same value for all products on a given date. |
| `stockout_flag` | Binary (0/1) | 1 if the product ran out of stock that day (`stock_on_hand` = 0), 0 otherwise. Must be consistent with `stock_on_hand`. |

## Data quality rules

- `date` + `product_id` has no duplicates.
- No nulls in any field.
- `units_sold` ≥ 0, `stock_on_hand` ≥ 0, `unit_price` > 0, `holding_cost_per_unit` > 0.
- `stockout_flag` = 1 exactly when `stock_on_hand` = 0.
- Binary fields contain only 0 or 1.

## Samples

| date | product_id | category | units_sold | unit_price | stock_on_hand | holding_cost_per_unit | promotion_active | is_holiday | stockout_flag |
|---|---|---|---|---|---|---|---|---|---|
| 2025-03-14 | P001 | Cookware | 12 | 24.99 | 85 | 0.03 | 0 | 0 | 0 |
| 2025-12-25 | P017 | Seasonal | 5 | 19.99 | 0 | 0.02 | 1 | 1 | 1 |