# Labs: Phase 03 Advanced Querying and Transactions

Difficulty: intermediate to advanced

## Exercise 1
Build a monthly revenue report grouped by category with sum and average values.

Expected check:
- include category, total_revenue, avg_revenue
- sorted by total_revenue descending

## Exercise 2
Create a transfer_credits function that moves credits from one wallet row to another in one transaction.

Expected check:
- when transfer amount is valid, both balances update
- when source balance is insufficient, no balance changes after rollback
