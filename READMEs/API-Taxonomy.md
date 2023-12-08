# Taxonomy API

## API usage flow:

1. Obtain `access_token` using authentication apis.
2. Call `/api/v1/taxonomy/data` to obtain list of `image_ids` and corresponding `labels` for each `image_id`.
3. Fetch the image by `image_id` using `/api/v1/taxonomy/image`
4. Fetch the label image by `label_id` (caching on client-side recommended).
5. Show the image and label to the user with buttons
    - `Yes`- meaning label and image match.
    - `No` - meaning label and image do not match.

6. Send user response to backend using `/api/v1/taxonomy/store`.

### Rest endpoints

#### /api/v1/taxonomy/store

- Type: POST
- Description:
- Authorization header (required): Bearer token
- Body:
  ```JSON
  {
       "image_id": "mUHkWNcTJg",
       "response" : "NO"
  }
  ```
- Response:
   ```JSON
  {"status": "success"} 
  ```
- Example:
    ```bash
    curl --location --request POST 'http://localhost:8080/api/v1/taxonomy/store' \
    --header 'Authorization: Bearer <access_token>' \
    --header 'Content-Type: application/json' \
    --data-raw '{
        "image_id": "mUHkWNcTJg",
        "response" : "NO"
    }'
    ```

#### /api/v1/taxonomy/image

- Type: GET
- Authorization header (required): Bearer token
- Description:
- Body
- Response:

    - 200: Image
- Example:
    ```bash
    curl --location --request GET 'http://localhost:8080/api/v1/taxonomy/image?image_id=mUHkWNcTJg' \
    --header 'Authorization: Bearer <access_token>'
    ```

#### /api/v1/taxonomy/data

- Type: GET
- Description:
- Authorization header (required): Bearer token
- Response
    - 200:
      List of `image_id` and `label`.
    - e.g.
       ```JSON
       {
        "result": [
            {
                "image_id": "KUBREpbQEV",
                "label": "14006"
            },
            {
                "image_id": "KIxCJeiDsF",
                "label": "10028"
            }
        ],
        "status": "success"
       }
       ```

- Example:
   ```bash
   curl --location --request GET 'http://localhost:8080/api/v1/taxonomy/data'\
    --header 'Authorization: Bearer <access_token>'
   ```

#### /api/v1/taxonomy/image-label

- Type: GET
- Authorization header (required): Bearer token
- Parameters:
    - `label_id`: label id
- Response:

    - 200: Image
- Example
    ```bash
    curl --location --request GET 'http://localhost:8080/api/v1/taxonomy/label?label_id=bFiLhzXzgO' \
    --header 'Authorization: Bearer <access_token>'
    ```

#### /api/v1/taxonomy/user-stats

- Type: GET
- Authorization header (required): Bearer token
- Parameters:
    - `start_date`- date in dd-mm-yyyy format
    - `end_date` - date in dd-mm-yyyy format
- Response:

    - 200: The number of swipe (YES/NO) done by the user per day in the given date range.
    
- Example
    ```bash
    curl --location --request GET 'http://localhost:8080/api/v1/taxonomy/user-stats?start_date=01-01-2021&end_date=01-12-2021' \
    --header 'Authorization: Bearer <access_token>'
    ```
- Sample response:
  ```
  {
    "result": {
        "NO": [
            {
                "date": "12-06-2021",
                "value": 1
            }
        ],
        "YES": [
            {
                "date": "12-06-2021",
                "value": 2
            }
        ]
    },
    "status": "success"
  }
  ```

- Validations in backend:
1. Date in dd-mm-yyyy format
2. Max 1-year data can be queried from backend.



#### /api/v1/taxonomy/overall-stats

- Type: GET
- Parameters:
    - `start_date`- date in dd-mm-yyyy format
    - `end_date` - date in dd-mm-yyyy format
- Response:

    - 200: The number of swipe (YES/NO) done in the given date range.
    
- Example
    ```bash
    {{server}}/api/v1/taxonomy/overall-stats?start_date=01-01-2021&end_date=01-12-2021
    ```
- Sample response:
  ```
  {
    "result": {
        "NO": [
            {
                "date": "20-05-2021",
                "value": 1
            },
            {
                "date": "12-06-2021",
                "value": 1
            }
        ],
        "YES": [
            {
                "date": "12-06-2021",
                "value": 2
            }
        ]
    },
    "status": "success"
  }
  ```

- Validations in backend:
1. Date in dd-mm-yyyy format
2. Max 1-year data can be queried from backend.

### Loading data into taxonomy database (for backend developers)

1. Login into server where the crab is running.
2. Copy the taxonomy data into the folder where docker volume is mapped with the container (check `Marine`
   docker-compose `.yml` file)
3. Login into docker container using `docker exec -it <container_name> bash`.
    - e.g `docker exec -it crab_backend_dev bash`

4. Run the command `python -m helpers.load_taxonomy_data <path_of_the_folder_inside_the_container>`
