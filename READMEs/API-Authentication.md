## Authentication

#### /login

- method: POST
- description: Obtain an access token and a refresh token
- body:
    - parameters
        - `source`: Can be `brainstem`/`default`/`dataunion`/`wedatanation`/`other`. If not given `default` value is
          used.
    - Example
      ```JSON
      {
        "public_address": "0x0C82d6217153F58adB9C8350D9E148Fce978BF47",
        "signature": "<signature>",
        "source": "<words to say where it signs in from which app>"
      }
      ```
      (Note: source field is optional)

- /logout
- /get-nonce
    - method: GET
    - e.g. `http://localhost:8080/get-nonce?public_address=<public_address>

- /register
    - method: POST
    - body:
      - Parameters:
        - `referral_id`: Optional string, referral code
        - `public_address`: Public address of the account
        - `source`: Can be `litterbux`/`default`/`dataunion`/`wedatanation` 
      - Example
          ```JSON
            { 
              "public_address" : "<public_address>",
              "referral_id" : "<referral code>",
              "source": "words to say where it signs in from which app"
            }
          ```
          (Note: source/referral_id field is optional)

- **POST** `/refresh`
    - Example:
        ```bash
        curl --location --request POST 'http://localhost:8080/refresh' --header 'Authorization: Bearer <refresh_token>'
        ```
- /revoke-refresh-token

- /check

#### Login with email and password


- Example
    ```bash
    curl --location --request POST 'http://localhost:8080/login-with-email' \
    --header 'Content-Type: application/json' \
    --data-raw '{
      "email": "user@example.com",
      "password": "1234qwer"
    }'
    ```

- Response
  ```JSON
  {
    "status": "success",
    "access_token": "access_token",
    "refresh_token": "refresh_token"
  }  

#### /usage-flag POST

- method: POST
- Authorization header (required): Bearer token
- Description:
- Body parameters:
    - flag: REJECTED/ACCEPTED
- Example
  ```
  curl --location --request POST 'http://localhost:8080/usage-flag' \
  --header 'Authorization: Bearer <access_token>' \
  --header 'Content-Type: application/json' \
  --data-raw '{
      "flag" : "REJECTED"
  }'
  ```
- Response
  ```JSON
  {
      "status": "success"
  }
  ```

#### /usage-flag GET

- method: GET
- Authorization header (required): Bearer token
- Description:
- Example
  ```
  curl --location --request GET 'http://localhost:8080/usage-flag' \
  --header 'Authorization: Bearer <access_token>'
  ```
- Response
  ```JSON
  {
    "usage_flag": "UNKNOWN"
  }
  ```

#### Get referral id

- method: GET
- Authorization header (required): Bearer token
- Example
    ```bash
    curl --location --request GET 'http://localhost:8080/api/v1/user/referral-id' \
    --header 'Authorization: Bearer <access_token>'
    ```

- Response
    ```JSON
    {
      "result": {
        "referral_id": "CoRCp",
        "referred_users_count": 0
      }
    }
    ```

### Avatar management

#### Get user avatar

- method: GET
- Authorization header (required): Bearer token
- Example
    ```bash
    curl --location --request GET 'http://localhost:8080/api/v1/user/query-view?design-doc=user-info&view=avatar&query-type=user_id' \
    --header 'Authorization: Bearer <access_token>'
    ```

- Response
    ```JSON
    {
        "result": [
            {
                "avatar": [
                    "Rabbit",
                    "doctor",
                    "Guitar"
                ],
                "public_address": "0x8438979b692196FdB22C4C40ce1896b78425555A"
            }
        ]
    }
    ```
  
#### Start avatar generation


- Example
    ```bash
    curl --location --request POST 'http://localhost:8080/api/v1/user/avatar/generate' \
    --header 'Authorization: Bearer <access_token>' \
    --header 'Content-Type: application/json' \
    --data-raw '{
    }'
    ```

- Response
  ```JSON
  {
    "status": "success"
  }  
  ```

#### Stop avatar generation

- Example

    ```bash
    curl --location --request POST 'http://localhost:8080/api/v1/user/avatar/cancel' \
    --header 'Authorization: Bearer <access_token>' \
    --header 'Content-Type: application/json' \
    --data-raw '{}'
    ```
  
- Response
  - 200
    ```JSON
    {
      "status": "success"
    }  
    ```
  
  - 400
    ```bash
    {
      "messages": [
          "No avatar generation task running"
      ],
      "status": "failed"
    }  
    ```

### Profile Image
- /set_profile_image
    - Method: POST
    - Authorization header (required): Bearer token
    - Body:
      - Parameters:
        - `file`: File to upload
    - Example
      curl --location 'http://127.0.0.1:8080/set_profile_image' \
      --header 'Authorization: Bearer <access_token>' \
      --form 'file=@"/home/dawood/Desktop/IMG_0572.jpeg"' \
    Note (valid format of some parameters):
    ```bash
    - file: " jpg, jpeg, png, gif "
    ```
  - Response:
      - 200
    ```JSON
    {
      "image": "/var/www/html/Marine/Crab/data/0x861E95B76021618eb9a03526b8cbbcDb6BbCEE56/profile_images/IMG_0572.jpeg",
      "message": "Profile image set successfully"
    }
    ```
      - 400
    ```JSON
    {
      "messages": "Invalid request parameters or file format"
    }
    ```

- /get_profile_image
  - method: GET
  - Authorization header (required): Bearer token
  - Url Param : public_address
  - Example
      ```bash
      curl --location 'http://127.0.0.1:8080/get_profile_image/0x861E95B76021618eb9a03526b8cbbcDb6BbCEE56' \
      --header 'Authorization: Bearer <access_token>'
      ```

  - Response
      ```JSON
      - 200
      image content

      - 404
      {
        "error": ["User or profile image not found", "Profile image not found"]
      }
      ```

### User profile API - get

- Example
  ```bash
  curl --location 'localhost:8080/api/v1/profile' \
    --header 'Authorization: Bearer <access token>'
  ```
- Response
  ```JSONQ
  {
    "result": {
      "id": "<id>",
      "roles": ["creator]
      "profile": {
        "address": "address",
        "company_title": "data-union",
        "country": "country",
        "email": "test@domain.com"
      }
    },
    "status": "success"
  }
  ```

### User profile API - set

- Example
  ```bash
  curl --location --request PUT 'localhost:8080/api/v1/profile' \
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