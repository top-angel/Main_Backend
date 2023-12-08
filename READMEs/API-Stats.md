# Stats rest endpoints

## User Stats

#### /api/v1/stats/tags

- method: GET
- Parameters:
    - bounty : string
- Example:
  ```bash
  curl --location --request GET 'http://localhost:8080/api/v1/stats/tags?bounty=roman-letter-bounty'
  ```
- Response:
    - 200
  ```JSON
  {
    "result": [
        {
            "count": 177,
            "tag": "iii"
        },
        {
            "count": 281,
            "tag": "iv"
        },
        {
            "count": 234,
            "tag": "ix"
        },
        {
            "count": 1640,
            "tag": "roman-letter-bounty"
        },
        {
            "count": 196,
            "tag": "v"
        },
        {
            "count": 181,
            "tag": "vi"
        },
        {
            "count": 193,
            "tag": "vii"
        },
        {
            "count": 199,
            "tag": "viii"
        },
        {
            "count": 179,
            "tag": "x"
        }
    ],
    "status": "success"
  }
  ```

#### `/api/v1/stats/user`

- method: GET
- Parameters:
    - start_date: Date in 'dd-mm-yyyy' format
    - end_date: Date in 'dd-mm-yyyy' format
    - entity_type: (optional) string Value can be `image`/`video`
- Example:
  ```bash
    curl --location --request GET 'http://localhost:8080/api/v1/stats/user?start_date=01-01-2018&end_date=06-06-2021' --header 'Authorization: Bearer <access_token>'
  ```

- Response:
    - 200
    ```JSON
       {
        "result": {
            "tag_annotations": [
                {
                    "date": "6-5-2021",
                    "value": 18
                }
            ],
            "pixel_annotations": [
                {
                "date": "6-5-2021",
                "value": 2
                }
            ],
            "text_annotations": [
                {
                    "date": "6-5-2021",
                    "value": 5
                }
            ],
            "uploads": [
                {
                    "date": "6-5-2021",
                    "value": 1
                }
            ],
            "verifications": [
                {
                    "date": "6-5-2021",
                    "value": 6
                }
            ]
        },
        "status": "success"
    }
    ```

#### `/api/v1/stats/user-graph`

- method: GET
- Parameters:
    - start_date: Date in 'dd-mm-yyyy' format
    - end_date: Date in 'dd-mm-yyyy' format
    - entity_type: (optional) string Value can be `image`/`video`
- Example:
  ```bash
    curl --location --request GET 'http://localhost:8080/api/v1/stats/user-graph?start_date=01-01-2018&end_date=06-06-2021'
  ```
- Response:
    - 200
    ```JSON
    {
        "result": {
        "dates": [
            "10-05-2021",
            "11-05-2021"
        ],
        "pixel_annotations": [
            0,
            2
        ],
        "tag_annotations": [
            0,
            0
        ],
        "text_annotations": [
            0,
            0
        ],
        "verifications": [
            0,
            0
        ]
        },
        "status": "success"
    }
    ```

## Overall

#### `/api/v1/stats/overall`

- method: GET
- Parameters:
    - start_date: Date in 'dd-mm-yyyy' format
    - end_date: Date in 'dd-mm-yyyy' format
    - entity_type: (optional) string Value can be `image`/`video`

- Example:
  ```bash
    curl --location --request GET 'http://localhost:8080/api/v1/stats/overall?start_date=01-01-2018&end_date=06-06-2021''
  ```
- Response:
    - 200
    ```JSON
       {
        "result": {
            "tag_annotations": [
                {
                    "date": "6-5-2021",
                    "value": 18
                }
            ],
            "text_annotations": [
                {
                    "date": "6-5-2021",
                    "value": 5
                }
            ],
            "pixel_annotations": [
                {
                    "date": "6-5-2021",
                    "value": 2
                }
            ],
            "uploads": [
                {
                    "date": "6-5-2021",
                    "value": 1
                }
            ],
            "verifications": [
                {
                    "date": "6-5-2021",
                    "value": 6
                }
            ]
        },
        "status": "success"
    }
    ```

