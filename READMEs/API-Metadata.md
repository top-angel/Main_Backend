# Metadata rest apis

### Annotation

#### /api/v1/query-metadata

- method: POST
- Authorization header (required): Bearer token
- Description: Use this api to query the `image_ids`, `tags` and `descriptions`. Max 100 results in 1 api query. Use
  page number to get more data. Optional field in body: "type". possible values : "BoundingBox"/"TextTag"/"
  Anonymization"
- Body parameters:
    - status: string
    - page: number
    - type: string (optional) default: TextTag
    - entity-type: string (optional) default: image. Possible value: "video"/"image"
    - tags: list of strings (optional) (empty list of strings will return nothing)
    - fields: list of strings
- Example
  ```
  curl --location --request POST 'http://localhost:8080/api/v1/query-metadata' \
  --header 'Authorization: Bearer <access_token>' \
  --header 'Content-Type: application/json' \
  --data-raw '{
      "status" : "VERIFIABLE",
      "page": 1,
      "fields" : ["image_id","descriptions","tags"],
      "type" : "TextTag",
      "tags" : ["birdhouse"],
      "bounty": "general"
  }'
  ```
- Response
  ```JSON
  {
    "page": 1,
    "page_size": 100,
    "result": [
        {
            "descriptions": [],
            "image_id": "00000cf8fc7c3cd8",
            "tag_data": []
        },
        {
            "descriptions": [
                "sample description 1"
            ],
            "image_id": "9cd8d0c6e8294d4c",
            "tag_data": [
                "notecase",
                "Brittany spaniel",
                "pelican",
                "amphibian",
                "streetcar",
                "Aepyceros melampus"
            ]
        },
        {
            "descriptions": [
                "sample description 2"
            ],
            "image_id": "3b7e2865198c0b45bfd2a879b700553e",
            "tag_data": [
                "notecase",
                "Brittany spaniel",
                "pelican",
                "amphibian",
                "streetcar",
                "Aepyceros melampus"
            ]
        }
    ]
  }
  ```

#### /api/v1/metadata/annotation

- method: POST
- Description: This api can be used to add `annotations` to the images/supported entity types.
- Authorization header (required): Bearer token
- Description:
  Supported annotation types: `dots`, `box`, `anonymization`
- Example
  ```bash
  curl --location --request POST 'http://localhost:8080/api/v1/metadata/annotation' \
  --header 'Authorization: Bearer <access_token>' \
  --header 'Content-Type: application/json' \
  --data-raw '{
      "image_id": <access_token>,
      "annotations":[
          {
            "x": 1.0,
            "y":1.0,
            "width": 34.0,
            "height": 23.2,
            "type": "box",
            "tag": "sample"
          },
          {
            "skin_color": "Brown",
            "gender": "Male",
            "type": "anonymization",
            "age": 25
          },
          {
            "type": "dots",
            "tag": "random-tag",
            "dots": [{"x": 1, "y": 1, "height": 1, "width": 1}]
        }
      ]
  }'
  ```
- Response:
  ```JSON
  {
      "status": "success"
  }
  ```

#### /api/v1/metadata/query

- method: POST
- Description: Use this api to query the `annotations` associated with each image/video or other supported data types.
  Max 100 image_ids in 1 api query.
- Authorization header (required): Bearer token

- Example
  ```bash
  curl --location --request POST 'http://localhost:8080/api/v1/metadata/query' \
  --header 'Authorization: Bearer <access_token>' \
  --header 'Content-Type: application/json' \
  --data-raw '{
  "image_ids":["00000cf8fc7c3cd8"],
  "annotations" :["BoundingBox", "GeoLocation"]
  }'
  ```
