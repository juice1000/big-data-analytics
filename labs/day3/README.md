# Day 3 - Fraud Detection Pipeline App

We want to build a whole data processing pipeline around the topic we've had in day1 and day2: Banking Fraud detection

These are the components:

### API request

- We will do a POST request to a FastAPI endpoint /transaction which gets a transaction in JSON format

### Load Data / Preprocess

- We will load it into a Python script and extract the data (we expect clean data)

### Data Lakehouse

- an sqlite database having past transactions

### Whitelisting (Filtern)

- we will decide with past data from the same user if the transaction is unusual (geolocation and amount)

### Evaluation (ML)

- we will analyze the description with LLM and let it evaluate whether it's suspicious

### Action (Alert)

- if suspicious, we print ("alert, suspicious action")

## Run locally

- Ensure Python 3.12+
- execute python script `main.py`

The API starts on http://127.0.0.1:8080

## Example request (schema)

```bash
curl -X POST http://127.0.0.1:8080/transaction \
  -H 'Content-Type: application/json' \
  -d '{
    "id": null,
    "date": "2025-08-12T10:00:00Z",
    "client_id": "C123",
    "card_id": "CARD-001",
    "amount": 999.99,
    "currency": "USD",
    "use_chip": "Yes",
    "merchant_id": "ACME-001",
    "merchant_city": "ONLINE",
    "merchant_state": "CA",
    "zip": "94105",
    "mcc": 6011,
    "errors": "URGENT VERIFY ACCOUNT EXPIRES TODAY",
    "flagged_fraud": null,
    "is_fraud": null
  }'
```

Response:

```json
{
  "suspicious": true,
  "reason": "multiple fraud keywords",
  "score": 0.9
}
```
