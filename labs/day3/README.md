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

- Ensure Python 3.9+
- From repo root:

```bash
bash labs/day3/run.sh
```

The API starts on http://127.0.0.1:8000

## Example request

```bash
curl -X POST http://127.0.0.1:8000/transaction \
  -H 'Content-Type: application/json' \
  -d '{
    "client_id": "C123",
    "amount": 999.99,
    "currency": "USD",
    "merchant": "ACME",
    "merchant_city": "ONLINE",
    "description": "URGENT VERIFY ACCOUNT EXPIRES TODAY",
    "latitude": 37.7749,
    "longitude": -122.4194
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