- Response:
  ```JSON
  {
      "result": {
          "BoundingBox": [
              {
                  "image_id": "00000cf8fc7c3cd8",
                  "value": {
                      "height": 34,
                      "tag": "sample",
                      "width": 23.2,
                      "x": 1,
                      "y": 1
                  }
              }
          ],
          "GeoLocation": [
              {
                  "image_id": "00000cf8fc7c3cd8",
                  "value": {
                      "latitude": 48.74553,
                      "longitude": 9.10044
                  }
              }
          ]
      },
      "status": "success"
  }
  ```

#### /api/v1/metadata/tag-image-count

- method: GET
- Authorization header (required): Bearer token
- Example:

  ```bash
  curl --location --request GET 'localhost:8080/api/v1/metadata/tag-image-count?tag_name=tag_name1&tag_name=tag_name2' \
  --header 'Authorization: Bearer <access_token>'
  ```

- Responses:

    - 200

      ```JSON
      {
          "result": [
              {
                  "tag": "tag_name1",
                  "count": 2
              },
              {
                  "tag": "tag_name2",
                  "count": 1
              }
          ] ,
          "status": "success"
      }
      ```

    - 400

      ```JSON
      {
          "messages": "Failure issue message",
          "status": "failed"
      }
      ```

#### /api/v1/search-images

- method: POST
- Authorization header (required): Bearer token

- body:

    - page: (required) Number
    - tags: (required) Tags to search an image

- Example:
  ```bash
  curl --location --request POST 'http://localhost:8080/api/v1/search-images' \
  --header 'Authorization: Bearer <access_token>' \
  --header 'Content-Type: application/json' \
  --data-raw '{
    "page": 1,
    "tags" : ["tiny", "tree"],
    "page_size": 50
  }'
  ```
- Responses:
    - 200
      ```JSON
      {
          "page": 1,
          "result": [
              "d7d867a6c0206171"
          ],
          "total_count": 1
      }
      ```

### Metadata

#### /api/v1/upload-file

- method: POST
- Authorization header (required): Bearer token
- Example:
  ```bash
  curl --location --request POST 'localhost:8080/api/v1/upload-file' \
  --header 'Authorization: Bearer <access_token>' \
  --form 'mission_id=mission:abcd1234'
  --form 'latitude=123' \
  --form 'longitude=123123' \
  --form 'qr_code="1234567890"' \
  --form 'bounty="general"' \
  --form 'bounty="bname1"' \
  --form 'annotations=[
      {
        "x": 1.0,
        "y":1.0,
        "width": 34.0,
        "height": 23.2,
        "type": "box",
        "tag": "sample"
      },
      {
        "skin_color": "Brown",
        "gender": "Male",
        "type": "anonymization",
        "age": 25
      },
      {
        "type": "dots",
        "tag": "random-tag",
        "dots": [{"x": 1, "y": 1, "height": 1, "width": 1}]
      }
    ]' \
  --form 'file=@"/path/to/file"' \
  ```
- Note (valid format of some parameters):
  ```bash
  - file: file( any image, audio, and video files are allowed. if it is image file, it needs to be bigger than 600x400 )
  ```
- Response:
    - 200
  ```JSON
  {
    "id": "bounty:GAFmjZJBnXAESoE",
    "message": "File successfully uploaded"
  }
  ```
    - 400
  ```JSON
  {
    "status": "failed",
    "messages": ["Error message"]
  }
  ```

#### /api/v1/upload/user-data

- Description: Upload user's amazon/facebook data as zip file to the server. The server will ignore any media files. The
  data will be saved in the database in the json format.
- method: POST
- Authorization header (required): Bearer token
- Form Parameters
    - `type`: Possible values: `facebook`/`linkedin`/`linkedin_part_1`/`linkedin_part_2`/`google`/`spotify`/`netflix`/`amazon`/`zalando`/
      `web3`/`user_metadata`/`survey`/`twitter`
    - `upload-async`: Optional string to indicate whether the unzip and saving content to document should be performed asynchronously.
       Possible value: `true`/`false`. Default: `false`. If any other value is provided, fallbacks to `false`.
