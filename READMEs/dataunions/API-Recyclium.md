# Recyclium Apis

### Creator Registration
- Description
  - https://github.com/DataUnion-app/Crab/issues/480
- Example
  ```bash
  curl --location 'localhost:8080/register-creator' \
  --form 'public_address="0x1234"' \
  --form 'source="recyclium"' \
  --form 'email="example@dataunion.com"' \
  --form 'company_title="dataunion"' \
  --form 'address="address"' \
  --form 'country="US"' \
  --form 'image=@"/path/to/file"'
  ```

- Response
  ```JSON
  {
    "nonce": "nonce"
    "status": "success"
  }
  ```

### Collector Registration
- Description
  - https://github.com/DataUnion-app/Crab/issues/480
- Example
  ```bash
  curl --location 'localhost:8080/register-collector' \
  --form 'public_address="0x1234"' \
  --form 'source="recyclium"' \
  --form 'first_name="First"' \
  --form 'last_name="Last"' \
  --form 'image=@"/path/to/file"'
  ```

- Response
  ```JSON
  {
    "nonce": "nonce"
    "status": "success"
  }
  ```

### Storer Registration
- Description
  - https://github.com/DataUnion-app/Crab/issues/480
- Example
  ```bash
  curl --location 'localhost:8080/register-storer' \
  --form 'public_address="0x1234"' \
  --form 'source="recyclium"' \
  --form 'name="storer name"' \
  --form 'address="address"' \
  --form 'lat="100"' \
  --form 'lng="100"' \
  --form 'postalCode="12345"' \
  --form 'city="New York"' \
  --form 'country="US"' \
  --form 'worktime="From 8a to 5p"' \
  --form 'storageSpace="100"' \
  ```

- Response
  ```JSON
  {
    "nonce": "nonce"
    "status": "success"
  }
  ```

### Creator profile API - get

- Description
  - https://github.com/DataUnion-app/Crab/issues/350
- Example
  ```bash
  curl --location 'localhost:8080/api/v1/creator/:id' \
    --header 'Authorization: Bearer <access token>'
  ```
- Response
  ```JSONQ
  {
    "creator": {
        "address": "address",
        "company_title": "data-union",
        "country": "country",
        "email": "test@domain.com"
    },
    "status": "success"
  }
  ```

### Creator profile API - set

- Description
  - https://github.com/DataUnion-app/Crab/issues/350
- Example
  ```bash
  curl --location --request PUT 'localhost:8080/api/v1/creator/:id' \
    --header 'Content-Type: text/plain' \
    --header 'Authorization: Bearer <access token>' \
    --data-raw '{
        "email" : "test@domain.com",
        "company_title" : "data-union",
        "address" : "address",
        "country" : "country"
    }'
  ```
- Response
  ```JSON
  {
    "status": "success"
  }
  ```

### Creator API - /api/v1/creators - POST

- Description
  - End-point to fetch all creators by admin. This is private route.
- Example
  ```bash
  curl --location --request POST 'localhost:8080/api/v1/creators' \
    --header 'Content-Type: text/plain' \
    --header 'Authorization: Bearer <access token>' \
    --data-raw '{
      "page_no": 2,
      "per_page": 10,
      "sort": "desc"
    }'
  ```
- Response
  - 200
  ```JSON
  {
    "status": "success",
    "creators": [
      ...
    ]
  }
  ```

### Verificiation Queue API

- Description
  - https://github.com/DataUnion-app/Crab/issues/355
- Example
  ```bash
  curl --location --request GET 'localhost:8080/api/v1/users/pending?page_size=2&page=1&role=creator' \
    --header 'Content-Type: text/plain' \
    --header 'Authorization: Bearer <access token>'
  ```
- Response
  ```JSON
  {
    "pending_users": [
        {
            "_id": "MHtQIqvoNX",
            "claims": [
                "creator"
            ]
        },
        {
            "_id": "gfMrxNmJme",
            "claims": [
                "creator"
            ],
            "profile": {
                "address": "address",
                "company_title": "data-union",
                "country": "country",
                "email": "test@domain.com"
            }
        }
    ],
    "status": "success"
  }
  ```

### Storer profile API - get

- Description
  - Get profile for given storer. For more info, see https://github.com/DataUnion-app/Crab/issues/351
- Example
  ```bash
  curl --location 'localhost:8080/api/v1/storer/:id' \
    --header 'Authorization: Bearer <access token>'
  ```
- Response
  - 200
  ```JSON
  {
    "status": "success",
    "storer": {
        "address": "Mission Street 123",
        "city": "New York",
        "country": "USA",
        "geocode": {
            "lat": 23.456,
            "lng": 25.6987
        },
        "name": "Rob Lawson",
        "postalCode": "432A",
        "storageSpace": 40000,
        "worktime": "Mon-Fri 10.00-18.00"
    }
  }
  ```

### Storer profile API - set

- Description
  - Set profile for given storer. For more info, see https://github.com/DataUnion-app/Crab/issues/351
- Example
  ```bash
  curl --location --request PUT 'localhost:8080/api/v1/storer/:id' \
    --header 'Content-Type: text/plain' \
    --header 'Authorization: Bearer <access token>' \
    --data-raw '{
      "name": "Rob Lawson",
      "address": "Mission Street 123",
      "geocode": {
        "lat": 23.456,
        "lng": 25.6987
      },
      "postalCode": "432A",
      "city": "New York",
      "country": "USA",
      "worktime": "Mon-Fri 10.00-18.00",
      "storageSpace": 40000
    }'
  ```
- Response
  - 200
  ```JSON
  {
    "status": "success"
  }
  ```

### Storer API - /api/v1/storers

- Description
  - End-point to fetch all storers by admin. This is private route.
- Example
  ```bash
  curl --location --request POST 'localhost:8080/api/v1/storers' \
    --header 'Content-Type: text/plain' \
    --header 'Authorization: Bearer <access token>' \
    --data-raw '{
      "page_no": 2,
      "per_page": 10,
      "sort": "desc"
    }'
  ```
- Response
  - 200
  ```JSON
  {
    "status": "success",
    "storers": [
      ...
    ]
  }
  ```

### Search bar API

- Description
  - https://github.com/DataUnion-app/Crab/issues/358
- method: GET
- Parameters
  - `query`: Optional string
  - `role`: Optional string, ex: `CREATOR`, `STORER`, `USER`, `RECYCLER`
- Example
  ```bash
  curl --location 'localhost:8080/api/v1/user?query=User&role=STORER' \
    --header 'Authorization: Bearer <access token>' \
  ```
- Response
  ```JSON
    {
      "storer": [
          {
              "_id": "MHtQIqvoNX",
              "DID": "did:example:123456789abcdefghijk",
              "public_address": "0xAD143E30AD4852c97716ED5b32d45BcCfF7DEa36",
              "avatar_url": "avatar_url",
              "missions_count": 0,
              "profile": {
                  "name": "Username"
              },
              "returned_count": 482,
              "scanned_count": 25,
              "stored_count": 56
          }
      ]
  }
  ```

### Bounty State Change API

- Description
  - https://github.com/DataUnion-app/Crab/issues/360
- method: PUT
- Parameters
  - `state`: Required string, ex: `verified`, `in_progress`, `declined`, `completed`
- Example
  ```bash
  curl --location --request PUT 'localhost:8080/api/v1/bounty/:id' \
    --header 'Content-Type: text/plain' \
    --header 'Authorization: Bearer <access token>' \
    --data '{
      "state": "declined"
    }'
  ```
- Response
  ```JSON
  {
      "result": "declined"
  }
  ```

### Status profile API - get

- Description
  - https://github.com/DataUnion-app/Crab/issues/364
- method: GET
- Example
  ```bash
  curl --location --request GET 'localhost:8080/api/v1/user/:id/profile' \
    --header 'Content-Type: text/plain' \
    --header 'Authorization: Bearer <access token>' \
  ```
- Response
  ```JSON
  {
    "status": "inactive",
    "status_reason": "reasons"
  }
  ```

### Status profile API - set

- Description
  - https://github.com/DataUnion-app/Crab/issues/364
- method: PUT
- Parameters
  - `status`: Required string, ex: `new`, `active`, `inactive`
  - `status_reason`: Optional string,
- Example
  ```bash
  curl --location --request PUT 'localhost:8080/api/v1/user/:id/profile' \
    --header 'Content-Type: text/plain' \
    --header 'Authorization: Bearer <access token>' \
    ---data '{
        "status" : "inactive",
        "status_reason" : "reasons"
  ```

### Incident API - GET

- Description
  - https://github.com/DataUnion-app/Crab/issues/366
- method: GET
- Parameters
  - `user_id`: Optional string
- Example
  ```bash
  curl --location --request GET 'localhost:8080/api/v1/user/incidents?user_id=IwVuVPsPSV' \
    --header 'Content-Type: text/plain' \
    --header 'Authorization: Bearer <access token>' \
  ```
- Response
  ```JSON
    {
        "result": {
            "result": [
                {
                    "_id": "WImkpPXCwScZuwm",
                    "_rev": "1-70a7d34a437b91b8ae75587eb256a082",
                    "created_at": "2023-11-28T20:09:06.457105UTC",
                    "description": "reason",
                    "user_id": "IwVuVPsPSV"
                }
            ]
        },
        "status": "success"
    }
  ```

### Incident API - SET

- Description
  - https://github.com/DataUnion-app/Crab/issues/366
- method: POST
- Parameters
  - `user_id`: Required string
  - `description`: Required string
- Example
  ```bash
  curl --location 'localhost:8080/api/v1/user/incidents' \
    --header 'Content-Type: application/json' \
    --header 'Authorization: Bearer <access token>' \
    --data '{
        "user_id" : "IwVuVPsPSV",
        "description" : "reason"
      }'
  ```
- Response

  ```JSON
  {
    "status": "success"
  }
  ```

  #### Implement Earning Over Time API

- method: GET
- Parameters:
  - start_date: (Required) Date in 'YYYY-mm-dd' format
  - end_date: (Required) Date in 'YYYY-mm-dd' format
  - public address: (Optional) string but required for Admin role
