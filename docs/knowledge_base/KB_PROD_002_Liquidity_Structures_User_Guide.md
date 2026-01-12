# PRODUCT USER GUIDE: GLOBAL LIQUIDITY MANAGEMENT STRUCTURES
**Classification:** Confidential - Internal Treasury Use
**Scope:** HK, SG, UK, US, BR Entities

## 1. Physical Cash Concentration (Zero Balancing - ZBA)
**Definition:** An automated mechanism that physically moves funds between participant accounts and a header account to zero-out balances daily.

### Operational Mechanics
- **Sweep Time:** End of Day (EOD) approx. 22:00 Local Time.
- **Direction:**
  - *Surplus Accounts:* Balance swept TO Header.
  - *Deficit Accounts:* Funds swept FROM Header to cover overdrafts.
- **Accounting:** Creates an Intercompany Loan (ICL) daily. Interest on ICLs must be tracked for tax purposes (Transfer Pricing).
- **Applicability:** Used for USD (New York), HKD (Hong Kong), GBP (London).
- **Restrictions:** 
  - **Brazil:** ZBA is NOT permitted due to IOF tax on every sweep.
  - **China:** Requires Entrusted Loan framework if entities are not 100% owned.

## 2. Notional Pooling (Interest Optimization)
**Definition:** A mechanism where balances are *not* physically moved. The bank calculates interest based on the *net* position of the group.

### Operational Mechanics
- **No Physical Movement:** Underlying accounts retain their balances.
- **Interest Calculation:** Bank pays credit interest on the Net Group Position (Long + Short).
- **Cross-Currency:** "Multi-Currency Notional Pool" allows offsetting USD overdrafts against HKD surplus without FX conversion.
- **Legal Requirements:** Requires a Cross-Guarantee and Indemnity clause signed by all participants.
- **Regulatory Barriers:**
  - **Prohibited Jurisdictions:** Brazil, India, Mainland China (Strict separation of funds).
  - **Basel III Impact:** Banks charge higher fees for Notional Pools due to higher capital usage (Gross-up rule).

## 3. Virtual Accounts (VA) for Receivables
**Definition:** Dummy account numbers assigned to specific payers (customers) that map to a single physical bank account.

### Use Case
- **Reconciliation:** e.g., Assign VA `888-0001` to Customer A. When a payment hits, the ERP system automatically matches it to Customer A's invoice.
- **Structure:** 
  - *Static VAs:* Permanent VAs assigned to regular buyers.
  - *Dynamic VAs:* Unique VAs generated for a single invoice.

