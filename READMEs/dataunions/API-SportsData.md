# SportsData Apis

### Upload CSV - SET

- Description
  - https://github.com/DataUnion-app/Crab/issues/443
- method: POST
- Example
  ```bash
  curl --location 'localhost:8080/api/v1/training/upload-csv' \
  --header 'Authorization: Bearer <access_token>' \
  --form 'file=@"/data/csv/export-Training_Session_67.csv"' \
  --form 'url="https://github.com/DataUnion-app/Crab/files/12831482/export-Training_Session_67.csv"' \
  ```
- Response

  ```JSON
    {
            "_id": "HBjsLAOhRfIKBPf",
            "_rev": "1-45f5a88ef2f8d24c810b64d594c65122",
            "created_at": "2023-10-17T10:51:26.347568UTC",
            "extension": "csv",
            "filename": "export-Training_Session_67.csv",
            "hash": "HBjsLAOhRfIKBPf",
            "public_address": "0xAD143E30AD4852c97716ED5b32d45BcCfF7DEa36",
            "source": "icehockey",
            "status": "Accepted",
            "type": "video",
            "uploaded_by": "0xAD143E30AD4852c97716ED5b32d45BcCfF7DEa36",
            "file_path": "data/0xAD143E30AD4852c97716ED5b32d45BcCfF7DEa36/0xAD143E30AD4852c97716ED5b32d45BcCfF7DEa36-export-Training_Session_67.csv"
        }
  ```

### GET CSV - GET

- Description
  - https://github.com/DataUnion-app/Crab/issues/443
- Example
  ```bash
  curl --location 'localhost:8080/api/v1/training/get_csv?page_no=1&per_page=10' \
    --header 'Content-Type: text/plain' \
    --header 'Authorization: Bearer <access token>' \
  ```
- Response
  - 200
  ```JSON
  "csv": [
        {
            "_id": "HBjsLAOhRfIKBPf",
            "_rev": "1-45f5a88ef2f8d24c810b64d594c65122",
            "created_at": "2023-10-17T10:51:26.347568UTC",
            "extension": "csv",
            "filename": "export-Training_Session_67.csv",
            "hash": "HBjsLAOhRfIKBPf",
            "public_address": "0xAD143E30AD4852c97716ED5b32d45BcCfF7DEa36",
            "source": "icehockey",
            "status": "Accepted",
            "type": "video",
            "uploaded_by": "0xAD143E30AD4852c97716ED5b32d45BcCfF7DEa36",
            "file_path": "data/0xAD143E30AD4852c97716ED5b32d45BcCfF7DEa36/0xAD143E30AD4852c97716ED5b32d45BcCfF7DEa36-export-Training_Session_67.csv"
        }
      ],
      "status": "success"
      }
  ```

### Team Data Overview - GET

- Description
  - https://github.com/DataUnion-app/Crab/issues/463
- Example
  ```bash
  curl --location 'localhost:8080/api/v1/training/team-data-overview?per_page=2&page_no=1' \
    --header 'Content-Type: text/plain' \
    --header 'Authorization: Bearer <access token>' \
  ```
- Response
  - 200
  ```JSON
    {
      "result": [
          {
              "_id": "AYsmBWDgWr",
              "created_at": 1694548363.815951,
              "data_amount": 0,
              "match_files": 0,
              "players": 0,
              "profile": {
                  "user_name": "0xAD14Ea36"
              },
              "public_address": "0xAD143E30AD4852c97716ED5b32d45BcCfF7DEa36",
              "size": 0,
              "team_name": "0xAD14Ea36",
              "trainning_files": 0
          },
          {
              "_id": "IwVuVPsPSV",
              "created_at": 1692971546.63046,
              "data_amount": 206,
              "match_files": 2,
              "players": 206,
              "profile": {
                  "user_name": "data-union-user1"
              },
              "public_address": "0xAD143E30AD4852c97716ED5b32d45BcCfF7DEa32",
              "size": 10.9140625,
              "team_name": "data-union-user1",
              "trainning_files": 2
          }
      ],
      "status": "success"
  }
  ```

### Get Statistics for hockockey data - GET

- Description
  - https://github.com/DataUnion-app/Crab/issues/462
- Example
  ```bash
  curl --location 'localhost:8080/api/v1/training/get-statistics-icehockey-data' \
    --header 'Content-Type: text/plain' \
    --header 'Authorization: Bearer <access token>' \
  ```
- Response
  - 200
  ```JSON
    {
    "result": {
        "amount_of_team": 4,
        "first_data_amount": 200,
        "total_data_amount": 303,
        "user_data_amount": 103
    },
    "status": "success"
  }
  ```

#### Delete uploaded user data - DELETE

- Description
  - https://github.com/DataUnion-app/Crab/issues/465
- method: DELETE
- Example:

  ```bash
  curl --location --request DELETE 'localhost:8080/api/v1/training/delete-csv/<id>' \
  --header 'Authorization: Bearer <access_token>'
  ```

- Responses:

    - 400

  ```JSON
  {
    "messages": [
       "Invalid 'csv_id'"
    ]
  }
  ```

    - 200

  ```JSON
  {
      "status": "success"
  }
  ```
  
### GET CSV by User - GET

- Description
  - https://github.com/DataUnion-app/Crab/issues/464
- Example
  ```bash
  curl --location 'localhost:8080/api/v1/training/get-csv-by-user?page_no=1&per_page=10' \
    --header 'Content-Type: text/plain' \
    --header 'Authorization: Bearer <access token>' \
  ```
- Response
  - 200
  ```JSON
  "csv": [
        {
            "_id": "HBjsLAOhRfIKBPf",
            "_rev": "1-45f5a88ef2f8d24c810b64d594c65122",
            "created_at": "2023-10-17T10:51:26.347568UTC",
            "extension": "csv",
            "filename": "export-Training_Session_67.csv",
            "hash": "HBjsLAOhRfIKBPf",
            "public_address": "0xAD143E30AD4852c97716ED5b32d45BcCfF7DEa36",
            "source": "icehockey",
            "status": "Accepted",
            "type": "video",
            "uploaded_by": "0xAD143E30AD4852c97716ED5b32d45BcCfF7DEa36",
            "file_path": "data/0xAD143E30AD4852c97716ED5b32d45BcCfF7DEa36/0xAD143E30AD4852c97716ED5b32d45BcCfF7DEa36-export-Training_Session_67.csv"
        }
      ],
      "status": "success"
      }
  ```