- Example:

  ```bash
    curl --location 'localhost:8080/api/v1/rewards/user?public_address=address&start_date=2023-06-21&end_date=2023-09-01' --header 'Authorization: Bearer <access_token>'
  ```

- Response:
  ```JSON
    {
      "result": 1650000000000000000
    }
  ```

### Bounty Verificiation Queue API

- Description
  - https://github.com/DataUnion-app/Crab/issues/376
- method: GET
- Parameters
  - `page_size`: Optional string
  - `page`: Optional string
- Example
  ```bash
    curl --location 'localhost:8080/api/v1/bounty/pending?page_size=2&page=1' \
    --header 'Content-Type: text/plain' \
    --header 'Authorization: Bearer <access token>'
      "status": "success"
  }
  ```

### Collector API - /api/v1/collectors

- Description
  - End-point to fetch all collectors by admin. This is private route.
- Example
  ```bash
  curl --location --request POST 'localhost:8080/api/v1/collectors' \
    --header 'Content-Type: text/plain' \
    --header 'Authorization: Bearer <access token>' \
    --data-raw '{
      "page_no": 2,
      "per_page": 10,
      "sort": "desc"
    }'
  ```
- Response
  - 200
  ```JSON
  {
    "status": "success",
    "collectors": [
      ...
    ]
  }
  ```

### Most active location API for bounty

- Description
  - https://github.com/DataUnion-app/Crab/issues/380
- method: GET
- Example
  ```bash
  curl --location 'http://localhost:8080/api/v1/metadata/active-location' \
    --header 'Content-Type: text/plain' \
    --header 'Authorization: Bearer <access token>' \
  ```
- Response

  ```JSON
    {
      "result": [
          {
              "bounty_id": "bounty:YMcKmgOGjWfuRrO",
              "key": [
                  "bounty:YMcKmgOGjWfuRrO",
                  -11.538357847732584,
                  30.149940940197382
              ],
              "value": 6
          },
          {
              "bounty_id": "bounty:buGwTtEaxfYKVqp",
              "key": [
                  "bounty:buGwTtEaxfYKVqp",
                  -126.9929952577326,
                  63.35229010100258
              ],
              "value": 4
          },
          ... ...
   ]
  }

### Creator status API - set

- Description: https://github.com/DataUnion-app/Crab/issues/403

- Example

```bash
curl --location --request PUT 'localhost:8080/api/v1/creator/status/:id' \
  --header 'Content-Type: text/plain' \
  --header 'Authorization: Bearer <access token>' \
  --data-raw '{
    "status": "verified"
  }'
```

- Response

```JSON
{
  "status": "success"
}
```

### Creator status API - get

- Description: https://github.com/DataUnion-app/Crab/issues/403

- Example

```bash
curl --location --request GET 'localhost:8080/api/v1/creator/status/:id' \
  --header 'Content-Type: text/plain' \
  --header 'Authorization: Bearer <access token>' \
  --data-raw '{
    "status": "verified"
  }'
```

- Response

```JSON
{
  "creator": "verified",
  "status": {
    ...
  }
}
```

### Recent Verified API
- Description
    - https://github.com/DataUnion-app/Crab/issues/392
- method: GET
- Example
  ```bash
  curl --location --request GET 'localhost:8080/api/v1/users/verified' \
    --header 'Content-Type: text/plain' \
    --header 'Authorization: Bearer <access token>' \
  ```
- Response
  ```JSON
    {
      "status": "success",
      "verified_users": [
          {
              "_id": "IwVuVPsPSV",
              "created_at": 1692971546.63046,
              "profile": null,
              "public_address": "test@domain.com",
              "status": "verified"
          },
          {
              "_id": "wNAQKuyGKY",
              "created_at": 1692971495.119224,
              "profile": null,
              "public_address": "0xDF1dec52e60202be27b0644eA0F584B6eb5CE4EB",
              "status": "verified"
          },
          {
              "_id": "ZjDQMhshYF",
              "created_at": 1691695844.852333,
              "public_address": "0xAD143E30AD4852c97716ED5b32d45BcCfF7DEa36",
              "status": "verified"
          }
      ]
  }

### Set DID User API - SET

- Description
    - https://github.com/DataUnion-app/Crab/issues/402
- method: POST
- Parameters
    - `DID`: Required string
- Example
  ```bash
  curl --location --request PUT 'localhost:8080/api/v1/user/did/:id' \
    --header 'Content-Type: text/plain' \
    --header 'Authorization: Bearer <access token>' \
    --data '{
      "DID" : "did:example:123456789abcdefghijk"
    }'
  ```
- Response
  ```JSON
  {
    "status": "success"
  }
  ```

### Get DID User API - GET

- Description
    - https://github.com/DataUnion-app/Crab/issues/402
- method: GET
- Example
  ```bash
  curl --location 'localhost:8080/api/v1/user/did/:id' \
    --header 'Content-Type: text/plain' \
    --header 'Authorization: Bearer <access token>' \
  ```
- Response
  ```JSON
    {
      "status": "success",
      "User": [
          {
              "DID": "did:example:123456789abcdefghijk",
              "_id": "ZjDQMhshYF",
              "claims": [
                  "user"
              ],
              "public_address": "0xAD143E30AD4852c97716ED5b32d45BcCfF7DEa36s"
          }
      ],
      "status": "success"
  }
  ```

### Get All DID User API - GET

- Description
    - https://github.com/DataUnion-app/Crab/issues/402
- method: GET
- Example
  ```bash
  curl --location 'localhost:8080/api/v1/user/get_all_did' \
    --header 'Content-Type: text/plain' \
    --header 'Authorization: Bearer <access token>' \
  ```
- Response
  ```JSON
    {
    "User": [
        {
            "DID": "did:example:523456789abcdefghijz",
            "_id": "IwVuVPsPSV",
            "claims": [
                "creator",
                "admin"
            ],
            "public_address": "0xDF1dec52e60202be27b0644eA0F584B6eb5CE4EB"
        },
        {
            "DID": "did:example:123456789abcdefghijk",
            "_id": "ZjDQMhshYF",
            "claims": [
                "user"
            ],
            "public_address": "0xAD143E30AD4852c97716ED5b32d45BcCfF7DEa36s"
        }
    ],
    "status": "success"
  }
  ```

### Collector profile API - get
- Description
    - https://github.com/DataUnion-app/Crab/issues/398
- method: GET
- Example
  ```bash
  curl --location 'localhost:8080/api/v1/user/collector/:id' \
    --header 'Authorization: Bearer <access token>'
  ```
- Response
  ```JSON
  {
    "collector": {
        "user_name": "data-union-user"
    },
    "status": "success"
  }
  ```

### Collector profile API - set 
- Description
    - https://github.com/DataUnion-app/Crab/issues/398
- method: PUT
- Parameters
    - `user_name`: Required string
- Example
  ```bash
  curl --location --request PUT 'localhost:8080/api/v1/user/collector/:id' \
    --header 'Content-Type: text/plain' \
    --header 'Authorization: Bearer <access token>' \
    --data-raw '{
        "user_name" : "data-union-user"
    }'
  ```
- Response
  ```JSON
  {
    "status": "success"
  }
  ```

### GET Amount Storer and Collector by Mission ID - GET
- Description
    - https://github.com/DataUnion-app/Crab/issues/383
- method: GET
- Example
  ```bash
  curl --location 'localhost:8080/api/v1/missions/get_amount_storer_collector/:id' \
    --header 'Authorization: Bearer <access token>'
  ```
- Response
  ```JSON
  {
    "result": {
        "collector_amount": 15,
        "storer_amount": 6
    },
    "status": "success"
  }
  ```

### GET All Missions Payout Statistics Info by Creator ID - GET
- Description
    - https://github.com/DataUnion-app/Crab/issues/408
- method: GET
- Example
  ```bash
  curl --location 'localhost:8080/api/v1/missions/get_all_missions_info/:creator_id' \
    --header 'Authorization: Bearer <access token>'
  ```
- Response
  ```JSON
    {
      "result": [
          {
              "collector_amount": 5,
              "collector_reward": 0,
              "mission_id": "mission:BzdxQYZMAcqNprc",
              "storer_amount": 3
          },
          {
              "collector_amount": 6,
              "collector_reward": 0,
              "mission_id": "mission:CGNDHKkDvLqlwvT",
              "storer_amount": 3
          },
          {
              "collector_amount": 1,
              "collector_reward": 0,
              "mission_id": "mission:FYvIyAGEJZezYpT",
              "storer_amount": 2
          }
      ],
      "status": "success"
  }
  ```

### GET Total Missions Payout Statistics Info by Creator ID - GET
- Description
    - https://github.com/DataUnion-app/Crab/issues/407
- method: GET
- Example
  ```bash
  curl --location 'localhost:8080/api/v1/missions/get_total_missions_info/:creator_id' \
    --header 'Authorization: Bearer <access token>'
  ```
- Response
  ```JSON
  {
    "collector_amount": 12,
    "collector_reward": 0,
    "storer_amount": 8,
    "status": "success",

  }
  ```

### Product API - Create(Creator)

- Description
  - https://github.com/DataUnion-app/Crab/issues/393
- method: POST
- Example
  ```bash
  curl --location --request POST 'localhost:8080/api/v1/product/create' \
  --header 'Authorization: Bearer <access_token>' \
  --form 'name="Product Name"' \
  --form 'material_type="Material Type"' \
  --form 'material_size="10"' \
  --form 'example_image=@"/path/to/file"' \
  ```
- Response

  ```JSON
  {
    "result":
      {
        "_id": "GpvNnGXqESbdfRv",
        "_rev": "1-0c5ba4318cdeb12339b33eabb8164f6f",
        "created_at": "2023-10-10T01:42:23.916068UTC",
        "example_image": "data/0xBB1dda5aFD95A93acB9527e2c262d55B410B58A5/products/cm.jpg",
        "material_size": null,
        "material_type": "Type",
        "name": "First Product",
        "public_address": "0xBB1dda5aFD95A93acB9527e2c262d55B410B58A5",
        "source": "recyclium"
      }
  }
  ```

### Product API - Get my products(Creator)

- Description
  - https://github.com/DataUnion-app/Crab/issues/393
