# Demand Forecasting & Inventory Cost Optimizer

## 1. Company Context

**Vertex Home Goods** is a mid-size, vertically integrated company that manufactures and sells home and kitchen products (storage, cookware, small appliances, décor, seasonal items) through its own e-commerce site and a network of partner retailers.

| Attribute | Value |
|---|---|
| Annual revenue | ~$48M |
| Active SKUs | ~500 across 5 categories |
| Channels | 60% e-commerce, 40% wholesale/partner retail |
| Operations | Own manufacturing plant + 2 warehouses |
| Gross margin | ~34% |
| Average inventory value | ~$9.5M |
| Planning process | Monthly spreadsheet-based reorder decisions, driven by planner experience |

---

## 2. Frame the Problem

Vertex wants to run its manufacturing, sales, and inventory operations more efficiently. It has years of transactional data and suspects that a data scientist, combining statistical modeling with business knowledge, can turn that data into better decisions.

Today, two failures coexist: **overstock** on slow movers (cash tied up, markdowns, obsolescence) and **stockouts** on fast movers (lost sales, unhappy customers). Both come from the same source: replenishment and production decisions are made without a quantified view of future demand.

---

## 3. Root Cause (5 Whys)

1. **Why do you want to improve inventory and increase sales?**
   To get more revenue with less cost.
2. **Why are current revenue and investment not enough to achieve this?**
   Because we feel we can make more with less.
3. **Why do you feel you can make more with less effort?**
   Because our processes are somewhat outdated and competitors are moving faster than we expected.
4. **Why are your processes outdated?**
   Because we never followed up on or measured our operating state.
5. **Why was there no follow-up?**
   Because decisions have been made by experience and intuition, with no forecast or shared metrics to reduce uncertainty.

**Root cause.** The problem is not effort or investment; it is **uncertainty without measurement**. Without a demand forecast and tracked KPIs, the company over-protects with excess stock on some SKUs and under-protects on others. The project must therefore deliver a reliable view of future demand and a decision rule that converts that forecast into cost-aware inventory actions.

---

## 4. Business Objectives

| Type | Objective |
|---|---|
| **Primary** | Reduce total inventory cost while maintaining or improving service level. |
| **Secondary** | Recover revenue lost to stockouts and improve gross margin. |
| **Enabling** | Establish a measured, repeatable forecasting and replenishment process. |

**Stakeholders**

| Stakeholder | Interest |
|---|---|
| COO / Operations | Lower inventory cost, stable production planning |
| Supply chain planners | Actionable reorder points and order quantities |
| Finance (CFO) | Working capital released, margin impact |
| Sales / Merchandising | Availability of top sellers, promotion planning |

---

## 5. KPIs

Baselines are current state values; targets are 12-month goals. Each target will be validated on a held-out test period (backtest/simulation).

### 5.1 North Star

| KPI | Definition | Baseline | Target |
|---|---|---|---|
| **Total Inventory Cost (% of revenue)** | (Holding + ordering + stockout + obsolescence/markdown cost) ÷ revenue | 14.0% | ≤ 10.5% (−25%) |

### 5.2 Forecast Quality (predictive)

| KPI | Definition | Baseline (naive/manual) | Target |
|---|---|---|---|
| **WAPE** (weekly, SKU level) | Σ\|actual − forecast\| ÷ Σ actual | 32% | ≤ 18% |
| **Forecast Bias** | (Σ forecast − Σ actual) ÷ Σ actual | +9% (over-forecast) | within ±5% |
| **Improvement vs. seasonal-naive** | Relative WAPE reduction | n/a | ≥ 20% |

### 5.3 Inventory & Service (prescriptive)

| KPI | Definition | Baseline | Target |
|---|---|---|---|
| **Service level / fill rate** | Units fulfilled ÷ units demanded | 91% | ≥ 96% |
| **Stockout rate** | % of SKU-days with zero stock | 8% | ≤ 3% |
| **Inventory turnover** | COGS ÷ average inventory value | 4.2x | ≥ 5.5x |
| **Days of inventory (DOI)** | Average inventory ÷ daily COGS | 87 days | ≤ 66 days |
| **Holding cost** | Annual cost of carrying inventory (22% of value) | $2.1M | ≤ $1.6M |

### 5.4 Financial

| KPI | Definition | Baseline | Target |
|---|---|---|---|
| **Lost sales from stockouts** | Estimated revenue lost on stockout days | 4.5% of revenue | ≤ 1.5% |
| **Gross margin** | (Revenue − COGS) ÷ revenue | 34% | ≥ 36% |
| **Working capital released** | Reduction in average inventory value | n/a | ≥ $1.5M |

**Guardrail.** No cost reduction is accepted if service level falls below 95%. Cutting inventory by letting stockouts rise does not count as a win.

---

## 6. Business Levers

Levers are the decisions the company can actually change. Demand, supplier behavior, and competitor actions are **not** levers; they are uncertainties to model.

| Lever | Decision | Affects |
|---|---|---|
| **Safety stock** | Buffer per SKU based on forecast error and lead time | Stockouts vs. holding cost |
| **Reorder point** | Stock level that triggers replenishment | Service level, DOI |
| **Order / production quantity** | Batch size per SKU (EOQ-style tradeoff) | Ordering cost vs. holding cost |
| **Review frequency** | Monthly → weekly replenishment review | Responsiveness, workload |
| **Pricing & promotions** | Price points, discount depth and timing | Demand, margin, clearing slow stock |
| **Assortment prioritization** | ABC-XYZ policy by value and demand variability | Where to concentrate service and capital |
| **Production planning** | Align manufacturing schedule with the forecast | Lead time, overstock |

**Constraints**

- Minimum order quantities and lead times (7–45 days depending on SKU)
- Warehouse capacity limit
- Price changes bounded to ±15% and constrained by brand positioning
- Service-level floor of 95% for A-class SKUs

---

## 7. Main Question

> **How can demand forecasting and inventory and pricing optimization help Vertex's supply chain and finance teams reduce total inventory cost by 25% while keeping service level above 95%?**

## 8. Analytical Approach

This project is **predictive + prescriptive**:

- **Predictive:** forecast SKU-level demand with uncertainty (prediction intervals), because the cost optimizer needs forecast error, not just a point estimate.
- **Prescriptive:** convert forecasts into replenishment and pricing decisions that minimize total expected cost under the constraints above.

**Success criteria**

- Forecast model beats the seasonal-naive baseline by ≥ 20% WAPE on a time-based hold-out.
- Optimized policy cuts simulated total inventory cost by ≥ 25% with service level ≥ 95%.
- Results are explained in business terms (dollars, days of stock, fill rate), not only model metrics.