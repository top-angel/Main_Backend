# Ncight apis

### User management API

#### Register

```bash
curl --location --request POST 'https://crab.ncight.dataunion.app/register' \
--header 'Content-Type: application/json' \
--data-raw '{
    "public_address" : "<public_address>"
}'
```

#### Login

```bash
curl --location --request POST 'https://crab.ncight.dataunion.app/login' \
--header 'Content-Type: application/json' \
--data-raw '{
    "public_address": "0xxx82xx2xx1xxxx8adB9xxxxx9xx48Fce978BFxx",
    "signature": "<signature>",
    "source" : "ncight"
}'
```

### Upload data APIs

#### Upload user metadata file

```bash
curl --location --request POST 'https://crab.ncight.dataunion.app/api/v1/upload-file' \
--header 'Authorization: Bearer <access_token>' \
--form 'file=@"/home/ash/Desktop/git/Crab/tests/data/ncight/user_metadata.json"' \
--form 'annotations="[]"' \
--form 'file-type="user_metadata"'
```

#### Upload image with annotations

```bash
curl --location --request POST 'https://crab.ncight.dataunion.app/api/v1/upload-file' \
--header 'Authorization: Bearer <access_token>' \
--form 'file=@"/home/ash/Pictures/2022-09-30_16-09.png"' \
--form 'annotations="[{\"type\": \"TrueTag\", \"tags\": [\"knee\"]}]"' \
--form 'file-type="image"'
```

  
#### Get ncight user ranks

- Example
  ```bash
  curl --location --request GET 'http://localhost:8080/api/v1/other/query-view?design-doc=ncight&view=user-ranks&query-type=all' \
  --header 'Authorization: Bearer <access_token>
  ```
  
- Response
  ```JSON
  {
        "result": [
            [
                {
                    "address": "0x8438979b692196FdB22C4C40ce1896b78425555A",
                    "score": 25.25,
                    "username": "abc",
                    "value": {
                        "classification_accuracy": 100,
                        "referrals": 9,
                        "total_classifications": 1
                    }
                },
                {
                    "address": "0xdF1dEc52e602020E27B0644Ea0F584b6Eb5CE4eA",
                    "score": 23.150000000000002,
                    "username": "<default=some random string> e.g. NpXrKISUZE",
                    "value": {
                        "referrals": 5,
                        "upload": 102
                    }
                },
                {
                    "address": "0x1f1dEC52E602020e27b0644EA0f584B6EB5Ce4eB",
                    "score": 0,
                    "username": "123",
                    "value": {
                        "referrals": 0
                    }
                }
            ]
        ]
  }
  ```