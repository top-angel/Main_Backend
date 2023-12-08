# Crab documentation

Supported HTTP REST apis

## Metadata

[Metadata apis](READMEs/API-Metadata.md)

#### /api/v1/query-tags

- method: POST
- Description: This api is to search tags for a list of image ids. The response returns up-votes and down-votes from the
  verifications and count of bounding boxes from the annotations.
- Authorization header (required): Bearer token

- Example
    ```bash
    curl --location --request POST 'http://localhost:8080/api/v1/query-tags' \
    --header 'Authorization: Bearer <token>' \
    --header 'Content-Type: application/json' \
    --data-raw '{
        "image_ids": [
            "00000000000000ff",
            "0000000000000244"
          ]
    }'
    ```
- Response:
    ```
    {
        "result": [
            {
                "image_id": "00000000000000ff",
                "value": [
                    {
                        "bounding_boxes": 0,
                        "down_votes": 0,
                        "tag": "Dark",
                        "up_votes": 0
                    },
                    {
                        "bounding_boxes": 5,
                        "down_votes": 0,
                        "tag": "Black",
                        "up_votes": 0
                    }
                ]
            },
            {
                "image_id": "0000000000000244",
                "value": [
                    {
                        "bounding_boxes": 0,
                        "down_votes": 0,
                        "tag": "Loxodonta africana",
                        "up_votes": 0
                    }
                ]
            }
        ],
        "status": "success"
    }
    ```

##### /api/v1/annotate

- method: POST
- Authorziation header (required): Bearer token
- body parameters
    - tags (optional)
    - image_id
    - description (optional)
      e.g.
      ```JSON
      {
        "image_id" : "abx",
        "tags" : ["t1", "t2"],
        "description" : "sample desc"
      }
      ```

- Response:
  ```JSON
  {"status": "success"}
    ```

- **POST** `/api/v1/bulk/upload-zip`

    - method: POST

- **GET** `/api/get/my-metadata`
    - Response:
    ```JSON
    {
        "page": 1,
        "page_size": 100,
        "result": [
            {
                "_id": "cimHzaQSxK",
                "tag_data": [
                    {
                        "created_at": 1611057900.844088,
                        "other": {
                            "description": "sample text"
                        },
                        "tags": [
                            "t1,ty"
                        ],
                        "updated_at": 1611057900.844088,
                        "uploaded_by": "0x60E41b9d32Ef84a85fd9D28D88c57B4EEd730eDa"
                    }
                ]
            }
        ]
    }
    ```

- /api/v1/my-images

    - method: GET

    - Authorziation header (required): Bearer token

    - parameters:
        - page: (optional) This is a number.

    - response
        - 200
        ```JSON
                   {
                       "page": 1, "page_size": 100,
                       "result": [
                         {
                          "filename": "bf7ffffe72f00000-img5.PNG",
                          "hash": "bf7ffffe72f00000",
                          "type": "image",
                          "uploaded_at": 1612003116.712261
                         }
                        ]
                    }
        ```

#### /api/v1/get-image-by-id

    - method: GET

    - parameters:
        - id : Required. This is the image id.

    - response - 200 Image

- /api/v1/report-images

    - method: POST

    - Authorziation header (required): Bearer token

    - parameters:
        - photos: (required) This is the list of json objects e.g. ```[{"photo_id": image_id}]```.

  body e.g. {'photos': [{'photo_id': 'abc'}]}

    - response
        - 200
        ```JSON
        {"status": "success"}
        ```

- **POST** `/api/v1/verify-image`

    - Authorziation header (required): Bearer token

    - body:
        - data: (required)
        - e.g.
          ```JSON
          {
            "image_id" :"6404e078ddb331f2",
            "verification" :{
              "tags":{
                  "up_votes":["t1"],
                  "down_votes":["my own down vote"]
              },
            "descriptions":{
                  "up_votes":[],
                  "down_votes":["test_sDescription 2"]
              }  
            },
            "annotation" :{
              "tags":["tag1","tag2"],
              "description":"sample text"
            }
          }
          ```

    - Response:
        - 200
          ```JSON 
              {"status": "success"}
          ```

#### **GET** `/api/v1/image/thumbnail`
- parameter:
    - image_id: (required) string

- response
    - 200 Thumbnail image
- Example:
    ```bash
    curl --location --request GET 'http://localhost:8080/api/v1/image/thumbnail?image_id=ffffff9fafe62000' --header 'Authorization: Bearer <access_token>'
    ```

- **GET** `/api/v1/tags`

    - Authorziation header (required): Bearer token
    - parameter:
        - status: (required) string `VERIFIABLE`/`VERIFIED`
    - response
        - 200 List of tags for the images with input status.
    - Example:
        ```bash
        curl --location --request GET 'http://localhost:8080/api/v1/tags?status=VERIFIED' --header 'Authorization: Bearer <access_token>'        
        ```
    - Response
    - 200
       ```JSON
       {
       "status": "success",
       "tags": [
           "anonymization bounty",
           "barge"
         ]
       }
       ```
- **POST** `/api/v1/videos/upload`
    - Authorziation header (required): Bearer token
    - body(multipart/form-data):
        - file: (required) GIF image or Video file
    - response
        - 200
            ```JSON
            {
                "message": "File successfully uploaded",
                "id": "<ID of the created gif/video entity>"
            }
            ```
        - 400
            ```JSON
            {
                "status": "failed",
                "messages": "<Array of error messages>"
            }
            ```

- **GET** `/api/v1/videos/<video_id>/download`
    - Authorziation header (required): Bearer token
    - response
        - 200: Video/GIF file

***

## Staticdata

- **GET** `/staticdata/tags`

    - parameters:
        - type (required)
          RECOMMENDED_WORDS or BANNED_WORDS


- **GET** `/staticdata/user-count`
    - parameters: None



