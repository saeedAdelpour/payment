# payment App

## Pay your debts with your friends easily with `payment` app

### you can use this app to

- create new persons for your accounting
- create transaction on who must pay and who must be paid
- compute payments: who must pay and who must be paid

This is a GraphQL API, you can read API doc at `/graphql/`

## endpoints

### Query

- `persons`: Get list of all persons
- `compute_payments`: Pass a list of debtors and creditors and price should pay

### Mutation

- `create_person`: Create a person
- `create_transaction`: Pass persons must pay, person that paid and price
