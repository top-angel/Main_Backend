## Entity lists

#### api/v1/entity-lists/create

- method: POST
- Authorization header (required): Bearer token
- Parameters:
    - image: optional
- Example:

  ```bash
  curl --location --request POST 'localhost:8080/api/v1/entity-lists/create' \
  --header 'Authorization: Bearer <access_token>' \
  --header 'Content-Type: application/json' \
  --data-raw '{
    "entity_type": "image",
    "visibility": "public",
    "entity_ids" : ["753c5fc6696deb38"],
    "description" : "Test desc",
    "name": "test name",
    "image": "<base 64 encoded image as string>"
  }'
  ```

- Responses:

    - 400

      ```JSON
      {
        "messages": [
            "Invalid 'entity_ids'"
        ]
      }
      ```

    - 200
      ```JSON
      {
        "id": "VBrICYYQUy"
      }
      ```

#### api/v1/entity-lists/create-from-annotations

- method: POST
- Description: This api allows users to create/update an entity. The api finds the list of available entity_ids for the
  given annotation type and adds them to a list. Currently, only `TextTag` annotation is supported.
  If `entity_list_id` is specified and not empty, then the data is added to the existing list.
  The two examples are given below.

- Authorization header (required): Bearer token
- Example 1:

  ```bash
  curl --location --request POST 'http://localhost:8080/api/v1/entity-lists/create-from-annotations' \
  --header 'Authorization: Bearer <access_token>' \
  --header 'Content-Type: application/json' \
  --data-raw '{
    "entity_type": "image",
    "visibility": "private",
    "tags" : ["abc", "xyz"],
    "annotation_type" : "TextTag",
    "description" : "Test desc",
    "name": "test name",
    "image": "<base 64 encoded image as string>"
  }'
  ```

- Example 2:

  ```bash
  curl --location --request POST 'http://localhost:8080/api/v1/entity-lists/create-from-annotations' \
  --header 'Authorization: Bearer <access_token>' \
  --header 'Content-Type: application/json' \
  --data-raw '{
    "entity_type": "image",
    "tags" : ["abc", "xyz"],
    "annotation_type" : "TextTag",
    "entity_list_id": "entity_list:ScfLCPHGCDJUYbb"
  }'
  ```

- Responses:

    - 400

      ```JSON
      {
         "messages": [
          "Name too long. Limit is 200 characters."
         ]
      }
      ```

    - 200
      ```JSON
      {
        "id": "entity_list:lRhELUyFgfhMqJd"
      }
      ```

#### api/v1/entity-lists/

- method: GET
- Example:

  ```bash
  curl --location --request GET 'localhost:8080/api/v1/entity-lists/?id=entity_list:xRaVCzRaOiEZkPe'
  ```

- Responses:
    - 200
  ```JSON
  {
    "description": "Test desc",
    "entity_ids": [
        "23c3830303030707"
    ],
    "id": "entity_list:xRaVCzRaOiEZkPe",
    "name": "test name"
  }
  ```

#### api/v1/entity-lists/

- method: DELETE
- Authorization header (required): Bearer token
- Example:

  ```bash
  curl --location --request DELETE 'localhost:8080/api/v1/entity-lists/?id=ncmGPrAWUn' \
  --header 'Authorization: Bearer <access_token>'
  ```

- Responses:

    - 400

  ```JSON
  {
    "messages": [
       "Invalid 'entity_ids'"
    ]
  }
  ```

    - 200

  ```JSON
  {
      "id": "ncmGPrAWUn"
  }
  ```

#### api/v1/entity-lists/own

- method: GET
- Authorization header (required): Bearer token
- Example:

  ```bash
  curl --location --request GET 'localhost:8080/api/v1/entity-lists/own?page=1&entity_type=image' \
  --header 'Authorization: Bearer <access_token>'
  ```