#### `/api/v1/stats/overall-tags`

- method: GET
- Parameters:
    - start_date: Date in 'dd-mm-yyyy' format
    - end_date: Date in 'dd-mm-yyyy' format
    - entity_type: (optional) string Value can be `image`/`video`

- Example:
  ```bash
    curl --location --request GET 'http://localhost:8080/api/v1/stats/overall-tags?start_date=01-01-2018&end_date=06-06-2021''
  ```
- Response:
    - 200
    ```JSON
    {
        "result": {
            "bronchocele": [
                {
                    "date": "6-5-2021",
                    "value": 1
                }
            ],
            "gallantize": [
                {
                    "date": "6-5-2021",
                    "value": 1
                }
            ],
            "pennywinkle": [
                {
                    "date": "6-5-2021",
                    "value": 1
                }
            ],
            "sicca": [
                {
                    "date": "6-5-2021",
                    "value": 1
                }
            ],
            "venomer": [
                {
                    "date": "6-5-2021",
                    "value": 1
                }
            ]
        },
        "status": "success"
    }
    ```
- Validations:
    - Max date range difference: 366 days


- **GET** `/api/v1/stats/overall-graph`
    - Parameters:
        - start_date: Date in 'dd-mm-yyyy' format
        - end_date: Date in 'dd-mm-yyyy' format
        - entity_type: (optional) string Value can be `image`/`video`
    - Example:
      ```bash
        curl --location --request GET 'http://localhost:8080/api/v1/stats/overall-graph?start_date=01-01-2018&end_date=06-06-2021'
      ```
    - Response:
        - 200
        ```JSON
        {
            "result": {
            "dates": [
                "10-05-2021",
                "11-05-2021"
            ],
            "tag_annotations": [
                0,
                804
            ],
            "text_annotations": [
                0,
                433
            ],
            "verifications": [
                0,
                1845
            ],
            "pixel_annotations": [
                0,
                2
            ]
            },
            "status": "success"
        }
        ```
    - Validations:
        - Max date range difference: 366 days

#### `/api/v1/stats/`

- method: GET
- Parameters:
    - source: The source for which the data is needed. Default null.
- Example:
  ```bash
  curl --location --request GET 'http://localhost:8080/api/v1/stats/'
  ```
- Response:
    - 200
    ```JSON
    {
    "entity_counts": [
        {
            "count": 1,
            "type": "audio"
        },
        {
            "count": 9,
            "type": "image"
        },
        {
            "count": 1,
            "type": "video"
        }
    ],
    "entity_uploads_per_hour": [
        {
            "count": 1,
            "date": "2022-5-16T16:00:00.000000",
            "type": "audio"
        },
        {
            "count": 9,
            "date": "2022-5-16T16:00:00.000000",
            "type": "image"
        },
        {
            "count": 1,
            "date": "2022-5-16T16:00:00.000000",
            "type": "video"
        }
    ],
    "handshake_count": 3,
    "handshakes_per_hour": [
        {
            "count": 2,
            "date": "2022-4-29T14:00:00.000000"
        },
        {
            "count": 1,
            "date": "2022-5-14T20:00:00.000000"
        },
        {
            "count": 1,
            "date": "2022-5-16T8:00:00.000000"
        }
    ],
    "rewards": [
        {
            "type": "image",
            "value": 1
        },
        {
            "type": "audio",
            "value": 1
        },
        {
            "type": "video",
            "value": 1
        }
    ]
    }
    ```

#### `/api/v1/stats/events`

- method: GET
- Parameters:
    - source: The source for which the data is needed. Default null.
    - start-time: datetime
    - end-time: datetime
    - handshakes: boolean flag
    - entities: boolean flag
- Example:
    - Without source field:
      ```bash
      curl --location --request GET 'http://localhost:8080/api/v1/stats/events?
      start-time=17-05-2021 00:00:00&
      end-time=18-05-2022 23:00:00&
      handshakes=true&
      entities=true'
      ```
    - With source field:
      ```bash
      curl --location --request GET 'http://localhost:8080/api/v1/stats/events?
      start-time=17-05-2021 00:00:00&
      end-time=18-05-2022 23:00:00&
      handshakes=true&
      entities=true&
      source=test'
      ```