- method: GET
- Example
  ```bash
  curl --location --request GET 'localhost:8080/api/v1/product/my-products' \
  --header 'Authorization: Bearer <access_token>' \
  ```
- Response

  ```JSON
  {
    "result": [
      {
        "_id": "GpvNnGXqESbdfRv",
        "_rev": "1-0c5ba4318cdeb12339b33eabb8164f6f",
        "created_at": "2023-10-10T01:42:23.916068UTC",
        "example_image": "data/0xBB1dda5aFD95A93acB9527e2c262d55B410B58A5/products/cm.jpg",
        "material_size": null,
        "material_type": "Type",
        "name": "First Product",
        "public_address": "0xBB1dda5aFD95A93acB9527e2c262d55B410B58A5",
        "source": "recyclium"
      }
    ]
  }
  ```

### Product API - Get all products(Recyclium Admin)

- Description
  - https://github.com/DataUnion-app/Crab/issues/393
- method: GET
- Example
  ```bash
  curl --location --request GET 'localhost:8080/api/v1/product/all' \
  --header 'Authorization: Bearer <access_token>' \
  ```
- Response

  ```JSON
  {
    "result": [
      {
        "_id": "GpvNnGXqESbdfRv",
        "_rev": "1-0c5ba4318cdeb12339b33eabb8164f6f",
        "created_at": "2023-10-10T01:42:23.916068UTC",
        "example_image": "data/0xBB1dda5aFD95A93acB9527e2c262d55B410B58A5/products/cm.jpg",
        "material_size": null,
        "material_type": "Type",
        "name": "First Product",
        "public_address": "0xBB1dda5aFD95A93acB9527e2c262d55B410B58A5",
        "source": "recyclium"
      }
    ]
  }
  ```

### Product API - Get product by id

- Description
  - https://github.com/DataUnion-app/Crab/issues/393
- method: GET
- Example
  ```bash
  curl --location --request GET 'localhost:8080/api/v1/product/get/<id>' \
  --header 'Authorization: Bearer <access_token>' \
  ```
- Response

  ```JSON
  {
    "result": [
      {
        "_id": "GpvNnGXqESbdfRv",
        "_rev": "1-0c5ba4318cdeb12339b33eabb8164f6f",
        "created_at": "2023-10-10T01:42:23.916068UTC",
        "example_image": "data/0xBB1dda5aFD95A93acB9527e2c262d55B410B58A5/products/cm.jpg",
        "material_size": null,
        "material_type": "Type",
        "name": "First Product",
        "public_address": "0xBB1dda5aFD95A93acB9527e2c262d55B410B58A5",
        "source": "recyclium"
      }
    ]
  }
  ```

### Product API - Get product example image by id

- Description
  - https://github.com/DataUnion-app/Crab/issues/393
- method: GET
- Example
  ```bash
  curl --location --request GET 'localhost:8080/api/v1/product/<id>/example_image' \
  --header 'Authorization: Bearer <access_token>' \
  ```

#### Create QR code upload API

- Description
  - https://github.com/DataUnion-app/Crab/issues/440
- method: POST
- Example
  ```bash
  curl --location --request POST 'localhost:8080/api/v1/product/upload-qrcode' \
  --header 'Authorization: Bearer <access_token>' \
  --form 'file=@"<file_path>"' \
  --form 'bounty_id="<bounty_id>"' \
  --form 'batch_name="Batch Name"' \
  --form 'product_id="<product_id>"' \
  ```
