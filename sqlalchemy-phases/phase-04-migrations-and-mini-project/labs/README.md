# Labs: Phase 04 Migrations and Mini Project

Difficulty: advanced

## Exercise 1
Create a mini bookstore workflow with models:
- Customer
- Book
- BookOrder
- BookOrderItem

Tasks:
- insert sample order data
- generate report: top 3 books by quantity sold
- generate report: total spend by customer

Expected check:
- output includes ranked list of books
- output includes customer totals sorted descending

## Exercise 2
Write migration notes:
- add discount_percent column to order table
- backfill existing rows with 0
- ensure nullable=false in final schema