- Response:
    - 200
    ```JSON
    {
    "entities": [
        {
            "date": "17-5-2022 12:56:52",
            "location": {
                "latitude": "123",
                "longitude": "123123"
            },
            "type": "image"
        },
        {
            "date": "17-5-2022 12:58:23",
            "location": {
                "latitude": null,
                "longitude": null
            },
            "type": "image"
        },
        {
            "date": "17-5-2022 12:59:42",
            "location": {
                "latitude": null,
                "longitude": null
            },
            "type": "image"
        },
        {
            "date": "17-5-2022 13:1:12",
            "location": {
                "latitude": null,
                "longitude": null
            },
            "type": "image"
        },
        {
            "date": "17-5-2022 13:41:3",
            "location": {
                "latitude": null,
                "longitude": null
            },
            "type": "image"
        },
        {
            "date": "17-5-2022 13:41:35",
            "location": {
                "latitude": "123",
                "longitude": "345"
            },
            "type": "image"
        }
    ],
    "handshakes": [
        {
            "date": "29-4-2022 14:50:11",
            "location": {
                "latitude": "1232",
                "longitude": "32223"
            }
        },
        {
            "date": "29-4-2022 14:50:39",
            "location": {
                "latitude": "1232",
                "longitude": "32223"
            }
        },
        {
            "date": "14-5-2022 20:17:12",
            "location": {
                "latitude": 123,
                "longitude": 234
            }
        },
        {
            "date": "16-5-2022 8:31:51",
            "location": {
                "latitude": 123,
                "longitude": 234
            }
        },
        {
            "date": "16-5-2022 8:57:20",
            "location": {
                "latitude": 123,
                "longitude": 234
            }
        }
    ]
    }
    ```

#### **GET** `/api/v1/stats/success-rate`

- Parameters:
    - None
- Example:
    ```bash
       curl --location --request GET 'http://localhost:8080/api/v1/stats/success-rate' \
         --header 'Authorization: Bearer <access_token>'
    ```
- Response:
    - 200
       ```JSON
       {
            "classification_count": 4,
            "correct": {
                "knee": 1,
                "shoulder": 1
            },
            "knee_classification_percentage": 1.5152,
            "shoulder_classification_percentage": 2.7778,
            "success_rate_knee": 33.3333,
            "success_rate_shoulder": 100.0,
            "success_rate_total": 66.66665,
            "total": {
                "knee": 3,
                "shoulder": 1
            }
        }
      ```

#### /api/v1/stats/classifications

- method: GET
- Parameters:
    - None
- Example:
    ```bash
       curl --location --request GET 'http://localhost:8080/api/v1/stats/classifications'
    ```
- Response
    - 200
      ```bash
        [
        {
            "correct_classifications": 4,
            "incorrect_classifications": 1,
            "public_address": "0x8438979b692196FdB22C4C40ce1896b78425555A",
            "referrals": 1,
            "total_classifications": 5,
            "user_name" : "abc"
        },
        {
            "correct_classifications": 1,
            "incorrect_classifications": 1,
            "public_address": "0xdF1dEc52e602020E27B0644Ea0F584b6Eb5CE4eA",
            "referrals": 0,
            "total_classifications": 2,
            "user_name" : null
        }
        ]
        ```

#### /api/v1/stats/reduced

- Description: General stats API
- Parameters:
    - `db-name`: Required
    - `design-doc`: Required
    - `view`: Required
- Examples:
    - Example-1: Brainstem stats
        - Usage
            ```bash
            curl --location --request GET 'http://localhost:8080/api/v1/stats/reduced?db-name=metadata&design-doc=brainstem&view=recording-durations'
            ```
        - Response
            ```JSON
            [
                {
                    "count": 55016,
                    "duration": 55090.576999902725
                }
            ]
            ```