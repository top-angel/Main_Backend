## Entity lists

#### api/v1/missions/info

This returns all the missions for a specific user (the one with the access token) that they started (in progress) or
completed.

- method: GET
- Authorization header (required): Bearer token
- Description: Use this api to get the mission related information for the user. Api will return maximum 100 results in
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
      curl --location --request GET 'http://localhost:8080/api/v1/missions/info?type=upload&status=completed&page=1' \
      --header 'Authorization: Bearer <access_token>'
      ```
    - Responses:
    - 200
       ```JSON
       {
        "missions": [
          {
              "criteria": {
                  "target": 10
              },
              "description": "bd",
              "bounty_id": "bounty:EtipvJMJRDnAJBn",
              "id": "mission:yMHtWfOHonczzBY",
              "image": "not-so-easy-todo",
              "level": 1,
              "progress": 0,
              "status": "ready_to_start",
              "title": "bname",
              "type": "upload"
          },
          {
              "criteria": {
                  "target": 10
              },
              "description": "bd",
              "bounty_id": "bounty:EtipvJMJRDnAJBn",
              "id": "mission:vJNMZYKbvneMMAG",
              "image": "not-so-easy-todo",
              "level": 1,
              "progress": 0,
              "status": "ready_to_start",
              "title": "bname",
              "type": "upload"
          }
      ],
      "total_count": 2
      }
      ```

#### api/v1/missions/

Get mission information by mission id.

- method: GET
- Authorization header (required): Bearer token
- Description: Use this api to get the mission related information for the user by mission id.
- Parameters:
    - `mission_id`: str - required
    - Example:
      ```bash
      curl --location --request GET 'http://localhost:8080/api/v1/missions/?mission_id=mission:rZqpoNXreLYWrGX' \
      --header 'Authorization: Bearer <access_token>'
      ```
    - Responses:
    - 200
       ```JSON
        {    
            "created_at": "2022-04-03T14:51:44.714837",
            "created_by": "0x8438979b692196FdB22C4C40ce1896b78425555A",
            "criteria": {
                "target": 10
            },
            "description": "bd",
            "id": "mission:rZqpoNXreLYWrGX",
            "bounty_id": "bounty:rer45645g",
            "level": 1,
            "progress": 2,
            "status": "in_progress",
            "title": "bname",
            "type": "verify"
        }
      ```