- Responses:
    - 200
      ```JSON
      {
      "total_count": 2,
      "result": [
         {
             "entity_ids": ["753c5fc6696deb38"],
             "entity_list_type": "public",
             "id": "VBrICYYQUy",
             "description" : "test desc",
             "name" : "test name"
         },
         {
             "entity_ids": ["753c5fc6696deb38"],
             "entity_list_type": "private",
             "id": "LfRKFOCeDc",
             "description" : "test desc",
             "name" : "test name"
         }
      ]
      }
      ```

#### api/v1/entity-lists/update

- method: POST
- Authorization header (required): Bearer token
- Example:

  ```bash
  curl --location --request POST 'localhost:8080/api/v1/entity-lists/update' \
  --header 'Authorization: Bearer <access_token>' \
  --header 'Content-Type: application/json' \
  --data-raw '{
      "id": "VBrICYYQUy",
      "visibility": "public",
      "entity_ids" : [ "753c5fc6696deb38", "d8e4a6eec44923f4"],
      "description" : "Test 2",
      "name": "test name2",
      "image": "<base 64 encoded image as string>"
  }'
  ```

- Responses:

    - 200
        - Empty string

#### api/v1/entity-lists/search

- method: GET
- Example:

  ```bash
  curl --location --request GET 'localhost:8080/api/v1/entity-lists/search?entity_type=image&page=1'
  ```

- Responses:
    - 200
  ```JSON
  {
  "result": [
      {
          "description": "Test 2",
          "entity_ids": [
              "753c5fc6696deb38",
              "d8e4a6eec44923f4"
          ],
          "id": "VBrICYYQUy",
          "name" : "test"
      }
  ]
  }
  ```

#### api/v1/entity-lists/favorites

- method: GET
- Authorization header (required): Bearer token
- Example:

  ```bash
  curl --location --request GET 'localhost:8080/api/v1/entity-lists/favorites' \
  --header 'Authorization: Bearer <access_token>'
  ```

- Responses:
    - 200
  ```JSON
  {
      "result": {
          "private_favorites_list": ["entity_list_1", "entity_list_2"],
          "public_favorites_list": ["entity_list_3", "entity_list_4"]
      },
      "status": "success"
  }
  ```
    - 400
  ```JSON
  {
      "messages": ["Error message"],
      "status": "failed"
  }
  ```

#### api/v1/entity-lists/manage-favorites

- method: POST
- Authorization header (required): Bearer token
- Example:

  ```bash
  curl --location --request POST 'localhost:8080/api/v1/entity-lists/manage-favorites' \
  --header 'Authorization: Bearer <access_token>' \
  --header 'Content-Type: application/json' \
  --data-raw '{
      "entity_lists_to_mark": ["entity_list_1", "entity_list_2"],
      "entity_lists_to_unmark": ["entity_list_3", "entity_list_4"],
  }'
  ```

- Responses:
    - 200
  ```JSON
  {
      "status": "success"
  }
  ```
    - 400
  ```JSON
  {
      "messages": ["Error message"],
      "status": "failed"
  }
  ```

#### api/v1/entity-lists/merge

- method: POST
- Description:
    - Calling user should be owner of destination list.
    - Calling user should be also the owner of the source list in case source is a private list.
    - Merge of bounty lists is not permitted.
- Authorization header (required): Bearer token
- Example:

  ```bash
  curl --location --request POST 'http://localhost:8080/api/v1/entity-lists/merge' \
  --header 'Authorization: Bearer <access_token>' \
  --header 'Content-Type: application/json' \
  --data-raw '{
      "destination": "entity_list:TMjtBmjcHsImzqs",
      "sources" : ["entity_list:DpuFqeABuRpNMQv"]
  }'
  ```

- Responses:
    - 200
     ```JSON
     {
       "result": null,
       "status": "success"
     }
     ```
    - 400
    ```JSON
    {
    "messages": [
      "[0xcFc3E1AE2752449eBB0B9b9DDdFa9138c73dD35f] is not owner of destination list."
    ], 
    "status": "failed"
    }
    ```
    - 400
    ```JSON
    {
    "messages": [
      "[0xcFc3E1AE2752449eBB0B9b9DDdFa9138c73dD35f] is not owner of source list [<some-id>]."
    ], 
    "status": "failed"
    }
    ```
