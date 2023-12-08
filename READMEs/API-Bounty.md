# Crab backend REST api

## Bounty apis

### api/v1/bounty/create

- method: POST
- Authorization header (required): Bearer token
- Example:
  ```bash
  curl --location --request POST 'localhost:8080/api/v1/bounty/create' \
  --header 'Authorization: Bearer <access_token>' \
  --form 'company_name="test"' \
  --form 'company_description="test"' \
  --form 'bounty_description="bd"' \
  --form 'start_date="2023-11-30T00:00:00.000Z"' \
  --form 'end_date="2023-12-25T00:55:31.820Z"' \
  --form 'bounty_name="test"' \
  --form 'bounty_image=@"<image_url>"' \
  --form 'company_image=@"<image_url>"' \
  --form 'tags="test"' \
  --form 'sample_data_list="gfdgdf,rtgyrth"' \
  --form 'image_requirements="test"' \
  --form 'image_count="1"' \
  --form 'image_format="jpeg"' \
  --form 'number_of_verifications="1000000"' \
  --form 'entity_list_name="entity_list:MggkpsmCIVXpIMk"' \
  --form 'bounty_type="upload"' \
  --form 'entity_list_ids="[]"' \
  --form 'status="in_progress"' \
  --form 'product_id="FRBxaUSLxYcycCe"' \
  --form 'special_instructions="test_special_instructions"' \
  --form 'minimum_amount_stored="10"' \
  --form 'minimum_amount_returned="5"' \
  --form 'amount_of_items="10"' \
  --form 'amount_of_reward="25"' \
  --form 'location="{\"latitude\": 123.25684, \"longitude\": 98.25698, \"radius\":20, \"worldwide\": false}"' \
  --form 'qr_code=@"<image_url>"' \
  --form 'batch_ids="[\"batch:kVAoixWRUuXVtci\"]"'
  ```
- Note (valid format of some parameters):
  ```bash
  - company_name : string( max 200chars )
  - company_description: string( max 2000chars )
  - bounty_type: string ( upload/annotate/verify )
  - bounty_name: string( max 200chars )
  - bounty_description: string( max 2000chars )
  - start_date: datetime( at least today datetime )
  - end_date: datetime( at least today datetime && greater than start_date )
  - company_image: file( bigger than 400x400 )
  - bounty_image: file( bigger than 400x400 )
  ```
- Response:
    - 200
  ```JSON
  {
    "id": "bounty:GAFmjZJBnXAESoE"
  }
  ```

### api/v1/bounty/list

- Description:
  In api response, following parameters can be `null`:
    - `rejected_entity_count`
    - `accepted_entity_count`
    - `number_of_annotations`
    - `number_of_verifications`
- Example
  ```bash
  curl --location --request GET 'localhost:8080/api/v1/bounty/list' \
  --header 'Authorization: Bearer <access_token>'
  ```
- Response:
    - 200
  ```JSON
  [
    {
        "bounty_description": "bd",
        "bounty_image_url": "todo",
        "bounty_name": "bname",
        "company_description": "cd",
        "company_image_url": "todo",
        "company_name": "cname",
        "end_date": "2022-11-14T00:55:31.820Z",
        "id": "bounty:GAFmjZJBnXAESoE",
        "start_date": "2022-01-24T00:55:31.820Z",
        "sample_data_list": [ "gfdgdf", "rtgyrth"],
        "tags": [ "sdfargij", "agtrjuh", "syheary"],
        "image_count": 1234,
        "image_format": [
            "png",
            "jpeg"
        ],
        "image_requirements": "dffgre,grtu",
        "number_of_verifications": 324,
        "bounty_type": "verify",
        "total_entity_count": 0,
        "rejected_entity_count": 0,
        "accepted_entity_count": 0,
        "number_of_annotations": 123
    }
  ]
  ```

### api/v1/bounty/

