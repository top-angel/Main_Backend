## Handshake

#### api/v1/handshake/all

- method: GET
- Example:

  ```bash
  curl --location --request GET 'localhost:8080/api/v1/handshake/all'
  ```

- Responses:
  - 200
  ```JSON
  {
    "status": "success",
    "result": [
      {
        "handshake_id": "2342343242",
        "created_time": "2022-11-14T00:55:31.820Z",
        "location": {
          "latitude": "latitudexx",
          "longitude": "longitudexx"
        },
        "initiated_by": "address1",
        "completed_by": "address2"
      }
    ]
  }
  ```

#### api/v1/handshake/create

- method: POST
- Authorization header (required): Bearer token
- Example:

  ```bash
  curl --location --request POST 'localhost:8080/api/v1/handshake/create' \
  --header 'Authorization: Bearer <access_token>' \
  --header 'Content-Type: application/json' \
  --data-raw '{
    "latitude": "xxx",
    "longitude": "xxxx",
    "initiated_by" : "address"
  }'
  ```

- Responses:

  - 400

    ```JSON
    {
      "status": "failed",
      "messages": [
        "error message"
      ]
    }
    ```

  - 200
    ```JSON
    {
      "status": "success",
      "id": "VBrICYYQUy"
    }
    ```
