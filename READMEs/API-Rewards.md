# Rewards rest apis

#### /api/v1/rewards/claim

- method: POST
- Authorization header (required): Bearer token
- Parameters:
    - `source`: string. Optional. Possible values: `brainstem`/`wedatanation`
- Example
  ```
  curl --location --request POST 'http://localhost:8080/api/v1/rewards/claim' \
  --header 'Authorization: Bearer <access_token>' \
  --header 'Content-Type: application/json' \
  --data-raw '{
    "entity_type": "image"
  }'
  ```
- Response
  ```JSON
  {
    "transaction_hash" : "123..."
  }
  ```

#### /api/v1/rewards/

- method: GET
- Authorization header (required): Bearer token
- Description: Returns the amount in Wei the user can claim.
- Parameters:
    - `source`: string. Optional. Possible values: `brainstem`/`wedatanation`
    - `include_today` : boolean. Optional. Possible values: `true`/`false`
- Example
  ```
  curl --location --request GET 'localhost:8080/api/v1/rewards/?entity_type=image' \
  --header 'Authorization: Bearer <bearer_token>' \
  --data-raw ''
  ```
- Response
  ```JSON
  {
    "amount": 400000000000000000,
    "end_date": "06-03-2022",
    "start_date": "01-01-2021"
  }
  ```

#### /api/v1/rewards/list

- method: GET
- Authorization header (required): Bearer token
- Description: Returns the list of claims with status, amount, start_date, and end_date if applicable. 
  User can claim rewards only upv to yesterday from the current date. sCurrent date's rewards can be claim on the next day.
- Example
  ```
  curl --location --request GET 'localhost:8080/api/v1/rewards/list?entity_type=image&page=1' \
  --header 'Authorization: Bearer <bearer_token>' \
  --data-raw ''
  ```
- Response
  ```JSON
  {
    "result": [
        {
            "amount": null,
            "end_date": "20-10-2021",
            "start_date": "20-10-2021",
            "status": "failed",
            "transaction_hash": null,
            "reason": "Reward amount is 0"
        },
        {
            "amount": 400000000000000000,
            "end_date": "20-10-2021",
            "start_date": "19-10-2021",
            "status": "transfer_succeeded",
            "transaction_hash": "0x053389dec2c8d1e0954b59f0afaa4a39e3ad8183adb32a93394104f03ec398d4"
        },
        {
            "amount": 300000000000000064,
            "end_date": "19-10-2021",
            "start_date": "01-01-2021",
            "status": "transfer_succeeded",
            "transaction_hash": "0x053389dec2c8d1e0954b59f0afaa4a39e3ad8183adb32a93394104f03ec398d4"
        }
    ]
  }
  ```

#### /api/v1/rewards/total-rewards

- method: GET
- Authorization header (required): Bearer token
- Description: Api returns sum of all the rewards successfully transferred to user.
- Example
  ```
  curl --location --request GET 'localhost:8080/api/v1/rewards/total-rewards' \
  --header 'Authorization: Bearer <bearer_token>' \
  --data-raw ''
  ```
- Response
  ```JSON
  { "result": 200000000000000000 }
  ```