- Description: Get bounty by id
  In api response, following parameters can be `null`:
    - `rejected_entity_count`
    - `accepted_entity_count`
    - `number_of_annotations`
    - `number_of_verifications`
- Example
  ```bash
  curl --location --request GET 'http://localhost:8080/api/v1/bounty/?id=bounty:DjGtobpEOpprcZy' \
  --header 'Authorization: Bearer <access_token>'
  ```
- Response:
    - 200
  ```JSON
    {
    "result": {
        "accepted_entity_count": 0,
        "bounty_description": "bd",
        "bounty_image_url": "todo",
        "bounty_name": "bname",
        "bounty_type": "upload",
        "company_description": "cd",
        "company_image_url": "todo",
        "company_name": "cname",
        "end_date": "2023-11-14T00:55:31.820000+00:00",
        "entity_ids": 0,
        "entity_list_id": "entity_list:XeuVUqVjPDIhNLH",
        "id": "bounty:DjGtobpEOpprcZy",
        "image_count": 10000,
        "image_format": [
            "png",
            "jpeg"
        ],
        "image_requirements": "213",
        "number_of_annotations": 234,
        "number_of_verifications": 123,
        "rejected_entity_count": 0,
        "sample_data_list": [
            "gfdgdf",
            "rtgyrth"
        ],
        "start_date": "2022-12-07T00:00:31.820000+00:00",
        "status": "created",
        "tags": [
            "sdfargij",
            "agtrjuh",
            "syheary"
        ]
    }
  }
  ```

### Get bounty and company image

- method: GET
- Examples

  ```bash
  curl --location --request GET 'localhost:8080/api/v1/bounty/image?bounty_id=bounty:OjnVxVqnQKeFiEO&image_type=company_image' \
  --header 'Authorization: Bearer <access_token>'
  ```

  ```bash
  curl --location --request GET 'localhost:8080/api/v1/bounty/image?bounty_id=bounty:OjnVxVqnQKeFiEO&image_type=bounty_image' \
  --header 'Authorization: Bearer <access_token>'
  ```

- Response:
    - 200 Image

### Get entity ids by bounty id

- method: GET
- Examples

  ```bash
  curl --location --request GET 'localhost:8080/api/v1/bounty/images_ids?bounty_id=bounty:OjnVxVqnQKeFiEO' \
  --header 'Authorization: Bearer <access_token>'
  ```

- Response:
    - 200
  ```
    [
      "image_id1",
      "image_id2",
    ]
  ```

### Handle the acceptance & rejection of image ids of bounty

- method: POST
- Examples

  ```bash
  curl --location --request GET 'localhost:8080/api/v1/bounty/image_handler' \
  --header 'Authorization: Bearer <access_token>'
  --header 'Content-Type: application/json' \
  --data-raw '{
    "bounty_id": "bounty:UpfOLZbdxAjTVYd",
    "accepted_image_ids": ["image_id1", "image_id2"],
    "rejected_image_ids" : ["image_id3", "image_id4"]
  }'
  ```