- Response

  ```JSON
  {
    "id": "<id>",
    "status": "success"
  }
  ```

  ```
### GET Aggregated data API - verified storer flow - GET
- Description
    - https://github.com/DataUnion-app/Crab/issues/417
- method: GET
- Example
  ```bash
  curl --location 'localhost:8080/api/v1/user/get_aggregated_data_verified_storer/:storer_id' \
    --header 'Authorization: Bearer <access token>'
  ```
- Response
  ```JSON
    {
      "result": {
          "incidents": [
            {
                "_id": "UofmOcmzqcmTAcL",
                "_rev": "2-11d231e1ee9d93332cb7e21c11482848",
                "created_at": "2023-08-30T18:13:52.570965UTC",
                "description": "description",
                "user_id": "ZjDQMhshYF"
            },
            {
                "_id": "bcISHKmscmErAEP",
                "_rev": "2-3bde499a09dc08fcfdea1636d50ca373",
                "created_at": "2023-08-30T18:00:36.074582UTC",
                "description": "reason",
                "user_id": "ZjDQMhshYF"
            }
        ],
          "logs": {
              "returned_list": [...],
              "scanned_list":[...],
              "stored_list": [...]
          },
          "missions": [...],
          "storer_details": {
              "avartar": null,
              "incident_amount": 1,
              "profile": {
                  "email": "collector@example.com",
                  "user_name": "0xAD14Ea36"
              },
              "public_address": "0xAD143E30AD4852c97716ED5b32d45BcCfF7DEa36",
              "returned_count": 0,
              "stored_count": 0,
              "success_rate": null,
              "total_earned": 0
          },
          "total_earning_chat": [
            {
                "_id": "6e634bb1e7ecc88a3077100dee0153d9",
                "amount": 620000000000000000,
                "end_date": "2022-03-20T18:46:56.647612",
                "public_address": "0xAD143E30AD4852c97716ED5b32d45BcCfF7DEa36s",
                "start_date": "2021-01-01T00:00:00"
            },
            {
                "_id": "6e634bb1e7ecc88a3077100dee00efce",
                "amount": 500000000000000000,
                "end_date": "2022-03-20T18:46:56.647612",
                "public_address": "0xAD143E30AD4852c97716ED5b32d45BcCfF7DEa36s",
                "start_date": "2021-01-01T00:00:00"
            },
            {
                "_id": "6e634bb1e7ecc88a3077100dee00c915",
                "amount": 100000000000000000,
                "end_date": "2022-03-20T18:46:56.647612",
                "public_address": "0xAD143E30AD4852c97716ED5b32d45BcCfF7DEa36s",
                "start_date": "2021-01-01T00:00:00"
            }
        ]
      },
      "status": "success"
  }
  ```
### GET Aggregated data API - collector details - GET
- Description
    - https://github.com/DataUnion-app/Crab/issues/422
- method: GET
- Example
  ```bash
  url --location 'localhost:8080/api/v1/user/get_aggregated_data_collector/:collector_id' \
    --header 'Authorization: Bearer <access token>'
  ```
- Response
  ```JSON
      {
      "result": {
          "collector_details": {
              "avartar": null,
              "mission_amount": 1,
              "profile": {
                  "user_name": "data-union-user"
              },
              "public_address": "0xAD143E30AD4852c97716ED5b32d45BcCfF7DEa36s",
              "returned_count": 0,
              "stored_count": 0,
              "success_rate": null,
              "total_earned": 620000000000000000
          },
          "incidents": [
            {
                "_id": "UofmOcmzqcmTAcL",
                "_rev": "2-11d231e1ee9d93332cb7e21c11482848",
                "created_at": "2023-08-30T18:13:52.570965UTC",
                "description": "description",
                "user_id": "ZjDQMhshYF"
            },
            {
                "_id": "bcISHKmscmErAEP",
                "_rev": "2-3bde499a09dc08fcfdea1636d50ca373",
                "created_at": "2023-08-30T18:00:36.074582UTC",
                "description": "reason",
                "user_id": "ZjDQMhshYF"
            }
        ],
          "logs": {
              "scanned_list": [
                  {
                      "_id": "entity_list:CLLzGjpEOyUfPZq",
                      "_rev": "2-97df7b19eb26b5568f2b45431a1a67f6",
                      "company_name": "cname",
                      "created_at": "2023-09-12T13:52:46",
                      "description": "Test",
                      "entity_list_type": "private",
                      "entity_type": "image",
                      "favorites_of": [],
                      "image": null,
                      "log_name": "bname",
                      "name": "test",
                      "number_of_scans": 10,
                      "profile_image": {
                          "bounty_image": {
                              "content_type": "image/png",
                              "digest": "md5-32WiUJoevs5HuzQ4MAodNQ==",
                              "length": 35242,
                              "revpos": 3,
                              "stub": true
                          },
                          "company_image": {
                              "content_type": "image/png",
                              "digest": "md5-B/b2HIMvs/IyhgeR2JOPtA==",
                              "length": 35272,
                              "revpos": 2,
                              "stub": true
                          }
                      },
                      "public_address": "0xAD143E30AD4852c97716ED5b32d45BcCfF7DEa36s",
                      "qr_code": "dcJlPsBDOzoEcoO",
                      "type": "Scanned",
                      "updated_at": "2023-09-12T13:52:46"
                  }
              ]
          },
          "missions": [
              {
                  "_id": "mission:FYvIyAGEJZezYpT",
                  "bounty_id": "bounty:yKaYXsjjzzuKmzJ",
                  "company_name": "cname",
                  "mission_name": "bname",
                  "number_of_scans": 10,
                  "profile_image": {
                      "bounty_image": {
                          "content_type": "image/png",
                          "digest": "md5-s8gTnAhBlnqk4B5j94ergw==",
                          "length": 35374,
                          "revpos": 3,
                          "stub": true
                      },
                      "company_image": {
                          "content_type": "image/png",
                          "digest": "md5-w1R+nZ4hFrIfGOfrhpSAnQ==",
                          "length": 35303,
                          "revpos": 2,
                          "stub": true
                      }
                  },
                  "status": "completed",
                  "title": "bname"
              }
          ],
          "total_earning_chat": [
            {
                "_id": "6e634bb1e7ecc88a3077100dee0153d9",
                "amount": 620000000000000000,
                "end_date": "2022-03-20T18:46:56.647612",
                "public_address": "0xAD143E30AD4852c97716ED5b32d45BcCfF7DEa36s",
                "start_date": "2021-01-01T00:00:00"
            },
            {
                "_id": "6e634bb1e7ecc88a3077100dee00efce",
                "amount": 500000000000000000,
                "end_date": "2022-03-20T18:46:56.647612",
                "public_address": "0xAD143E30AD4852c97716ED5b32d45BcCfF7DEa36s",
                "start_date": "2021-01-01T00:00:00"
            },
            {
                "_id": "6e634bb1e7ecc88a3077100dee00c915",
                "amount": 100000000000000000,
                "end_date": "2022-03-20T18:46:56.647612",
                "public_address": "0xAD143E30AD4852c97716ED5b32d45BcCfF7DEa36s",
                "start_date": "2021-01-01T00:00:00"
            }
        ]
      },
      "status": "success"
  }
  ```
  
### GET Aggregated data API - Unverified creator details - GET
- Description
    - https://github.com/DataUnion-app/Crab/issues/423
- method: GET
- Example
  ```bash
  curl --location 'localhost:8080/api/v1/user/get_aggregated_data_unverified_creator/:creator_id' \
    --header 'Authorization: Bearer <access token>'
  ```
- Response
  ```JSON
      {
      "result": {
          "creator_detail": {
              "avartar": null,
              "profile": {
                  "address": "address",
                  "company_title": "data-union",
                  "country": "country",
                  "email": "test@domain.com",
                  "user_name": "data-union-user1"
              },
              "public_address": "0xAD143E30AD4852c97716ED5b32d45BcCfF7DEa36",
              "status": "new"
          }
      },
      "status": "success"
  }
  ```

### GET Aggregated data API - Unverified recycler details - GET
- Description
    - https://github.com/DataUnion-app/Crab/issues/540
- method: GET
- Example
  ```bash
  curl --location 'localhost:8080/api/v1/user/get_aggregated_data_unverified_recycler/GnEbtphSjT' \
    --header 'Authorization: Bearer <access token>'
  ```
- Response
  ```JSON
    {
      "result": {
          "recycler_detail": {
              "avartar": null,
              "profile": {
                  "accepted_materials": null,
                  "city": "test_city",
                  "country": "test_country",
                  "description": "description",
                  "geocode": {
                      "lat": null,
                      "lng": null
                  },
                  "name": "test_name",
                  "post_code": "test_post_code",
                  "street": "test_street"
              },
              "public_address": "0xA4427E30AD4852c97716ed5b32d45BCCff7dED58",
              "status": "new"
          }
      },
      "status": "success"
    }
  ```

### GET Aggregated data API - Unverified storer details - GET
- Description
    - https://github.com/DataUnion-app/Crab/issues/418
- method: GET
- Example
  ```bash
  curl --location 'localhost:8080/api/v1/user/get_aggregated_data_unverified_storer/:storer_id' \
    --header 'Authorization: Bearer <access token>'
  ```
- Response
  ```JSON
  {
      "result": {
          "storer_details": {
              "avartar": null,
              "profile": {
                  "email": "collector@example.com",
                  "user_name": "0xAD14Ea36"
              },
              "public_address": "0xAD143E30AD4852c97716ED5b32d45BcCfF7DEa36",
              "status": "new"
          }
      },
      "status": "success"
  }
  ```
  
### GET Collectors page in category - GET
- Description
  - https://github.com/DataUnion-app/Crab/issues/421
- method: GET
- Example
  ```bash
  curl --location 'localhost:8080/api/v1/user/get_collectors_page_in_category \
    --header 'Authorization: Bearer <access token>'
  ```
- Response

  ```JSON
  {
      "result": {
          "top_collectors": [
              {
                "collected_amount": 10,
                "profile": {
                    "user_name": "data-union-user"
                },
                "public_address": "0xAD143E30AD4852c97716ED5b32d45BcCfF7DEa36s",
                "rewards": 620000000000000000
            },
            {
                "collected_amount": 340,
                "profile": {
                    "email": "collector@example.com",
                    "user_name": "0xAD14Ea36"
                },
                "public_address": "0xAD143E30AD4852c97716ED5b32d45BcCfF7DEa36",
                "rewards": 500000000000000000
            }
          ],
          "verified_collectors": {
            "result": [
                {
                    "_id": "ZjDQMhshYF",
                    "claims": [
                        "user"
                    ],
                    "created_at": 1691695844.852333,
                    "profile": {
                        "user_name": "data-union-user"
                    },
                    "status": "verified"
                }
            ]
        },
        "verification_queue_collectors": {
            "result": [
                {
                    "_id": "AYsmBWDgWr",
                    "claims": [
                        "user"
                    ],
                    "created_at": 1694548363.815951,
                    "profile": {
                        "email": "collector@example.com",
                        "user_name": "0xAD14Ea36"
                    },
                    "status": "new"
                }
            ]
        },
      "status": "success"
  }
  ```

### GET storers page in category - GET
- Description
  - https://github.com/DataUnion-app/Crab/issues/420
- method: GET
- Example
  ```bash
  curl --location 'localhost:8080/api/v1/user/get_storers_page_in_category \
    --header 'Authorization: Bearer <access token>'
  ```
- Response

  ```JSON
  {
    "result": {
        "top_storers": [
            {
                "address": "address",
                "company_title": "data-union",
                "country": "country",
                "email": "test@domain.com",
                "public_address": "0x80Fe2fdEBf458803a1717d76378D43FF82dED147",
                "rewards": 0
            }
        ],
        "verified_storers": {
            "result": [
                {
                    "_id": "ZjDQMhshYF",
                    "claims": [
                        "storer"
                    ],
                    "created_at": 1691695844.852333,
                    "profile": {
                        "user_name": "storer"
                    },
                    "status": "verified"
                }
            ]
        },
        "verification_queue_storers": {
            "result": [
                {
                    "_id": "AYsmBWDgWr",
                    "claims": [
                        "storer"
                    ],
                    "created_at": 1694548363.815951,
                    "profile": {
                        "email": "storer@example.com",
                        "user_name": "0xAD14Ea36"
                    },
                    "status": "new"
                }
            ]
        }
    },
    "status": "success"
  }
  ```

### GET Creators page in category - GET
- Description
  - https://github.com/DataUnion-app/Crab/issues/419
- method: GET
- Example
  ```bash
  curl --location 'localhost:8080/api/v1/user/get_creators_page_in_category \
    --header 'Authorization: Bearer <access token>'
  ```
- Response

  ```JSON
  {
    "result": {
        "top_creators": [
            {
                "address": "address",
                "company_title": "data-union",
                "country": "country",
                "email": "test@domain.com",
                "public_address": "0x80Fe2fdEBf458803a1717d76378D43FF82dED147",
                "rewards": 0
            }
        ],
        "verified_creators": {
            "result": [
                {
                    "_id": "ZjDQMhshYF",
                    "claims": [
                        "creator"
                    ],
                    "created_at": 1691695844.852333,
                    "profile": {
                        "user_name": "creator"
                    },
                    "status": "verified"
                }
            ]
        },
        "verification_queue_creators": {
            "result": [
                {
                    "_id": "AYsmBWDgWr",
                    "claims": [
                        "creator"
                    ],
                    "created_at": 1694548363.815951,
                    "profile": {
                        "email": "creator@example.com",
                        "user_name": "0xAD14Ea36"
                    },
                    "status": "new"
                }
            ]
        }
    },
    "status": "success"
  }
  ```

### API creation - mission overview enterprise portal

- method: GET
- Authorization header (required): Bearer token
- Description: 
  - https://github.com/DataUnion-app/Crab/issues/427
  Use this api to get the mission related information for the user. Api will return maximum 100 results in
  single query. If an image is uploaded/annotated/verified for a mission with status `ready_to_start`, backend will move
  it to `in_progress`. If target of the mission is completed/exceeded, mission will be marked as `completed`.
- Parameters:
    - `page`: int - Default 1
    - `type`: string - Possible values `upload`/`annotate`/`verifiy`
    - `status`: string - Possible values `inprogress`/`completed`/`ready_to_start`
    - `sort_direction`: string (Optional) - Possible values: `desc`/`asc`
    - `sort_by`: string (Optional) - Possible values: `created_at`
    - `bounty_id`: string (Optional) specific bounty id
    - Example:
      ```bash
      curl --location --request GET 'http://localhost:8080/api/v1/missions/overview_info?type=upload&status=completed&page=1' \
      --header 'Authorization: Bearer <access_token>'
      ```
- Responses:
- 200
    ```JSON
    {
    "missions": [
        {
            "accepted_count": 0,
            "bounty_id": "bounty:yKaYXsjjzzuKmzJ",
            "criteria": {
                "target": 1
            },
            "description": "bd",
            "end_date": "2023-09-13T13:48:50.906013",
            "id": "mission:FYvIyAGEJZezYpT",
            "level": 1,
            "progress": 10,
            "returned_count": 0,
            "reward_status": "ready_to_pay",
            "status": "completed",
            "title": "bname",
            "type": "upload"
        }
    ],
    "total_count": 1
  }
      ```
### Verify QR Codes by storer API - SET

- Description
  - https://github.com/DataUnion-app/Crab/issues/458
- Example
  ```bash
  curl --location 'localhost:8080/api/v1/product/verify-qrcodes' \
    --header 'Content-Type: text/plain' \
    --header 'Authorization: Bearer <access token>' \
    --data '{
      "qrcodes":[["55cda624-4676-11ee-acbd-31dfe62827f4"], ["55cda623-4676-11ee-acbd-31dfe62827f4s"]],
      "status": "stored"
    }'
  ```
- Response
  ```JSON
  {
    "status": "success"
  }

### Add Ratings to Storers - SET 
- Description
    - https://github.com/DataUnion-app/Crab/issues/438
- method: POST
- Parameters
    - `storer_public_address`: Required string
    - `rate`: Required string
    - `description`: Required string
- Example
  ```bash
  curl --location 'localhost:8080/api/v1/user/set_storer_rating' \
    --header 'Content-Type: text/plain' \
    --header 'Authorization: Bearer <access token>' \
    --data-raw '{
        "storer_public_address" : "0xDF1dEc52e60202bE27B0644Ea0F584b6Eb5CE4eB",
        "rate" : "3",
        "description" : "description"
    }'
  ```
- Response
  ```JSON
  {
    "status": "success"
  }
  ```

### Add Ratings to Recyclers - SET 
- Description
    - https://github.com/DataUnion-app/Crab/issues/543
- method: POST
- Parameters
    - `recycler_public_address`: Required string
    - `rate`: Required string
    - `description`: Required string
