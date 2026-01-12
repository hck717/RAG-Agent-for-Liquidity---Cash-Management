# TREASURY OPERATIONS MANUAL: GLOBAL PAYMENT CUT-OFF TIMES & SLA
**Version:** 4.2 (Effective Jan 1, 2026)
**Owner:** Global Treasury Operations (HK Hub)
**Applicability:** All entities operating under the Asia-Pacific (APAC) Cash Pool

## 1. Outward Telegraphic Transfers (OTT) - SWIFT & RTGS
Strict adherence to these cut-off times is required to ensure same-day value (Value Date = T+0). Instructions received after the cut-off will be processed on a "best efforts" basis or queued for the next business day (T+1).

| Currency | Destination Market | Channel: Host-to-Host (H2H) | Channel: Online Banking (Manual) | Processing Window | Value Date Impact |
|----------|--------------------|---------------------------|----------------------------------|-------------------|-------------------|
| **USD**  | United States      | 16:30 HKT                 | 17:30 HKT                        | NY Clearing       | Same Day (T+0)    |
| **HKD**  | Hong Kong (CHATS)  | 17:00 HKT                 | 17:55 HKT                        | RTGS              | Real-Time (T+0)   |
| **CNY**  | Mainland China     | 12:00 HKT                 | 14:00 HKT                        | CNAPS             | T+0 (if < 14:00)  |
| **CNH**  | Offshore (HK)      | 16:00 HKT                 | 16:30 HKT                        | RTGS              | Same Day (T+0)    |
| **EUR**  | Eurozone (SEPA)    | 15:30 HKT                 | 16:30 HKT                        | TARGET2           | Same Day (T+0)    |
| **GBP**  | UK (CHAPS)         | 16:00 HKT                 | 16:30 HKT                        | CHAPS             | Same Day (T+0)    |
| **BRL**  | Brazil             | 11:00 HKT                 | 12:00 HKT                        | FX Spot + TED     | **T+2 Standard**  |
| **JPY**  | Japan              | 10:30 HKT                 | 11:00 HKT                        | BOJ-NET           | Same Day (T+0)    |

## 2. ISO 20022 Transition Guidelines (Important)
As of Nov 2025, SWIFT has retired legacy MT formats. All corporate payment instructions must use **ISO 20022 XML (pain.001)** format.
- **Mandatory Fields:**
  - `UltmtDbtr` (Ultimate Debtor): Required for "On-Behalf-Of" (POBO) payments.
  - `Purp` (Purpose Code): 4-character code (e.g., `SALA` for Salary, `SUPP` for Supplier) is now **mandatory** for all cross-border flows.
  - `Strd` (Structured Remittance Info): Invoice numbers must be placed here, not in "Unstructured" fields, to ensure auto-reconciliation.

## 3. High Value & Restricted Payments
- **Threshold:** Payments > USD 5,000,000 require "Level 2" digital signature authorization.
- **Sanctions Screening:** All payments to/from Tier 3 countries (e.g., Myanmar, Venezuela) undergo enhanced due diligence (EDD), adding T+1 to T+3 processing time.
- **Typhoon/Black Rain:** If Signal 8 is hoisted before 12:00 HKT, the cut-off for all paper-based instructions is suspended. Electronic channels remain open but settlement may be delayed to T+1.
