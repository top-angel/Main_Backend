# Wedatanation apis\

#### Upload user metadata file as json

- Curl command
    ```bash
    curl --location --request POST 'https://crab.wedatanation.dataunion.app/api/v1/upload/user-data' \
    --header 'Authorization: Bearer <access_token>' \
    --form 'file=@"<file-path>/user_metadata.json"' \
    --form 'type="user_metadata"'
    ```
- Response
    - 200
  ```JSON
  {
    "id": "NclMNiKnlFDxXuy"
  }
  ```

#### View uploaded user metadata

- Curl command
    ```bash
    curl --location --request GET 'https://crab.wedatanation.dataunion.app/api/v1/metadata/query-view?design-doc=wedatanation&view=user-metadata&query-type=user_id' \
    --header 'Authorization: Bearer <access_token>'
    ```
- Response
    - 200
  ```bash
  {
    "result": [
        {
            "app": "wedatanation",
            "temp": 123
        },
        {
            "app": "wedatanation",
            "temp": 123
        }
    ]
  }
  ```

#### Get generated avatars

- Curl command
  ```bash
  curl --location --request GET 'http://localhost:8080/api/v1/user/query-view?design-doc=user-info&view=generated-avatar&query-type=user_id' \
  --header 'Authorization: Bearer <access_token>'
  ```

- Response
  - 200
    ```JSON
    {
        "result": [
            {
                "avatar_text": [],
                "avatar_text_status": "creating",
                "image_status": "generated",
                "image_urls": [
                    "https://pollinations-ci-bucket.s3.amazonaws.com/avatars1/1b3ca4e4.png",
                    "https://pollinations-ci-bucket.s3.amazonaws.com/avatars1/ab504543.png",
                    "https://pollinations-ci-bucket.s3.amazonaws.com/avatars1/f9d3e86c.png"
                ],
                "reserved_avatars": [
                    "https://pollinations-ci-bucket.s3.amazonaws.com/avatars1/1b3ca4e4.png",
                    "https://pollinations-ci-bucket.s3.amazonaws.com/avatars1/ab504543.png"
                ]
            }
        ]
    }
    ```
  - 200
    If the avatar generation is in progress, 
    ```JSON
    {
    "result": [
        {
            "status": "generating"
        }
    ]
    }
    ```
#### Reserve avatar

- Curl command
  ```bash
  curl --location --request POST 'https://crab.wedatanation.dataunion.app/api/v1/user/reserve-avatar' \
  --header 'Authorization: Bearer <access_token>' \
  --header 'Content-Type: application/json' \
  --data-raw '{
      "image_url": "https://pollinations-ci-bucket.s3.amazonaws.com/avatars1/ab504543.png"
  }'
  ```

    - Response
        - 200
      ```JSON
      {
        "result": {
            "description": null,
            "images": [
                "https://pollinations-ci-bucket.s3.amazonaws.com/avatars1/ab504543.png"
            ],
            "num_suggestions": null,
            "reserved": true,
            "user_id": "dataunion-0x8438979b692196FdB22C4C40ce1896b78425555A"
        },
        "status": "success"
      }
      ```

#### Messages

- Example

  ```bash
  curl --location --request GET 'http://localhost:8080/staticdata/query-view?design-doc=wedatanation&view=messages&query-type=all' \
  --header 'Authorization: Bearer <access_token>'
  ```

- Response

  ```JSON
  {
    "result": [
        [
            "a",
            "b",
            "c"
        ]
    ]
  }
  ```

### Survey APIs

#### JSON format of the surveys

```JSON
{
"name" : ,
"id" : ,
"end_date" : ,
"vote_limit" : <optional_value>,
"cover_image" : <optional_image>,
"external_media_url" : <optional_string>,
"survey_link" : ,
"result_image" : <optional_image>,
"result_external_url" : <optional_string>,
"result_message" : ,
"display_answer_log" : ,
"consecutive_surveys" : [
"consecutive_survey_id1" : , /* refers to the id of the survey /
"consecutive_survey_id2" : ,
"consecutive_survey_id3" : ,
"consecutive_survey_id4" :
],
"questions": [
"id": ,
"type": text | scale | select,
"question": ,
"external_media_url" : <optional_string>,
"external_url": <optional_string>,
"answers_options" : [ / for type select */
"option1" : ,
"option2" : ,
"option3" : ,
"option4" : ,
],
"default_answer" : ,
"required" :
]
}
```

#### Create a survey

- Description
  Input file should be a valid json with all information related to survey.
- Curl request
  ```bash
  curl --location --request POST 'http://localhost:8080/api/v1/upload/user-data' \
  --header 'Authorization: Bearer <access_token>' \
  --form 'file=@"<file_path>/survey.json"' \
  --form 'type="survey"'
  ```
- Response
    - 200
  ```JSON
  {
    "id": "kUubHermGHzwEXD"
  }
  ```

#### User: Query survey list

- Curl example
  ```bash
  curl --location --request POST 'http://localhost:8080/api/v1/query-metadata' \
  --header 'Authorization: Bearer <access_token>' \
  --header 'Content-Type: application/json' \
  --data-raw '{
      "type": "json",
      "sub-type" : "survey",
      "skip": 0,
      "limit": 100,
      "annotation_type" : "survey_response"
  }'
  ```
- Response
    - 200
  ```JSON
  {
    "result": [
        {
            "doc_id": "kUubHermGHzwEXD",
            "public": {
                "end_date": "",
                "questions": [
                    {
                        "id": 1,
                        "label": "",
                        "name": "tyui",
                        "options": [
                            {
                                "id": 1,
                                "name": "a"
                            },
                            {
                                "id": 2,
                                "name": "b"
                            }
                        ],
                        "type": "choice"
                    }
                ],
                "survey_name": ""
            }
        }
    ]
  } 
  ```

#### User: Submit survey

- Curl example
  ```bash
  curl --location --request POST 'http://localhost:8080/api/v1/metadata/annotation' \
  --header 'Authorization: Bearer <access_token>' \
  --header 'Content-Type: application/json' \
  --data-raw '{
      "entity_id": "nSfwbutZaRUBXbr",
      "annotations":[
          {
              "type": "survey_response",
              "data": {
                  "test": 123
              }
          }
      ]
  }'
  ```
- Response
  - 200
    ```JSON
    {
    "status": "success"
    }
    ```
  - 400
    ```JSON
    {
        "messages": [
            "Already submitted [survey_response] for entity"
        ],
        "status": "failed"
    }
    ```