- Example
  ```bash
  curl --location 'localhost:8080/api/v1/user/set_recycler_rating' \
    --header 'Content-Type: text/plain' \
    --header 'Authorization: Bearer <access token>' \
    --data-raw '{
        "recycler_public_address" : "0xDF1dEc52e60202bE27B0644Ea0F584b6Eb5CE4eB",
        "rate" : "3",
        "description" : "description"
    }'
  ```
- Response
  ```JSON
  {
    "status": "success"
  }
  ```

### GET User Ratings - GET
- Description
    - https://github.com/DataUnion-app/Crab/issues/438
- method: GET
- Example
  ```bash
  curl --location 'localhost:8080/api/v1/user/get_ratings/:user_id' \
    --header 'Authorization: Bearer <access token>'
  ```
- Response
  ```JSON
  {
      "average_rating": 3,
      "status": "success"
  }

### Handle the acceptance & rejection of image ids of bounty

- method: POST
- Examples

  ```bash
  curl --location 'localhost:8080/api/v1/bounty/image_handler' \
  --header 'Authorization: Bearer <access_token>'
  --header 'Content-Type: application/json' \
  --data-raw '{
    "bounty_id": "<bounty_id>",
    "image_ids": ["image_id1", "image_id2"]
  }'
  ```

- Response:

    - 200

  ```JSON
      {
      "accepted_image_ids": [
          "05ca0beba714b9a86bcc992b3fc1b811",
          "20ca60d52b8310bf1dd617e58d30d23c"
      ],
      "created_at": "2023-09-12T13:48:13",
      "description": null,
      "entity_ids": [
          "8edd97b5a1014aaee17499b5c5cacc9e",
          "6c9f0b24454aa177639a53ee2a4d6875",
          "e02af34364f4460eb597963a269b00cf",
          "ae5f181a8d517735cf099fbb1b2852fb",
          "bea8ca6b661b1bbf58124f8804c4e60d",
          "34951f0d6e35b4225ee2381425894475",
          "2b98807ce0d49256a7c2e0c4e12d7bca",
          "28cdbb377bd47139f439052a03f82f5d",
          "4ce2d2a551ffbbb2cab103f3e190c9d0",
          "ae8c4f3cef3d5717aa8b4d0bddceea24"
      ],
      "entity_list_type": "bounty",
      "entity_type": "image",
      "favorites_of": [],
      "id": "entity_list:tklyHIeonbvztGd",
      "image": null,
      "name": "test-dataset",
      "public_address": "0xDF1dEc52e60202bE27B0644Ea0F584b6Eb5CE4eB",
      "rejected_image_ids": [
          "0561507254d14cc976b0e8dced803397",
          "0e759291e9ce6e23b2ccfccab94cb4ea"
      ],
      "updated_at": "2023-09-12T19:48:16.095170"
  }
  ```
    - 400

  ```JSON
    {
      "messages": [
          "Error message"
      ]
    }
  ```
  
### Get All QR Codes and images API - POST

- Description
  - https://github.com/DataUnion-app/Crab/issues/454
- method: POST
- Parameters
  - `bounty_id`: Optional string
- Example
  ```bash
  curl --location --request POST 'localhost:8080/api/v1/product/get-qrcodes-images' \
    --header 'Content-Type: text/plain' \
    --header 'Authorization: Bearer <access token>' \
    --data '{
      "bounty_id" : "bounty:OXOpOeJVOHMEoSQ"
      }'
  ```
- Response
  ```JSON
  {
    "result": [
        {
            "_id": "RfWZYeQVsfNOvGR",
            "filepath": "...data/qrcode_images/Screenshot_2023-09-03_at_10.14.56.png",
            "qr_code": [
                "55cda624-4676-11ee-acbd-31dfe62827f4"
            ],
            "status": "created"
        },
        {
            "_id": "ZibFxkxzVYNDhHk",
            "qr_code": [
                "55cda623-4676-11ee-acbd-31dfe62827f4"
            ],
            "status": "collected"
        },
    ],
      "status": "success"
  }
  ```
#### Set QRCodes from storer to Creator - SET

- Description
  - https://github.com/DataUnion-app/Crab/issues/461
- method: POST
- Example:

  ```bash
  curl --location 'localhost:8080/api/v1/product/set-qrcodes-storer-to-creator' \
  --header 'Authorization: Bearer <access_token>'
  --data '{
    "bounty_id" : <bounty_id>
  }'
  ```

- Responses:

    - 400

  ```JSON
    {
      "messages": [
          "All status are not 'stored' [PFfbTTyuwnBznhk]."
      ],
      "status": "failed"
    }
  ```

    - 200

  ```JSON
  {
      "status": "success"
  }
  ```

### Check QRCode uploaded already exist for a bounty API - POST

- Description
  - https://github.com/DataUnion-app/Crab/issues/452
- method: POST
- Examples

  ```bash
  curl --location --request POST 'localhost:8080/api/v1/product/check-exist-qrcode-in-bounty' \
  --header 'Authorization: Bearer <access_token>'
  --header 'Content-Type: application/json' \
  --data '{
    "qrcode" : ["55cda623-4676-11ee-acbd-31dfe62827f4s"],
    "bounty_id" : "bounty:OXOpOeJVOHMEoSQ"
  }'
  ```

- Response:

    - 400

  ```JSON
      {
        "messages": [
            "QRCode already exist"
        ],
        "status": "failed"
      }
  ```
    - 400

  ```JSON
    {
      "messages": [
          "No QRCode on the bounty items"
      ],
      "status": "failed"
    }
  ```
    - 200

  ```JSON
    {
      "id": "PFfbTTyuwnBznhk",
      "status": "success"
    }
  ```

### Get aggregation items qrcode by bounty - POST

- Description: https://github.com/DataUnion-app/Crab/issues/457

- Example
  ```bash
  curl --location --request POST 'localhost:8080/api/v1/product/get-aggregation-qrcode-by-bounty' \
    --header 'Authorization: Bearer <access token>'
    --data '{
      "bounty_id" : "bounty:OXOpOeJVOHMEoSQ",
      "status" : "scanned"
    }'
  ```

- Response

```JSON
  {
      "items": [
          {
              "image_ids": [
                  "6c9f0b24454aa177639a53ee2a4d6875"
              ],
              "qr_code": [
                  "55cda623-4676-11ee-acbd-31dfe62827f4s"
              ],
              "status": "scanned"
          },
          {
              "image_ids": [
                  "092c599614fcf11bed3947849ac87a8e"
              ],
              "qr_code": [
                  "55cda624-4676-11ee-acbd-31dfe62827f4"
              ],
              "status": "scanned"
          }
      ],
      "status": "success"
  }
```

### Get aggregation items qrcode by User - POST

- Description: https://github.com/DataUnion-app/Crab/issues/457

- Example
  ```bash
  curl --location --request POST 'localhost:8080/api/v1/product/get-aggregation-qrcode-by-user' \
    --header 'Authorization: Bearer <access token>'
    --data '{
      "public_address" : "0xAD143E30AD4852c97716ED5b32d45BcCfF7DEa36",
      "status" : "scanned"
    }'
  ```

- Response

```JSON
  {
    "items": [
        {
            "image_ids": [
                "6c9f0b24454aa177639a53ee2a4d6875"
            ],
            "public_address": "0xAD143E30AD4852c97716ED5b32d45BcCfF7DEa36",
            "qr_code": [
                "55cda623-4676-11ee-acbd-31dfe62827f4s"
            ],
            "status": "scanned"
        },
        {
            "image_ids": [
                "092c599614fcf11bed3947849ac87a8e"
            ],
            "public_address": "0xAD143E30AD4852c97716ED5b32d45BcCfF7DEa36",
            "qr_code": [
                "55cda624-4676-11ee-acbd-31dfe62827f4"
            ],
            "status": "scanned"
        }
    ],
    "status": "success"
  }