- Example:
    - Facebook
      ```bash
         curl --location --request POST 'http://localhost:8080/api/v1/upload/user-data' \
         --header 'Authorization: Bearer <access_token>' \
         --form 'file=@"<file_path>/facebook.zip"' \
         --form 'type="facebook"'
      ```
    - Amazon
       ```bash
         curl --location --request POST 'http://localhost:8080/api/v1/upload/user-data' \
         --header 'Authorization: Bearer <access_token>' \
         --form 'file=@"<file_path>/amazon.zip"' \
         --form 'type="amazon"'
      ```

- Response:
    - 200
      ```JSON
      {
         "id": "DgwTAjzUWsVurOd"
      }
      ```
    - 200: When `upload-async` is `true`
      ```JSON
      {
          "status": "processing"
      }
      ```

#### /api/v1/metadata/query-view

- Method: GET
- Authorization header (required): Bearer token
- Parameters:
    - `design-doc`: string
    - `view-name`: string
    - `query-type` : string `user_id`/`keys`/`key_range`
- Examples:
    - User contributions for wedatanation
        - Curl Command
           ```bash
           curl --location --request GET 'http://localhost:8080/api/v1/metadata/query-view?design-doc=wedatanation&view=user-contributions&query-type=user_id' \
           --header 'Authorization: Bearer <access_token>'
           ```
        - response:
            - 200
          ```JSON
          {
            "result": [
                {
                    "created_date": "2022-07-05T12:59:28.756Z",
                    "id": "JGGnBuOOEPSVzUz",
                    "last_updated_date": "2022-07-05T12:59:28.756Z",
                    "monetization_status": "enabled",
                    "type": "amazon"
                },
                {
                    "created_date": "2022-07-07T08:39:11.197Z",
                    "id": "lkOEdDXIIVLeNdX",
                    "last_updated_date": "2022-07-07T08:39:11.197Z",
                    "monetization_status": "enabled",
                    "type": "facebook"
                },
                {
                    "created_date": "2022-07-07T08:25:00.400Z",
                    "id": "plPqrOTMZUTTCDf",
                    "last_updated_date": "2022-07-07T08:25:00.400Z",
                    "monetization_status": "disabled",
                    "type": "facebook"
                }
            ]
          } 
          ```

#### /api/v1/metadata/monetization-status

- Method: POST
- Authorization header (required): Bearer token
- Example
    ```bash
    curl --location --request POST 'http://localhost:8080/api/v1/metadata/monetization-status' \
    --header 'Authorization: Bearer <access_token>' \
    --header 'Content-Type: application/json' \
    --data-raw '{
        "entity_id": "lkOEdDXIIVLeNdX",
        "entity_type": "json",
        "monetization_status": "disabled"
    }'
    ```
- Response
    - 200:
      ```JSON
      {}
      ```

#### /api/v1/metadata/web3-wallet/nonce

- Method: GET
- Authorization header (required): Bearer token
- Example
    ```bash
      curl --location --request GET 'http://localhost:8080/api/v1/metadata/web3-wallet/nonce?wallet_address=123' \
      --header 'Authorization: Bearer <access_token>' \
      --data-raw ''
    ```
- Response
    - 200:
      ```JSON
      {
        "nonce": "2445829164411"
      }
      ```

#### /api/v1/metadata/web3-wallet

- Method: POST
- Authorization header (required): Bearer token
- Parameter:
    - Body:
        - `wallet_address`: required
        - `signature`: required
        - `network` : option `eth_mainnet`/`polygon_mainnet`. Default : `None`
- Example
  ```bash
  curl --location --request POST 'http://localhost:8080/api/v1/metadata/web3-wallet' \
    --header 'Authorization: Bearer <access_token>' \
    --header 'Content-Type: application/json' \
    --data-raw '{"wallet_address":"123", "signature":"sdfsdfsdf"}'
  ```
- Response
    - 200
      ```JSON
      
      ```
    - 400
      ```JSON
      {
         "messages": [
            "Invalid signature"
         ]
      }
      ```