# Brainstem apis

#### Access token

View [/login API](../API-Authentication.md) with source `brainstem`.

#### Upload hearbeat file

- method: GET
- Parameters
    - `file-type` Required. `heartbeat`/`hbr_rr`/``
- Example
    ```bash
    curl --location --request POST 'http://localhost:8080/api/v1/upload-file' \
    --header 'Authorization: Bearer <access_token>' \
    --form 'file=@"<file_path>"' \
    --form 'file-type="heartbeat"'
    ```
- Response
  ```JSON
  {
    "id": "WQlsELAuQzjlMQv",
    "message": "File successfully uploaded"
  }
  ```

### Get list of downloadable files

- Description
    - Requires user with role `download`
- Example
  ```bash
  curl --location --request GET 'http://localhost:8080/api/v1/metadata/query-view?design-doc=brainstem&view=downloadables&query-type=all&type=metadata' \
  --header 'Authorization: Bearer <access_token>'
  ```
- Response
  ```JSON
  {
    "result": [
        {
            "file_name": "x17.nn.txt",
            "file_type": "heartbeat",
            "id": "OGxJfGeOaBGQXrH",
            "type": "text"
        },
        {
            "file_name": "x18.nn.txt",
            "file_type": "heartbeat",
            "id": "1234567890",
            "type": "text"
        }
    ]
  }
  ```

#### Download a file

- Description
    - Requires user with role `download`
- Example
  ```bash
   curl --location --request GET 'http://localhost:8080/api/v1/download/ZwuDIxsQxqwynEf' \
  --header 'Authorization: Bearer <access_token>'
  ```

### Create a data share

- Description
    - Create a Data NFT for the user if not exists
    - Create a Data Token
- Example
  ```bash
  curl --location --request POST 'http://localhost:8080/api/v1/metadata/create-data-share' --header 'Authorization: Bearer <access_token>'
  ```
- Response
  ```JSON
  {
    "result": {
      "data_nft_address": "0xb8cb616877403C466584Af3656bAaC33C8D94Cb0",
      "data_share_id": "rcxndQovGcGhNBZ",
      "data_token_address": "0x4CbD9f7175974DB73Cff5B4FFcD3Dbe3e398Be09"
    }
  }
  ```

### Share data to the consumer

- Description
    - Mint Data Token to the consumer
- Example
  ```bash
  curl --location --request POST 'http://localhost:8080/api/v1/metadata/share-data?to_address=<to_address>&data_share_id=<data_share_id>' \
  --header 'Authorization: Bearer <access_token>'
  ```
- Response
  ```JSON
  {
    "result": {
      "data_share_id": "rcxndQovGcGhNBZ",
      "mint_tx": "0xa6f07d91a0d827926e091a47cc4432b64fafccf06cd4f0ab5583e23615bd53cf"
    }
  }
  ```

### Share data(when the consumer clicks the link)

- Description
    - Mint Data Token to the consumer
- Example
  ```bash
  curl --location --request POST 'http://localhost:8080/api/v1/metadata/consumer-share-data?data_share_id=<data_share_id>' \
  --header 'Authorization: Bearer <access_token>'
  ```
- Response
  ```JSON
  {
    "result": {
      "data_share_id": "rcxndQovGcGhNBZ",
      "mint_tx": "0xa6f07d91a0d827926e091a47cc4432b64fafccf06cd4f0ab5583e23615bd53cf"
    }
  }
  ```

### Download Data Share

- Description
    - Consumer should spend datatoken before calling this api
    - Download all data as zip that the sharer uploaded
- Example
  ```bash
  curl --location --request GET 'http://192.168.110.67:8080/api/v1/compute/data/download-share-data-zip/<access_token>?data_share_id=<data_share_id>&order_tx_hash=<order_tx_hash>'
  ```

### Report Data Share

- Description
    - Report data share
- Example
  ```bash
  curl --location --request POST 'http://localhost:8080/api/v1/compute/data/report-share-data/<access_token>' \
  --header 'Content-Type: application/json' \
  --data '{
      "entity_id": "<data_share_id>",
      "annotations":[
          {
              "type": "data_share_report",
              "data": "<content>"
          }
      ]
  }'

### Get Reports of Data Share

- Description
    - Report data share
- Example
  ```bash
  curl --location --request GET 'http://localhost:8080/api/v1/compute/data/share-data-reports/<access_token>' \
  --header 'Content-Type: application/json' \
  --data '{
      "entity_id": "<data_share_id>",
      "annotations":[
          {
              "type": "data_share_report",
              "data": "<content>"
          }
      ]
  }'
  ```

### Get tokens list

- Description
    - Get tokens list of a wallet
- Example
  ```bash
  curl --location --request GET 'http://localhost:8080/api/v1/metadata/tokens-list?wallet_address=<wallet_address>' \
  --header 'Authorization: Bearer <access_token>'
  ```

### Get data share by data token address

- Description
    - Get data share by data token address
- Example
  ```bash
  curl --location --request GET 'http://localhost:8080/api/v1/metadata/data-share-by-data-token-address?data_token_address=<address>' \
  --header 'Authorization: Bearer <access_token>'
  ```