```
#### Report Creation - SET

- Description
  - https://github.com/DataUnion-app/Crab/issues/473
- Parameters
  - `mission_id`: Optional string
  - `product_id`: Optional string
  - `start_date`: Optional string
  - `end_date`: Optional string
  - `filetype`: Optional string, ex: `pdf`, `csv`
- method: POST
- Example:

  ```bash
  curl --location 'localhost:8080/api/v1/product/report-creation' \
  --header 'Authorization: Bearer <access_token>'
  --data '{
    "mission_id" : "mission:NsAprmODGhoLGjh",
    "product_id" : "product_id",
    "start_date" : "2023-10-16",
    "end_date" : "2023-10-28",
    "filetype" : "pdf",

  }'
  ```

- Responses:

    - 200

  ```JSON
  {
    "result": "iGEOrHxuhqJeFUp",
    "status": "success"
  }
  ```

### Report API - Get my reports(Creator) - POST

- Description
  - https://github.com/DataUnion-app/Crab/issues/483
- method: POST
- Parameters
  - `filetype`: Optional string, ex: `pdf`, `csv`
- Example
  ```bash
  curl --location 'localhost:8080/api/v1/product/get-reports' \
  --header 'Authorization: Bearer <access_token>' \
  --data '{
    "filetype" : "pdf"
    "mission_id" : "mission:NsAprmODGhoLGjh",
    "start_date" : "2023-10-15",
    "end_date" : "2023-11-29",
    "sort_by" : "asc"
  }'
  ```
- Response

  ```JSON
    {
      "result": [
          {
              "_id": "iGEOrHxuhqJeFUp",
              "_rev": "1-312b415b0e6667efe7b58a0a9930cd56",
              "created_at": "2023-10-25T19:57:44.453593UTC",
              "mission_id" : "mission:NsAprmODGhoLGjh",
              "filename": "bounty:OXOpOeJVOHMEoSQ_product_id_2023-10-16_Report.pdf",
              "filepath": "/home/source/Crab/data/pdf/0xDF1dec52e60202be27b0644eA0F584B6eb5CE4EB/bounty:OXOpOeJVOHMEoSQ_product_id_2023-10-16_Report.pdf",
              "filesize": 104.7470703125,
              "public_address": "0xDF1dec52e60202be27b0644eA0F584B6eb5CE4EB",
              "filetype": "pdf",
              "source": "recyclium"
          },
          {
              "_id": "mpsuWMTUtvYCbtI",
              "_rev": "1-81eedbcca17c63b5a8f895f6d7262731",
              "created_at": "2023-10-25T19:53:26.593313UTC",
              "mission_id" : "mission:NsAprmODGhoLGjh",
              "filename": "_product_id_2023-10-16_Report.pdf",
              "filepath": "/home/source/Crab/data/pdf/0xDF1dec52e60202be27b0644eA0F584B6eb5CE4EB/_product_id_2023-10-16_Report.pdf",
              "filesize": 104.69921875,
              "public_address": "0xDF1dec52e60202be27b0644eA0F584B6eb5CE4EB",
              "filetype": "pdf",
              "source": "recyclium"
          }
      ],
      "status": "success"
        }
  ```

### Report API - Download Report PDF - GET

- Description
  - https://github.com/DataUnion-app/Crab/issues/473
- method: GET
- Example
  ```bash
  curl --location --request GET 'localhost:8080/api/v1/product/download/<report_id>' \
  --header 'Authorization: Bearer <access_token>' \
  ```
- Response

  ```
    PDF File
  ```

### Collector profile stats - GET

- Description
  - https://github.com/DataUnion-app/Crab/issues/495
- method: GET
- Example
  ```bash
  curl --location 'localhost:8080/api/v1/user/collector/stat/<user_id>' \
  --header 'Authorization: Bearer  <access_token>'
  ```
- Response
  
  ```JSON
  {
    "collector": {
        "amount_of_companies": 1,
        "amount_of_rewards": 620000000000000000,
        "amount_of_scanned_items": 1,
        "amount_of_storers": 2,
        "number_of_missions": 1
     },
    "status": "success"
  }
  ```

### Report API - Get QRCodes by Bounty_ID -GET

- Description
  https://github.com/DataUnion-app/Crab/issues/491
- method: GET
- Parameters
  - `bounty_id`: Required string
- Example
  ```bash
  curl --location 'localhost:8080/api/v1/qrcode/get-qrcodes?bounty_id=bounty%3AOXOpOeJVOHMEoSQ' \
  --header 'Authorization: Bearer <access_token>' \
  ```
 - Response

  ```JSON

      {
    "result": {
        "returned_count": 2,
        "returned_qrcodes": [
            {
                "public_address": "0xDF1dec52e60202be27b0644eA0F584B6eb5CE4EB",
                "qr_code": [
                    "55cda623-4676-11ee-acbd-31dfe62827f4s"
                ],
                "status": "returned",
                "updated_at": "2023-10-19T16:48:33.295409UTC"
            },
            {
                "public_address": "0xDF1dec52e60202be27b0644eA0F584B6eb5CE4EB",
                "qr_code": [
                    "55cda629-4676-11ee-acbd-31dfe62827f4"
                ],
                "status": "returned",
                "updated_at": "2023-10-16T17:33:49.907438UTC"
            }
        ],
        "scanned_count": 0,
        "scanned_qrcodes": [],
        "stored_count": 1,
        "stored_qrcodes": [
            {
                "public_address": "0xDF1dec52e60202be27b0644eA0F584B6eb5CE4EB",
                "qr_code": [
                    "55cda624-4676-11ee-acbd-31dfe62827f4"
                ],
                "status": "stored",
                "updated_at": "2023-11-09T21:01:45.081828UTC"
            }
        ]
    },
    "status": "success"
  }
  ```

### Collector profile stats - GET

- Description
  - https://github.com/DataUnion-app/Crab/issues/495
- method: GET
- Example
  ```bash
  curl --location 'localhost:8080/api/v1/user/storer/stat/<user_id>' \
  --header 'Authorization: Bearer  <access_token>'
  ```
- Response
  
  ```JSON
  {
    "status": "success",
    "storer": {
        "amount_of_collectors": 1,
        "amount_of_companies": 1,
        "amount_of_rewards": 620000000000000000,
        "amount_of_stored_items": 10,
        "number_of_missions": 1,
        "storer_rating": null
    }
  }
  ```
  
### Retrieve all items of batches for a product API - POST

- Description
  - https://github.com/DataUnion-app/Crab/issues/501
- method: POST
- Parameters
  - `product_id`:  string
  - `page`:  number
  - `page_size`:  number
- Example
  ```bash
  curl --location --request POST 'localhost:8080/api/v1/product/get-all-items-batch-list' \
  --header 'Authorization: Bearer <access_token>' \
  --data '{
      "product_id" : "vTNlYGweNPsMXHt",
      "page" : 1,
      "page_size" : 100
  }'
  - Response

  ```JSON
  "result": [
        {
            "_id": "IfTEGSvxZOGhdEo",
            "_rev": "1-673ac522b460003bccbc80475b81eea2",
            "batch_name": "Batch1",
            "bounty_id": null,
            "created_at": "2023-11-21T10:57:04.515829UTC",
            "filepath": "/home/messi/work/galziv/source/Crab/data/generated_qr_code/test@domain.com_vTNlYGweNPsMXHt_Batch1_3_qr_code_2.png",
            "product_id": "vTNlYGweNPsMXHt",
            "public_address": "test@domain.com",
            "qr_code": "Product: vTNlYGweNPsMXHt\nBatch: Batch1\nItem: 2",
            "source": "recyclium",
            "status": "created"
        },
        {
            "_id": "UdjcfLbWuHKIrXb",
            "_rev": "1-d9bd33e2a8b535001c051df8fd902eb7",
            "batch_name": "Batch1",
            "bounty_id": null,
            "created_at": "2023-11-21T10:57:04.541816UTC",
            "filepath": "/home/messi/work/galziv/source/Crab/data/generated_qr_code/test@domain.com_vTNlYGweNPsMXHt_Batch1_3_qr_code_3.png",
            "product_id": "vTNlYGweNPsMXHt",
            "public_address": "test@domain.com",
            "qr_code": "Product: vTNlYGweNPsMXHt\nBatch: Batch1\nItem: 3",
            "source": "recyclium",
            "status": "created"
        },
        {
            "_id": "doArMZZHKNkKYkb",
            "_rev": "1-95a954f595c935afd6de039b7e68ec6d",
            "batch_name": "Batch1",
            "bounty_id": null,
            "created_at": "2023-11-21T10:57:04.485231UTC",
            "filepath": "/home/messi/work/galziv/source/Crab/data/generated_qr_code/test@domain.com_vTNlYGweNPsMXHt_Batch1_3_qr_code_1.png",
            "product_id": "vTNlYGweNPsMXHt",
            "public_address": "test@domain.com",
            "qr_code": "Product: vTNlYGweNPsMXHt\nBatch: Batch1\nItem: 1",
            "source": "recyclium",
            "status": "created"
        }
    ],
    "status": "success"
  }
  ```

### Retrieve not used batches for a product API - POST

- Description
  - https://github.com/DataUnion-app/Crab/issues/509
- method: POST
- Parameters
  - `product_id`:  string
  - `page`:  number
  - `page_size`:  number
- Example
  ```bash
  curl --location --request POST 'localhost:8080/api/v1/product/get-not-used-batch-list' \
  --header 'Authorization: Bearer <access_token>' \
  --data '{
      "product_id" : "vTNlYGweNPsMXHt",
      "page" : 1,
      "page_size" : 100
  }'
  - Response

  ```JSON
  {
    "result": [
        {
            "_id": "batch:lrTBZaYeDOhNJrS",
            "_rev": "1-0ff91629ef58779c270e5ba7e5ab1ee8",
            "amount_of_items": "3",
            "batch_name": "Batch1",
            "bounty_id": null,
            "created_at": "2023-11-22T07:12:24",
            "product_id": "vTNlYGweNPsMXHt",
            "public_address": "test@domain.com",
            "updated_at": "2023-11-22T07:12:24"
        }
    ],
    "status": "success"
  }
  ```
### Retrieve all batches for a product API - POST

- Description
  - https://github.com/DataUnion-app/Crab/issues/509
- method: POST
- Parameters
  - `product_id`:  string
  - `page`:  number
  - `page_size`:  number
- Example
  ```bash
  curl --location --request POST 'localhost:8080/api/v1/product/get-all-batch-list' \
  --header 'Authorization: Bearer <access_token>' \
  --data '{
      "product_id" : "vTNlYGweNPsMXHt",
      "page" : 1,
      "page_size" : 100
  }'
  - Response

  ```JSON
  {
    "result": [
        {
            "_id": "batch:kVAoixWRUuXVtci",
            "_rev": "5-41c9e3eb13c963a4fef749242404f7d5",
            "amount_of_items": "3",
            "batch_name": "Batch1",
            "bounty_id": "bounty:RJpHtvvRplfZnSs",
            "created_at": "2023-11-22T06:49:47",
            "product_id": "vTNlYGweNPsMXHt",
            "public_address": "test@domain.com",
            "updated_at": "2023-11-22T06:49:47"
        },
        {
            "_id": "batch:lrTBZaYeDOhNJrS",
            "_rev": "1-0ff91629ef58779c270e5ba7e5ab1ee8",
            "amount_of_items": "3",
            "batch_name": "Batch1",
            "bounty_id": null,
            "created_at": "2023-11-22T07:12:24",
            "product_id": "vTNlYGweNPsMXHt",
            "public_address": "test@domain.com",
            "updated_at": "2023-11-22T07:12:24"
        }
    ],
    "status": "success"
  }
  ```

### Fetch all storers for creator -GET

- Description
  - https://github.com/DataUnion-app/Crab/issues/490
- method: GET
- Example
  ```bash
  curl --location 'localhost:8080/api/v1/get-all-storers/<user_id>' \
  --header 'Authorization: Bearer <access_token>'
  ```
- Response

  ```JSON
    {
    "status": "success",
    "storers": [
        {
            "stored_items": 0,
            "storer_address": null,
            "storer_name": "0xAD14Ea36",
            "storer_size": null,
            "storing_items": 18
        },
        {
            "stored_items": 1,
            "storer_address": "address",
            "storer_name": null,
            "storer_size": null,
            "storing_items": 24
        },
        {
            "stored_items": 0,
            "storer_address": null,
            "storer_name": "data-union-user",
            "storer_size": null,
            "storing_items": 1
        }
    ]
  }
  ```

