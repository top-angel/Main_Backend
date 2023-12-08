#### Get pending notifications

- Parameters
  - Body:
    - `mark_as_read`: An optional boolean flag. Defaults to `true`
- Example:
    ```bash
    curl --location --request POST 'http://localhost:8080/api/v1/other/notifications' \
    --header 'Authorization: Bearer <accesstoken>' \
    --header 'Content-Type: application/json' \
    --data-raw '{
        "mark_as_read": false
    }'
    ```
  - Response:
    - 200
      ```bash
      [
        {
            "created_at": "2023-01-06T22:20:39.386409",
            "data": {
                "message": "A new user joined with your referral id!"
            },
            "id": "notification-iWIyfLKfIb",
            "type": "referral_used"
        },
        {
            "created_at": "2023-01-06T22:26:34.900609",
            "data": {
                "new-rank": 2
            },
            "id": "notification-IzoGMlIhEa",
            "type": "rank_updated"
        }
      ]
      ```
    