Table: accounts
Schema:
| account_id                   | client_name        | client_segment | entity            | currency | balance    | type        | pool_id          |
| ---------------------------- | ------------------ | -------------- | ----------------- | -------- | ---------- | ----------- | ---------------- |
| HK_MAIN_HQ                   | FastFashion Co     | Retail         | FastFashion HK HQ | HKD      | 85,000,000 | HEADER      | POOL_HK_01       |
| US_SALES                     | DeepTech Solutions | Technology     | DeepTech US Inc.  | USD      | 35,000,000 | PARTICIPANT | POOL_NOTIONAL_01 |
| CN_PLANT_SH                  | HeavyMetal Mfg     | Industrial     | Shanghai Mfg      | CNY      | 80,000,000 | ISOLATED    | NONE             |
| ... and 12 more accounts ... |                    |                |                   |          |            |             |                  |



Table: payments
Schema:
| payment_id                  | account_id  | amount | currency | counterparty     | purpose | status   | date       |
| --------------------------- | ----------- | ------ | -------- | ---------------- | ------- | -------- | ---------- |
| PMT_001                     | HK_MAIN_HQ  | 2M     | HKD      | Landlord         | RENT    | SETTLED  | 2026-01-10 |
| PMT_102                     | EU_R_D      | 150k   | EUR      | Berlin Tech Park | RENT    | PENDING  | 2026-01-12 |
| PMT_203                     | IN_PLANT_MU | 2M     | INR      | Labor Union      | PAYROLL | REJECTED | 2026-01-10 |
| ... and 6 more payments ... |             |        |          |                  |         |          |            |