### Status bar for collector -GET

- Description
  - https://github.com/DataUnion-app/Crab/issues/497
- method: GET
- Example
  ```bash
  curl --location 'localhost:8080/api/v1/user/collector/stat-bar/<user_id>' \
  --header 'Authorization: Bearer <access_id>'
  ```
- Response

  ```JSON
    {
    "information": {
        "number_of_incidents": 1,
        "number_of_missions": 1,
        "reward": 620000000000000000,
        "success_rate": 100
    },
    "status": "success"
  }
  ```

### Status bar for storer -GET

- Description
  - https://github.com/DataUnion-app/Crab/issues/497
- method: GET
- Example
  ```bash
  curl --location 'localhost:8080/api/v1/user/storer/stat-bar/<user_id>' \
  --header 'Authorization: Bearer <access_id>'
  ```
- Response

  ```JSON
    {
      "information": {
          "amount_of_returned_items": 0,
          "amount_of_stored_items": 0,
          "number_of_incidents": 1,
          "number_of_missions": 0,
          "reward": 620000000000000000
      },
      "status": "success"
    }
  ```

### Status bar for creator -GET

- Description
  - https://github.com/DataUnion-app/Crab/issues/497
- method: GET
- Example
  ```bash
  curl --location 'localhost:8080/api/v1/user/creator/stat-bar/<user_id>' \
  --header 'Authorization: Bearer <access_id>'
  ```
  - Response

  ```JSON
    {
      "information": {
          "number_of_incidents": 0,
          "amount_of_scanned_items": 0,
          "amount_of_stored_items": 1,
          "amount_of_returned_items": 0,
          "number_of_missions": 1,
          "reward": 620000000000000000
      },
      "status": "success"
    }
  ```
### Return all new storers API -GET

- Description
  - https://github.com/DataUnion-app/Crab/issues/513
- method: GET
- Example
  ```bash
  curl --location 'localhost:8080/api/v1/user/get-all-new-storers?page_size=10&page=1' \
  --header 'Authorization: Bearer <access_id>'
  ```
  - Response

  ```JSON
    {
    "status": "success",
    "storers": [
        {
            "_id": "wNAQKuyGKY",
            "_rev": "41-5d43fd5bf58b7972daa3b3a0e29e2688",
            "claims": [
                "storer",
            ],
            "created_at": 1692971495.119224,
            "current_mission_number": 0,
            "guidelines_acceptance_flag": "UNKNOWN",
            "guild_id": null,
            "is_access_blocked": false,
            "missions": [],
            "nonce": 6167290299849,
            "profile": {
                "address": "address",
                "company_title": "data-union",
                "country": "country",
                "email": "test@domain.com"
            },
            "public_address": "0xDF1dEc52e60202bE27B0644Ea0F584b6Eb5CE4eB",
            "ratings": [
                {
                    "description": "description",
                    "rate": 4,
                    "rated_by": "test@domain.com"
                },
                {
                    "description": "description",
                    "rate": 3,
                    "rated_by": "test@domain.com"
                }
            ],
            "referral_id": "yraMe",
            "referred_users": [],
            "rewards": 0,
            "status": "new",
            "usage_flag": "UNKNOWN"
        }
    ]
  }
  ```

### Return all new creators API -GET

- Description
  - https://github.com/DataUnion-app/Crab/issues/513
- method: GET
- Example
  ```bash
  curl --location 'localhost:8080/api/v1/user/get-all-new-creators?page_size=10&page=1' \
  --header 'Authorization: Bearer <access_id>'
  ```
  - Response

  ```JSON
    {
    "creators": [
        {
            "DID": "did:example:123456789abcdefghijk",
            "_id": "IwVuVPsPSV",
            "_rev": "51-6e3e6a88996cca2cc64b7f4b5ed096cf",
            "claims": [
                "creator",
            ],
            "created_at": 1692971546.63046,
            "current_mission_number": 0,
            "guidelines_acceptance_flag": "UNKNOWN",
            "guild_id": null,
            "is_access_blocked": false,
            "missions": [],
            "nonce": 4078553330111,
            "profile": {
                "address": "address",
                "company_title": "data-union",
                "country": "country",
                "email": "test@domain.com",
                "user_name": "data-union-user1"
            },
            "public_address": "test@domain.com",
            "ratings": [
                {
                    "description": "description",
                    "rate": 4,
                    "rated_by": "test@domain.com"
                },
                {
                    "description": "description",
                    "rate": 3,
                    "rated_by": "test@domain.com"
                }
            ],
            "referral_id": "JDgny",
            "referred_users": [],
            "rewards": 0,
            "status": "new",
            "team_id": "GKSQZBDFneQOAYL",
            "team_role": "viewer",
            "usage_flag": "UNKNOWN"
        },
        {
            "_id": "wNAQKuyGKY",
            "_rev": "41-5d43fd5bf58b7972daa3b3a0e29e2688",
            "claims": [
                "creator"
            ],
            "created_at": 1692971495.119224,
            "current_mission_number": 0,
            "guidelines_acceptance_flag": "UNKNOWN",
            "guild_id": null,
            "is_access_blocked": false,
            "missions": [],
            "nonce": 6167290299849,
            "profile": {
                "address": "address",
                "company_title": "data-union",
                "country": "country",
                "email": "test@domain.com"
            },
            "public_address": "0xDF1dEc52e60202bE27B0644Ea0F584b6Eb5CE4eB",
            "ratings": [
                {
                    "description": "description",
                    "rate": 4,
                    "rated_by": "test@domain.com"
                },
                {
                    "description": "description",
                    "rate": 3,
                    "rated_by": "test@domain.com"
                }
            ],
            "referral_id": "yraMe",
            "referred_users": [],
            "rewards": 0,
            "status": "new",
            "usage_flag": "UNKNOWN"
        }
    ],
    "status": "success"
  }
  ```


  ### Get all new recyclers API - GET

- Description
  - https://github.com/DataUnion-app/Crab/issues/518
- method: GET
- Example
  ```bash
  curl --location 'localhost:8080/api/v1/user/get-all-new-recyclers?page_size=10&page=1' \
  --header 'Authorization: Bearer <access_id>'
 - Response
  ```JSON
    {
  "recyclers": [
        {
            "_id": "cGeVSClLEy",
            "_rev": "2-d1ce38103c8842d91b729251b6e2322d",
            "claims": [
                "recycler"
            ],
            "created_at": 1701022406.182493,
            "current_mission_number": 0,
            "guidelines_acceptance_flag": "UNKNOWN",
            "guild_id": null,
            "is_access_blocked": false,
            "missions": [],
            "nonce": 1698081639174,
            "profile": {
                "accepted_materials": null,
                "city": "test_city",
                "country": "test_country",
                "description": "description",
                "geocode": {
                    "lat": null,
                    "lng": null
                },
                "name": "test_name",
                "post_code": "test_post_code",
                "street": "test_street",
                "verification_document": "/home/messi/work/galziv/source/Crab(Kawai)/data/0xB3227e30Ad4852C97716ed5B32D45bccfF7dE859/verificaton_document/export-Training_Session_67.csv"
            },
            "public_address": "0xB3227e30Ad4852C97716ed5B32D45bccfF7dE859",
            "referral_id": "LyZGJ",
            "referred_users": [],
            "rewards": 0,
            "status": "new",
            "usage_flag": "UNKNOWN"
        },
        {
            "_id": "eowyanMXMe",
            "_rev": "2-96d02aebf50ac771cede6340cef7cb73",
            "claims": [
                "recycler"
            ],
            "created_at": 1701070767.943278,
            "current_mission_number": 0,
            "guidelines_acceptance_flag": "UNKNOWN",
            "guild_id": null,
            "is_access_blocked": false,
            "missions": [],
            "nonce": 7546147800586,
            "profile": {
                "accepted_materials": null,
                "city": "test_city",
                "country": "test_country",
                "description": "description",
                "geocode": {
                    "lat": null,
                    "lng": null
                },
                "name": "test_name",
                "post_code": "test_post_code",
                "profileImage": "/home/messi/work/galziv/source/Crab(Kawai)/data/0xD5227E30ad4852c97716ED5B32D45BccFf7dE85a/profile_images/test-qrcode.png",
                "street": "test_street"
            },
            "public_address": "0xD5227E30ad4852c97716ED5B32D45BccFf7dE85a",
            "referral_id": "pJaer",
            "referred_users": [],
            "rewards": 0,
            "status": "new",
            "usage_flag": "UNKNOWN"
        },
    ],
    "status": "success"
  }
   ```
=======
### signup as a recycler API - POST

- Description
  - https://github.com/DataUnion-app/Crab/issues/516
- method: POST
- Example
  ```bash
  curl --location 'localhost:8080/register-recycler' \
  --form 'name="test_name"' \
  --form 'street="test_street"' \
  --form 'post_code="test_post_code"' \
  --form 'city="test_city"' \
  --form 'country="test_country"' \
  --form 'description="description"' \
  --form 'accpeted_materials="[]"' \
  --form 'verificaton_document=@"<doc_file>"' \
  --form 'avatar=@"<avatar_file>"' \
  --form 'public_address="0xB3227E30AD4852c97716ED5b32d45BcCfF7DE859"'
  ```
  - Response

  ```JSON
    {
      "nonce": 1698081639174,
      "status": "success"
    }
  ```

### create new material API - POST

- Description
  - https://github.com/DataUnion-app/Crab/issues/521
- method: POST
- Example
  ```bash
  curl --location 'localhost:8080/api/v1/material/create' \
  --header 'Authorization: Bearer <access_token>'
  --data '{
    "material_name" : "wood"
  }'
  ```
  - Response

  ```JSON
    {
        "material_id": "material:KHBcuHMGoLNgJop",
        "message": "created successfully",
        "status": "success"
    }
  ```

### get all materials API - GET

- Description
  - https://github.com/DataUnion-app/Crab/issues/521
- method: GET
- Example
  ```bash
  curl --location --request GET 'localhost:8080/api/v1/material/get-all' \
  --header 'Authorization: Bearer <access_token>'
  --data '{
    "material_name" : "wood"
  }'
  ```
  - Response

  ```JSON
    {
      "materials": [
          {
              "_id": "material:KHBcuHMGoLNgJop",
              "_rev": "1-01fb0552e7464dc5c984fdbf1053ca5d",
              "created_at": "2023-11-27T07:46:27",
              "created_by": "0xD5227e30Ad4852c97716ed5b32d45BccFf7dE85B",
              "material_name": "wood",
              "updated_at": "2023-11-27T07:46:27"
          },
          {
              "_id": "material:UPQLABoyCJScJRv",
              "_rev": "1-21ad385408bd2d36f9f6e078f9d5cf21",
              "created_at": "2023-11-27T07:45:55",
              "created_by": "0xD5227e30Ad4852c97716ed5b32d45BccFf7dE85B",
              "material_name": "metal",
              "updated_at": "2023-11-27T07:45:55"
          }
      ],
      "status": "success"
    }
  ```
  
### Set recycler profile API - PUT

- Description
  - https://github.com/DataUnion-app/Crab/issues/517
- method: PUT
- Example
  ```bash
  curl --location --request PUT 'localhost:8080/api/v1/user/recycler/profile' \
  --header 'Content;' \
  --header 'Authorization: Bearer <access_token>' \
  --form 'name="name_test"' \
  --form 'street="street_test"' \
  --form 'post_code="post_code_test"' \
  --form 'city="city_test"' \
  --form 'country="country_test"' \
  --form 'description="description_test"' \
  --form 'accepted_materials="accepted_materials_test"' \
  --form 'verification_document=@"<doc_file>' \
  --form 'avatar=@"<avatar_file>"' \
  --form 'lat="85.1654898"' \
  --form 'lng="201.258899"'
    ```
  - Response

  ```JSON
    {
    "status": "success"
    }
    