- Response:

    - 200

  ```
    {
      "_id": "entity_list:FmDePwFgbnzthyd",
      "_rev": "6-b807a19ccc315aec03e1ff1222689f76",
      "accepted_image_ids": [
          1,
          2,
          3,
          4
      ],
      "created_at": "2022-03-23T19:42:17",
      "description": null,
      "entity_ids": [],
      "entity_list_type": "bounty",
      "entity_type": "image",
      "name": "test list name",
      "public_address": "0x38173F9e3A3ceE4bD4077f1da6A9e5a6F912AbAf",
      "rejected_image_ids": [
          2,
          3,
          4
      ],
      "updated_at": "2022-03-23T19:42:17"
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

#### /api/v1/bounty/query-view

- Description: This is a general purpose api to get the information from the views exposed by the database.
- method: GET
- Authorization header (required): Bearer token
- Parameters:
  - `design-doc`: String
  - `view`: string
  - `query-type`: string
  - `type`: string
  - `doc_id`: string
- Examples
    - Get bounty information by id
        - Request:
          ```bash
          curl --location --request \
          GET 'http://localhost:8080/api/v1/bounty/query-view?design-doc=bounty-info&view=bounty-id&query-type=public_entity_id&type=bounty&doc_id=bounty:KbVjwhzFPUBTOBD' \
          --header 'Authorization: Bearer <access_token>'
          ```
        - Response:
          ```JSON
           {
            "result": [
            {
                "bounty_description": "bd",
                "bounty_image_url": "todo",
                "bounty_name": "bname",
                "bounty_type": "upload",
                "company_description": "cd",
                "company_image_url": "todo",
                "company_name": "cname",
                "end_date": "2023-11-14T00:55:31.820000+00:00",
                "entity_list_id": "entity_list:YZneLeFJRBtSLgB",
                "id": "bounty:KbVjwhzFPUBTOBD",
                "image_count": 10000,
                "image_format": [
                    "png",
                    "jpeg"
                ],
                "image_requirements": "213",
                "number_of_annotations": 234,
                "number_of_verifications": 123,
                "sample_data_list": [
                    "gfdgdf",
                    "rtgyrth"
                ],
                "start_date": "2022-12-07T00:00:31.820000+00:00",
                "status": "created",
                "tags": [
                    "sdfargij",
                    "agtrjuh",
                    "syheary"
                ]
            }
           ]
          }
          ```

#### List all bounties

- Example

```bash
curl --location --request GET 'http://localhost:8080/api/v1/bounty/query-view?design-doc=bounty-info&view=all&query-type=all' \
--header 'Authorization: Bearer <access_token>'
```

- Response
  - 200
  ```JSON
  {
    "result": [
        ...,
        {
            "bounty_description": "bd",
            "bounty_name": "test",
            "bounty_type": "annotate",
            "company_description": "test",
            "company_name": "test",
            "created_at": "2023-03-02T22:30:24",
            "created_by": "0x8438979b692196FdB22C4C40ce1896b78425555A",
            "document_type": "bounty",
            "end_date": "2023-11-14T00:55:31.820000+00:00",
            "id": "bounty:FXADDlELECCnibs",
            "start_date": "2023-03-02T00:00:00+00:00"
        },
       ...
    ]
  }
  ```
#### Bounty creation

- Example

```bash
curl --location 'localhost:8080/api/v1/bounty/create' \
--header 'Authorization: Bearer <access_token>' \
--form 'company_name="test"' \
--form 'company_description="test"' \
--form 'bounty_description="bd"' \
--form 'start_date="2023-11-21T00:00:00.000Z"' \
--form 'end_date="2023-11-25T00:55:31.820Z"' \
--form 'bounty_name="test"' \
--form 'bounty_image=@"<image_url>"' \
--form 'company_image=@"<image_url>"' \
--form 'tags="test"' \
--form 'sample_data_list="gfdgdf,rtgyrth"' \
--form 'image_requirements="test"' \
--form 'image_count="1"' \
--form 'image_format="jpeg"' \
--form 'number_of_verifications="1000000"' \
--form 'entity_list_name="entity_list:MggkpsmCIVXpIMk"' \
--form 'bounty_type="upload"' \
--form 'entity_list_ids="[]"' \
--form 'status="in_progress"' \
--form 'product_id="FRBxaUSLxYcycCe"' \
--form 'special_instructions="test_special_instructions"' \
--form 'minimum_amount_stored="10"' \
--form 'minimum_amount_returned="5"' \
--form 'amount_of_items="10"' \
--form 'amount_of_reward="25"' \
--form 'location="{\"latitude\": 123.25684, \"longitude\": 98.25698, \"radius\":20, \"worldwide\": false}"' \
--form 'qr_code=@"<image_url>"'
```

- Response
  - 200
  ```JSON
  {
    "id": "bounty:UEwuBaVOujOQnWN"
  }
  ```