### Get recycler profile API - GET

- Description
  - https://github.com/DataUnion-app/Crab/issues/517
- method: GET
- Example
  ```bash
  curl --location --request GET 'localhost:8080/api/v1/user/recycler' \
  --header 'Content;' \
  --header 'Authorization: Bearer <access_token>' \
   ```
  - Response

  ```JSON
    {
      "profile": {
          "accepted_materials": null,
          "city": "test_city",
          "country": "test_country",
          "description": "description",
          "geocode": {
              "lat": null,
              "lng": null
          },
          "name": "test_name",
          "post_code": "test_post_code",
          "profileImage": "/home/messi/work/galziv/source/Crab(Kawai)/data/0xD5227E30ad4452c97712Ed5B32D45BCCfF7De85B/profile_images/test-qrcode.png",
          "street": "test_street",
          "verification_document": "/home/messi/work/galziv/source/Crab(Kawai)/data/0xD5227E30ad4452c97712Ed5B32D45BCCfF7De85B/verification_document/Stickers.Recyclium.1.pdf"
      },
      "status": "success"
    }
  ```

### Generated QR Code API - POST

- Description
  - https://github.com/DataUnion-app/Crab/issues/494
- method: POST
- Example
  ```bash
  curl --location 'localhost:8080/api/v1/product/generate-qrcode' \
  --header 'Authorization: Bearer <access_token>' \
  --form 'batch_name="Batch1"' \
  --form 'batch_size="3"' \
  --form 'product_id="vTNlYGweNPsMXHt"'
   ```
  - Response

  ```JSON
    {
      "status": "success"
    }
  ```

### GET Recyclers page in category API - GET
- Description
    - https://github.com/DataUnion-app/Crab/issues/539
- method: GET
- Example
  ```bash
  curl --location 'localhost:8080/api/v1/user/get_recyclers_page_in_category' \
    --header 'Authorization: Bearer <access token>'
  ```
- Response
  ```JSON
      {
        "status": "success",
        "top_recyclers": [
            {
                "accepted_materials": null,
                "city": "test_city",
                "country": "test_country",
                "description": "description",
                "geocode": {
                    "lat": null,
                    "lng": null
                },
                "name": "test_name",
                "post_code": "test_post_code",
                "profileImage": "/home/messi/work/galziv/source/Crab(Kawai)/data/0xD5227e30Ad4852c97716ed5b32d45BccFf7dE85B/profile_images/test-qrcode.png",
                "public_address": "0xD5227e30Ad4852c97716ed5b32d45BccFf7dE85B",
                "rewards": 0,
                "street": "test_street"
            },
        ],
        "verification_queue_recyclers": {
            "result": [
                {
                    "_id": "MwEGJHMHMs",
                    "created_at": 1701071379.598096,
                    "profile": {
                        "accepted_materials": null,
                        "city": "test_city",
                        "country": "test_country",
                        "description": "description",
                        "geocode": {
                            "lat": null,
                            "lng": null
                        },
                        "name": "test_name",
                        "post_code": "test_post_code",
                        "profileImage": "/home/messi/work/galziv/source/Crab(Kawai)/data/0xD5227E30ad4452c97712Ed5B32D45BCCfF7De85B/profile_images/test-qrcode.png",
                        "street": "test_street",
                        "verification_document": "/home/messi/work/galziv/source/Crab(Kawai)/data/0xD5227E30ad4452c97712Ed5B32D45BCCfF7De85B/verification_document/Stickers.Recyclium.1.pdf"
                    },
                    "public_address": "0xD5227E30ad4452c97712Ed5B32D45BCCfF7De85B",
                    "status": "new"
                },
            ]
        },
        "verified_recyclers": {
            "result": []
        }
    }
  ```

### Recycler API - /api/v1/recyclers - POST

- Description
  - End-point to fetch all recyclers by admin. This is private route.
  - https://github.com/DataUnion-app/Crab/issues/538
- Example
  ```bash
  curl --location --request POST 'localhost:8080/api/v1/recyclers' \
    --header 'Content-Type: text/plain' \
    --header 'Authorization: Bearer <access token>' \
    --data-raw '{
      "page_no": 2,
      "per_page": 10,
      "sort": "desc"
    }'
  ```
- Response
  - 200
  ```JSON
  {
    "status": "success",
    "recyclers": [
      ...
    ]
  }
  ```
    
### Verify QR Codes by recycler with transport status API - POST

- Description
  - https://github.com/DataUnion-app/Crab/issues/542
- Example
  ```bash
  curl --location 'localhost:8080/api/v1/product/verify-qrcodes-recycler-transport' \
    --header 'Content-Type: application/json' \
    --header 'Authorization: Bearer <access token>' \
    --data '{
      "qrcodes":[["55cda624-4676-11ee-acbd-31dfe62827f4"], ["55cda623-4676-11ee-acbd-31dfe62827f4s"]],
    }'
  ```
- Response
  ```JSON
  {
    "status": "success"
  }
  ```

### Verify QR Codes by recycler with qualitycheck status API - POST

- Description
  - https://github.com/DataUnion-app/Crab/issues/542
- Example
  ```bash
  curl --location 'localhost:8080/api/v1/product/verify-qrcodes-recycler-qualitycheck' \
    --header 'Content-Type: application/json' \
    --header 'Authorization: Bearer <access token>' \
    --data '{
      "qrcodes":[["55cda624-4676-11ee-acbd-31dfe62827f4"], ["55cda623-4676-11ee-acbd-31dfe62827f4s"]],
    }'
  ```
- Response
  ```JSON
  {
    "status": "success"
  }
  ```

### Verify QR Codes by recycler with recycled status API - POST

- Description
  - https://github.com/DataUnion-app/Crab/issues/542
- Example
  ```bash
  curl --location 'localhost:8080/api/v1/product/verify-qrcodes-recycler-recycled' \
    --header 'Content-Type: application/json' \
    --header 'Authorization: Bearer <access token>' \
    --data '{
      "qrcodes":[["55cda624-4676-11ee-acbd-31dfe62827f4"], ["55cda623-4676-11ee-acbd-31dfe62827f4s"]],
    }'
  ```
- Response
  ```JSON
  {
    "status": "success"
  }
  ```
### GET Aggregated data API - recycler details - GET
- Description
    - https://github.com/DataUnion-app/Crab/issues/541
- method: GET
- Example
  ```bash
  url --location 'localhost:8080/api/v1/user/get_aggregated_data_recycler/:recycler_id' \
    --header 'Authorization: Bearer <access token>'
  ```
- Response
  ```JSON
  {
    "result": {
        "incidents": [],
        "logs": {
            "returned_list": []
        },
        "missions": null,
        "recycler_details": {
            "avartar": null,
            "profile": {
                "user_name": "data-union-user"
            },
            "public_address": "0xBC143E30AD4852c977156D5b32d45BcCfF7DEa37",
            "returned_count": 0,
            "stored_count": 0,
            "success_rate": null,
            "total_earned": 0
        },
        "total_earning_chat": []
    },
    "status": "success"
  }
  ```

### Status bar for recycler -GET

- Description
  - https://github.com/DataUnion-app/Crab/issues/544
- method: GET
- Example
  ```bash
  curl --location 'localhost:8080/api/v1/user/recycler/stat-bar/<user_id>' \
  --header 'Authorization: Bearer <access_id>'
  ```
- Response

  ```JSON
    {
      "information": {
          "amount_of_returned_items": 0,
          "number_of_incidents": 1,
          "number_of_missions": 0,
          "reward": 620000000000000000
      },
      "status": "success"
    }
  ```

### Fetch all storers for recycler -GET

- Description
  - https://github.com/DataUnion-app/Crab/issues/545
- method: GET
- Example
  ```bash
  curl --location 'localhost:8080/api/v1/get-all-storers-for-recycler/<user_id>' \
  --header 'Authorization: Bearer <access_token>'
  ```
- Response

  ```JSON
    {
    "status": "success",
    "storers": [
        {
            "stored_items": 0,
            "storer_address": null,
            "storer_name": "0xAD14Ea36",
            "storer_size": null,
            "storing_items": 18
        },
        {
            "stored_items": 1,
            "storer_address": "address",
            "storer_name": null,
            "storer_size": null,
            "storing_items": 24
        },
        {
            "stored_items": 0,
            "storer_address": null,
            "storer_name": "data-union-user",
            "storer_size": null,
            "storing_items": 1
        }
    ]
  }
  ```